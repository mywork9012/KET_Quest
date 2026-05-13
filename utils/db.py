"""
数据库层：SQLite管理用户学习进度 + 游戏化数据
表结构：users / word_progress / fill_records / game_profile / badges
"""

import sqlite3
import json
from datetime import datetime, date, timedelta
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "ket_progress.db"
WORDS_PATH = Path(__file__).parent.parent / "data" / "words.json"


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    with get_conn() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            username     TEXT PRIMARY KEY,
            display_name TEXT NOT NULL,
            created_at   TEXT NOT NULL,
            start_date   TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS word_progress (
            username    TEXT NOT NULL,
            word_id     INTEGER NOT NULL,
            status      TEXT NOT NULL DEFAULT 'new',
            correct     INTEGER NOT NULL DEFAULT 0,
            wrong       INTEGER NOT NULL DEFAULT 0,
            last_seen   TEXT,
            next_review TEXT,
            streak      INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY (username, word_id)
        );

        CREATE TABLE IF NOT EXISTS fill_records (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            username   TEXT NOT NULL,
            word_id    INTEGER NOT NULL,
            mode       TEXT NOT NULL,
            result     INTEGER NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS game_profile (
            username      TEXT PRIMARY KEY,
            xp            INTEGER NOT NULL DEFAULT 0,
            level         INTEGER NOT NULL DEFAULT 1,
            coins         INTEGER NOT NULL DEFAULT 0,
            total_correct INTEGER NOT NULL DEFAULT 0,
            total_wrong   INTEGER NOT NULL DEFAULT 0,
            daily_streak  INTEGER NOT NULL DEFAULT 0,
            last_active   TEXT,
            max_combo     INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS badges (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            username  TEXT NOT NULL,
            badge_id  TEXT NOT NULL,
            earned_at TEXT NOT NULL,
            UNIQUE(username, badge_id)
        );
        """)


# ── 词库 ─────────────────────────────────────────────────────────────────

def load_words() -> list:
    with open(WORDS_PATH, encoding="utf-8") as f:
        data = json.load(f)
    return data["words"]


def get_word_by_id(word_id: int):
    for w in load_words():
        if w["id"] == word_id:
            return w
    return None


# ── 用户 ─────────────────────────────────────────────────────────────────

def get_or_create_user(username: str, display_name: str = "") -> dict:
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        if row:
            return dict(row)
        name = display_name or username
        today = date.today().isoformat()
        conn.execute("INSERT INTO users VALUES (?,?,?,?)",
                     (username, name, datetime.now().isoformat(), today))
        conn.execute("INSERT OR IGNORE INTO game_profile (username) VALUES (?)", (username,))
        return {"username": username, "display_name": name,
                "created_at": datetime.now().isoformat(), "start_date": today}


def list_users() -> list:
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM users ORDER BY created_at").fetchall()
        return [dict(r) for r in rows]


# ── 学习进度 ──────────────────────────────────────────────────────────────

EBBINGHAUS = [1, 2, 4, 7, 15, 30, 60]


def _next_review_date(streak: int) -> str:
    idx = min(streak, len(EBBINGHAUS) - 1)
    return (date.today() + timedelta(days=EBBINGHAUS[idx])).isoformat()


def get_all_progress(username: str) -> dict:
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM word_progress WHERE username=?", (username,)).fetchall()
        return {r["word_id"]: dict(r) for r in rows}


def upsert_progress(username: str, word_id: int, correct: bool) -> dict:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM word_progress WHERE username=? AND word_id=?",
            (username, word_id)).fetchone()
        now = datetime.now().isoformat()
        if row is None:
            streak = 1 if correct else 0
            c, w = (1, 0) if correct else (0, 1)
            conn.execute(
                """INSERT INTO word_progress
                   (username,word_id,status,correct,wrong,last_seen,next_review,streak)
                   VALUES (?,?,?,?,?,?,?,?)""",
                (username, word_id, "learning", c, w, now, _next_review_date(streak), streak))
            return {"streak": streak, "correct": correct}
        else:
            streak = (row["streak"] + 1) if correct else 0
            c = row["correct"] + (1 if correct else 0)
            w = row["wrong"] + (0 if correct else 1)
            if streak >= 5:
                status = "known"
            elif not correct:
                status = "learning"
            else:
                status = row["status"] if row["status"] != "new" else "learning"
            conn.execute(
                """UPDATE word_progress
                   SET status=?,correct=?,wrong=?,last_seen=?,next_review=?,streak=?
                   WHERE username=? AND word_id=?""",
                (status, c, w, now, _next_review_date(streak), streak, username, word_id))
            return {"streak": streak, "correct": correct}


def get_today_review_ids(username: str) -> list:
    today = date.today().isoformat()
    with get_conn() as conn:
        rows = conn.execute(
            """SELECT word_id FROM word_progress
               WHERE username=? AND next_review<=? AND status!='new'
               ORDER BY next_review""",
            (username, today)).fetchall()
        return [r["word_id"] for r in rows]


def get_stats(username: str) -> dict:
    progress = get_all_progress(username)
    words = load_words()
    total = len(words)
    learning = sum(1 for p in progress.values() if p["status"] == "learning")
    known = sum(1 for p in progress.values() if p["status"] == "known")
    tc = sum(p["correct"] for p in progress.values())
    tw = sum(p["wrong"] for p in progress.values())
    accuracy = tc / (tc + tw) if (tc + tw) > 0 else 0.0
    with get_conn() as conn:
        user = conn.execute("SELECT start_date FROM users WHERE username=?", (username,)).fetchone()
    start = date.fromisoformat(user["start_date"]) if user else date.today()
    days_elapsed = (date.today() - start).days + 1
    return {
        "total": total, "new": total - len(progress),
        "learning": learning, "known": known,
        "accuracy": accuracy,
        "review_due": len(get_today_review_ids(username)),
        "days_elapsed": days_elapsed,
        "days_left": max(0, 120 - days_elapsed),
    }


def get_weak_words(username: str, limit: int = 10) -> list:
    with get_conn() as conn:
        rows = conn.execute(
            """SELECT word_id, wrong*1.0/(correct+wrong+0.001) AS err_rate, correct, wrong
               FROM word_progress WHERE username=? AND wrong>0
               ORDER BY err_rate DESC LIMIT ?""",
            (username, limit)).fetchall()
    result = []
    for r in rows:
        w = get_word_by_id(r["word_id"])
        if w:
            result.append({**w, "err_rate": r["err_rate"],
                           "correct": r["correct"], "wrong": r["wrong"]})
    return result


def log_fill(username: str, word_id: int, mode: str, result: bool):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO fill_records (username,word_id,mode,result,created_at) VALUES (?,?,?,?,?)",
            (username, word_id, mode, int(result), datetime.now().isoformat()))


# ── 游戏化 ────────────────────────────────────────────────────────────────

# 等级XP阈值
LEVEL_XP = [0, 50, 120, 220, 360, 540, 780, 1080, 1450, 1900, 2500]

# 徽章定义 {badge_id: (名称, 图标, 描述)}
BADGE_DEFS = {
    "first_word":   ("初出茅庐", "🌱", "第一次答对单词"),
    "streak_3":     ("三连击",   "⚡", "连续答对3题"),
    "streak_5":     ("五连击",   "🔥", "连续答对5题"),
    "streak_10":    ("十连击",   "💥", "连续答对10题"),
    "known_10":     ("小有成就", "🥉", "掌握10个单词"),
    "known_50":     ("半百达人", "🥈", "掌握50个单词"),
    "known_100":    ("百词斩",   "🥇", "掌握100个单词"),
    "known_all":    ("KET词王",  "👑", "掌握全部198个单词"),
    "daily_3":      ("三天打卡", "📅", "连续打卡3天"),
    "daily_7":      ("一周坚持", "🗓️", "连续打卡7天"),
    "daily_30":     ("月度冠军", "🏆", "连续打卡30天"),
    "level_5":      ("中级学员", "⭐", "达到5级"),
    "perfect_quiz": ("全对！",   "💯", "一轮10题全对"),
}


def get_game_profile(username: str) -> dict:
    with get_conn() as conn:
        conn.execute("INSERT OR IGNORE INTO game_profile (username) VALUES (?)", (username,))
        row = conn.execute("SELECT * FROM game_profile WHERE username=?", (username,)).fetchone()
        return dict(row)


def get_level_info(xp: int) -> tuple:
    """返回 (当前等级, 本级起始XP, 下级所需XP)"""
    level = 1
    for i, threshold in enumerate(LEVEL_XP):
        if xp >= threshold:
            level = i + 1
    level = min(level, len(LEVEL_XP))
    current_start = LEVEL_XP[level - 1]
    next_threshold = LEVEL_XP[level] if level < len(LEVEL_XP) else LEVEL_XP[-1] + 999
    return level, current_start, next_threshold


def award_xp(username: str, correct: bool, combo: int) -> dict:
    """答题后结算XP和金币，返回结算结果"""
    if correct:
        multiplier = 1.0 + min(combo // 3, 4) * 0.5   # 每3连击+0.5倍，最高3倍
        xp_gained = int(10 * multiplier)
        coins_gained = 1 + (combo // 5)
    else:
        multiplier = 1.0
        xp_gained = 2
        coins_gained = 0

    with get_conn() as conn:
        prof = conn.execute("SELECT * FROM game_profile WHERE username=?", (username,)).fetchone()
        old_xp = prof["xp"] if prof else 0
        new_xp = old_xp + xp_gained
        new_coins = (prof["coins"] if prof else 0) + coins_gained
        tc = (prof["total_correct"] if prof else 0) + (1 if correct else 0)
        tw = (prof["total_wrong"] if prof else 0) + (0 if correct else 1)
        max_combo = max(prof["max_combo"] if prof else 0, combo)

        # 每日打卡
        today = date.today().isoformat()
        last_active = prof["last_active"] if prof else None
        daily_streak = prof["daily_streak"] if prof else 0
        if last_active != today:
            yesterday = (date.today() - timedelta(days=1)).isoformat()
            daily_streak = daily_streak + 1 if last_active == yesterday else 1

        old_level, _, _ = get_level_info(old_xp)
        new_level, _, _ = get_level_info(new_xp)

        conn.execute(
            """UPDATE game_profile SET
               xp=?,level=?,coins=?,total_correct=?,total_wrong=?,
               max_combo=?,last_active=?,daily_streak=?
               WHERE username=?""",
            (new_xp, new_level, new_coins, tc, tw,
             max_combo, today, daily_streak, username))

    return {
        "xp_gained": xp_gained,
        "coins_gained": coins_gained,
        "new_xp": new_xp,
        "level": new_level,
        "leveled_up": new_level > old_level,
        "multiplier": multiplier,
        "daily_streak": daily_streak,
    }


def check_and_award_badges(username: str, combo: int) -> list:
    """检查并发放徽章，返回本次新获得的badge_id列表"""
    stats = get_stats(username)
    prof = get_game_profile(username)
    new_badges = []

    def _try(badge_id):
        with get_conn() as conn:
            exists = conn.execute(
                "SELECT 1 FROM badges WHERE username=? AND badge_id=?",
                (username, badge_id)).fetchone()
            if not exists:
                conn.execute(
                    "INSERT INTO badges (username,badge_id,earned_at) VALUES (?,?,?)",
                    (username, badge_id, datetime.now().isoformat()))
                new_badges.append(badge_id)

    if prof["total_correct"] >= 1: _try("first_word")
    if combo >= 3:  _try("streak_3")
    if combo >= 5:  _try("streak_5")
    if combo >= 10: _try("streak_10")
    if stats["known"] >= 10:  _try("known_10")
    if stats["known"] >= 50:  _try("known_50")
    if stats["known"] >= 100: _try("known_100")
    if stats["known"] >= 198: _try("known_all")
    if prof["daily_streak"] >= 3:  _try("daily_3")
    if prof["daily_streak"] >= 7:  _try("daily_7")
    if prof["daily_streak"] >= 30: _try("daily_30")
    if prof["level"] >= 5: _try("level_5")
    return new_badges


def get_earned_badges(username: str) -> list:
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT badge_id, earned_at FROM badges WHERE username=? ORDER BY earned_at",
            (username,)).fetchall()
    result = []
    for r in rows:
        bid = r["badge_id"]
        if bid in BADGE_DEFS:
            name, icon, desc = BADGE_DEFS[bid]
            result.append({"id": bid, "name": name, "icon": icon,
                           "desc": desc, "earned_at": r["earned_at"]})
    return result
