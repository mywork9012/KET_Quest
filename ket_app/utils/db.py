"""
数据库层：SQLite管理用户学习进度
表结构：users / word_progress / study_logs / review_queue
"""

import sqlite3
import json
import os
from datetime import datetime, date, timedelta
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "ket_progress.db"
WORDS_PATH = Path(__file__).parent.parent / "data" / "words.json"


# ── 初始化 ──────────────────────────────────────────────────────────────

def get_conn() -> sqlite3.Connection:
    """返回带 row_factory 的数据库连接"""
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    """建表（幂等）"""
    with get_conn() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            username    TEXT PRIMARY KEY,
            display_name TEXT NOT NULL,
            created_at  TEXT NOT NULL,
            start_date  TEXT NOT NULL       -- 备考开始日期 YYYY-MM-DD
        );

        CREATE TABLE IF NOT EXISTS word_progress (
            username    TEXT NOT NULL,
            word_id     INTEGER NOT NULL,
            status      TEXT NOT NULL DEFAULT 'new',   -- new/learning/known
            correct     INTEGER NOT NULL DEFAULT 0,
            wrong       INTEGER NOT NULL DEFAULT 0,
            last_seen   TEXT,                           -- ISO datetime
            next_review TEXT,                           -- ISO date，艾宾浩斯下次复习日
            streak      INTEGER NOT NULL DEFAULT 0,     -- 连续答对次数
            PRIMARY KEY (username, word_id)
        );

        CREATE TABLE IF NOT EXISTS study_logs (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            username    TEXT NOT NULL,
            log_date    TEXT NOT NULL,                  -- YYYY-MM-DD
            words_new   INTEGER DEFAULT 0,
            words_reviewed INTEGER DEFAULT 0,
            correct_rate REAL DEFAULT 0.0,
            minutes     INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS fill_records (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            username    TEXT NOT NULL,
            word_id     INTEGER NOT NULL,
            mode        TEXT NOT NULL,                  -- fill/translate/spell
            result      INTEGER NOT NULL,               -- 1=correct 0=wrong
            created_at  TEXT NOT NULL
        );
        """)


# ── 词库 ─────────────────────────────────────────────────────────────────

def load_words() -> list[dict]:
    """从JSON加载完整词库"""
    with open(WORDS_PATH, encoding="utf-8") as f:
        data = json.load(f)
    return data["words"]


def get_word_by_id(word_id: int) -> dict | None:
    words = load_words()
    for w in words:
        if w["id"] == word_id:
            return w
    return None


# ── 用户 ─────────────────────────────────────────────────────────────────

def get_or_create_user(username: str, display_name: str = "") -> dict:
    """获取或创建用户，返回用户行 dict"""
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE username=?", (username,)
        ).fetchone()
        if row:
            return dict(row)
        name = display_name or username
        today = date.today().isoformat()
        conn.execute(
            "INSERT INTO users VALUES (?,?,?,?)",
            (username, name, datetime.now().isoformat(), today),
        )
        return {"username": username, "display_name": name,
                "created_at": datetime.now().isoformat(), "start_date": today}


def list_users() -> list[dict]:
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM users ORDER BY created_at").fetchall()
        return [dict(r) for r in rows]


# ── 学习进度 ──────────────────────────────────────────────────────────────

# 艾宾浩斯复习间隔（天），按streak索引
EBBINGHAUS = [1, 2, 4, 7, 15, 30, 60]


def _next_review_date(streak: int) -> str:
    idx = min(streak, len(EBBINGHAUS) - 1)
    delta = EBBINGHAUS[idx]
    return (date.today() + timedelta(days=delta)).isoformat()


def get_progress(username: str, word_id: int) -> dict | None:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM word_progress WHERE username=? AND word_id=?",
            (username, word_id),
        ).fetchone()
        return dict(row) if row else None


def upsert_progress(username: str, word_id: int, correct: bool):
    """更新单词掌握进度，返回新状态"""
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM word_progress WHERE username=? AND word_id=?",
            (username, word_id),
        ).fetchone()

        now = datetime.now().isoformat()
        if row is None:
            streak = 1 if correct else 0
            status = "learning"
            c, w = (1, 0) if correct else (0, 1)
            conn.execute(
                """INSERT INTO word_progress
                   (username,word_id,status,correct,wrong,last_seen,next_review,streak)
                   VALUES (?,?,?,?,?,?,?,?)""",
                (username, word_id, status, c, w, now,
                 _next_review_date(streak), streak),
            )
        else:
            streak = (row["streak"] + 1) if correct else 0
            c = row["correct"] + (1 if correct else 0)
            w = row["wrong"] + (0 if correct else 1)
            # 连续答对5次→known；答错→learning
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
                (status, c, w, now, _next_review_date(streak),
                 streak, username, word_id),
            )
        return {"streak": streak, "correct": correct}


def get_all_progress(username: str) -> dict[int, dict]:
    """返回 {word_id: progress_row}"""
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM word_progress WHERE username=?", (username,)
        ).fetchall()
        return {r["word_id"]: dict(r) for r in rows}


def get_today_review_ids(username: str) -> list[int]:
    """返回今天需要复习的word_id列表（next_review <= today）"""
    today = date.today().isoformat()
    with get_conn() as conn:
        rows = conn.execute(
            """SELECT word_id FROM word_progress
               WHERE username=? AND next_review<=? AND status!='new'
               ORDER BY next_review""",
            (username, today),
        ).fetchall()
        return [r["word_id"] for r in rows]


def get_stats(username: str) -> dict:
    """汇总统计"""
    progress = get_all_progress(username)
    words = load_words()
    total = len(words)
    new_cnt = total - len(progress)
    learning = sum(1 for p in progress.values() if p["status"] == "learning")
    known = sum(1 for p in progress.values() if p["status"] == "known")
    total_correct = sum(p["correct"] for p in progress.values())
    total_wrong = sum(p["wrong"] for p in progress.values())
    accuracy = (
        total_correct / (total_correct + total_wrong)
        if (total_correct + total_wrong) > 0 else 0.0
    )
    review_due = len(get_today_review_ids(username))

    # 备考天数
    with get_conn() as conn:
        user = conn.execute(
            "SELECT start_date FROM users WHERE username=?", (username,)
        ).fetchone()
    start = date.fromisoformat(user["start_date"]) if user else date.today()
    days_elapsed = (date.today() - start).days + 1
    days_left = max(0, 120 - days_elapsed)

    return {
        "total": total, "new": new_cnt, "learning": learning, "known": known,
        "accuracy": accuracy, "review_due": review_due,
        "days_elapsed": days_elapsed, "days_left": days_left,
    }


# ── 练习记录 ──────────────────────────────────────────────────────────────

def log_fill(username: str, word_id: int, mode: str, result: bool):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO fill_records (username,word_id,mode,result,created_at) VALUES (?,?,?,?,?)",
            (username, word_id, mode, int(result), datetime.now().isoformat()),
        )


def get_weak_words(username: str, limit: int = 10) -> list[dict]:
    """返回错误率最高的单词"""
    with get_conn() as conn:
        rows = conn.execute(
            """SELECT word_id,
                      wrong * 1.0 / (correct + wrong + 0.001) AS err_rate,
                      correct, wrong
               FROM word_progress
               WHERE username=? AND wrong>0
               ORDER BY err_rate DESC LIMIT ?""",
            (username, limit),
        ).fetchall()
    result = []
    for r in rows:
        w = get_word_by_id(r["word_id"])
        if w:
            result.append({**w, "err_rate": r["err_rate"],
                           "correct": r["correct"], "wrong": r["wrong"]})
    return result
