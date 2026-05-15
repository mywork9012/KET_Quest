"""
KET 专属背词软件 v2.0
新增：Web Speech API 点读 / XP+连击游戏化 / 徽章系统 / 强化选择题
运行: streamlit run app.py
"""

import streamlit as st
import random
import re
from datetime import date

st.set_page_config(
    page_title="KET 冲刺背词",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils.db import (
    init_db, get_or_create_user, list_users, load_words,
    get_all_progress, get_today_review_ids, upsert_progress,
    get_stats, log_fill, get_weak_words, get_word_by_id,
    get_game_profile, get_level_info, award_xp,
    check_and_award_badges, get_earned_badges, BADGE_DEFS, LEVEL_XP,
    arcade_upsert, get_arcade_pool,
)
from utils.planner import get_today_plan, STAGES
from utils.tts import tts_button, tts_button_small, auto_play

init_db()

# ── CSS ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');
html, body, [class*="css"] { font-family: 'Nunito', 'PingFang SC', sans-serif; }
.stApp { background: linear-gradient(135deg,#667eea15,#764ba215); }

.word-card {
  background:white; border-radius:20px; padding:24px 28px;
  box-shadow:0 8px 32px rgba(102,126,234,0.13);
  border-left:6px solid #667eea; margin-bottom:14px;
}
.word-main { font-size:2.6rem; font-weight:900; color:#2d3748; letter-spacing:-1px; }
.word-phonetic { font-size:1.05rem; color:#7c8db0; margin:4px 0 6px; }
.word-part {
  display:inline-block; background:#667eea; color:white;
  border-radius:8px; padding:2px 10px; font-size:0.82rem; font-weight:700; margin-right:6px;
}
.word-meaning { font-size:1.35rem; font-weight:700; color:#4a5568; margin-top:6px; }

.sentence-card {
  background:linear-gradient(135deg,#f8f9ff,#eef2ff);
  border-radius:14px; padding:16px 20px; margin:8px 0;
  border:1px solid #e2e8f0;
}
.sentence-en { font-size:1.1rem; font-weight:600; color:#2d3748; line-height:1.9; }
.sentence-cn { font-size:0.92rem; color:#718096; margin-top:4px; }
.highlight { color:#667eea; font-weight:900;
  text-decoration:underline; text-decoration-color:#667eea88; }

/* 游戏化HUD */
.xp-bar-wrap {
  background:#e2e8f0; border-radius:20px; height:14px;
  overflow:hidden; margin:6px 0;
}
.xp-bar-fill {
  height:100%; border-radius:20px;
  background:linear-gradient(90deg,#667eea,#764ba2);
  transition:width 0.5s ease;
}
.combo-badge {
  display:inline-block;
  background:linear-gradient(135deg,#f6d365,#fda085);
  color:white; border-radius:20px; padding:4px 16px;
  font-size:1rem; font-weight:900;
  box-shadow:0 4px 12px rgba(253,160,133,0.4);
  animation: pulse 0.6s ease;
}
@keyframes pulse {
  0%{transform:scale(1)} 50%{transform:scale(1.15)} 100%{transform:scale(1)}
}
.badge-card {
  background:white; border-radius:14px; padding:14px;
  text-align:center; box-shadow:0 4px 16px rgba(0,0,0,0.07);
  border-top:3px solid #667eea;
}
.badge-icon { font-size:2rem; }
.badge-name { font-weight:800; font-size:0.9rem; color:#2d3748; margin-top:4px; }
.badge-desc { font-size:0.75rem; color:#a0aec0; margin-top:2px; }
.badge-locked { opacity:0.3; filter:grayscale(1); }

.stat-box {
  background:white; border-radius:16px; padding:18px;
  text-align:center; box-shadow:0 4px 14px rgba(0,0,0,0.07);
}
.stat-number { font-size:2rem; font-weight:900; color:#667eea; }
.stat-label  { font-size:0.82rem; color:#718096; margin-top:3px; }

.correct-banner {
  background:linear-gradient(135deg,#48bb78,#38a169);
  color:white; border-radius:14px; padding:14px;
  text-align:center; font-size:1.15rem; font-weight:800; margin:10px 0;
}
.wrong-banner {
  background:linear-gradient(135deg,#fc8181,#e53e3e);
  color:white; border-radius:14px; padding:14px;
  text-align:center; font-size:1.15rem; font-weight:800; margin:10px 0;
}
.xp-toast {
  background:linear-gradient(135deg,#667eea,#764ba2);
  color:white; border-radius:10px; padding:8px 18px;
  display:inline-block; font-weight:800; font-size:0.95rem;
  margin-top:6px;
}
.quiz-question {
  background:white; border-radius:18px; padding:26px;
  box-shadow:0 6px 24px rgba(0,0,0,0.08); text-align:center; margin-bottom:18px;
}
.quiz-cn { font-size:1.4rem; font-weight:700; color:#2d3748; }
.quiz-hint { font-size:0.88rem; color:#a0aec0; margin-top:6px; }

div[data-testid="stButton"] > button {
  border-radius:12px !important; font-weight:700 !important;
  font-family:'Nunito',sans-serif !important;
  transition:transform 0.15s ease !important;
}
div[data-testid="stButton"] > button:hover { transform:translateY(-2px) !important; }

.sidebar-header {
  background:linear-gradient(135deg,#667eea,#764ba2);
  color:white; border-radius:14px; padding:14px 16px;
  margin-bottom:10px; text-align:center;
}
.level-chip {
  background:linear-gradient(135deg,#f6d365,#fda085);
  color:white; border-radius:20px; padding:3px 12px;
  font-weight:800; font-size:0.85rem; display:inline-block;
}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════════════════════

def render_sentence_html(s: str) -> str:
    return re.sub(r'\*\*(.+?)\*\*', r'<span class="highlight">\1</span>', s)

def status_badge(status: str) -> str:
    m = {"new":"🆕 新词","learning":"📖 学习中","known":"✅ 已掌握"}
    return f'<span style="font-size:0.8rem;font-weight:700">{m.get(status,"")}</span>'

def render_word_card(word: dict, progress: dict = None, show_tts: bool = True):
    """渲染单词主卡片 + TTS按钮"""
    status = progress["status"] if progress else "new"
    topic_icon = {
        "character":"😊","school":"📚","daily_life":"🛒","travel":"✈️",
        "hobbies":"🎵","states":"💡","study_work":"✏️",
        "life_shopping":"🏠","travel_weather":"🌤️","hobbies_health":"❤️",
    }.get(word.get("topic_en",""),"📖")
    s1 = render_sentence_html(word.get("sentence1",""))
    s2 = render_sentence_html(word.get("sentence2",""))

    st.markdown(f"""
    <div class="word-card">
      <div style="display:flex;justify-content:space-between;align-items:flex-start">
        <div>
          <div class="word-main">{word['word']}</div>
          <div class="word-phonetic">{word.get('phonetic','')}</div>
          <span class="word-part">{word.get('part','')}</span>
          {status_badge(status)}
        </div>
        <div style="font-size:2rem">{topic_icon}</div>
      </div>
      <div class="word-meaning">{word.get('meaning','')}</div>
      <div style="font-size:0.78rem;color:#a0aec0;margin-top:4px">
        {word.get('topic','')} · {word.get('level','')}类词
      </div>
    </div>
    """, unsafe_allow_html=True)

    # TTS 按钮行：单词 + 慢速
    if show_tts:
        c1, c2, c3 = st.columns([1, 1, 2])
        with c1:
            tts_button(word["word"], "🔊 单词", rate=0.8, key=f"tts_w_{word['id']}")
        with c2:
            tts_button(word["word"], "🐢 慢读", rate=0.5, key=f"tts_ws_{word['id']}")

    # 例句
    if s1:
        st.markdown(f"""
        <div class="sentence-card">
          <div class="sentence-en">① {s1}</div>
          <div class="sentence-cn">🇨🇳 {word.get('sentence1_cn','')}</div>
        </div>""", unsafe_allow_html=True)
        if show_tts and word.get("sentence1"):
            tts_button_small(word["sentence1"], "🔊 听例句①")

    if s2:
        st.markdown(f"""
        <div class="sentence-card">
          <div class="sentence-en">② {s2}</div>
          <div class="sentence-cn">🇨🇳 {word.get('sentence2_cn','')}</div>
        </div>""", unsafe_allow_html=True)
        if show_tts and word.get("sentence2"):
            tts_button_small(word["sentence2"], "🔊 听例句②")


def render_hud(prof: dict):
    """顶部XP/等级/连击状态栏"""
    xp = prof["xp"]
    level, lv_start, lv_next = get_level_info(xp)
    xp_in_level = xp - lv_start
    xp_needed = lv_next - lv_start
    pct = min(xp_in_level / max(xp_needed, 1), 1.0)
    combo = st.session_state.get("combo", 0)

    combo_html = (f'<span class="combo-badge">🔥 {combo} 连击！</span>'
                  if combo >= 3 else "")
    multiplier = 1.0 + min(combo // 3, 4) * 0.5
    multi_html = (f'<span style="font-size:0.85rem;color:#fda085;font-weight:800">'
                  f'×{multiplier:.1f} 倍XP</span>' if combo >= 3 else "")

    st.markdown(f"""
    <div style="background:white;border-radius:14px;padding:12px 18px;
                box-shadow:0 4px 16px rgba(0,0,0,0.07);margin-bottom:12px;">
      <div style="display:flex;justify-content:space-between;align-items:center">
        <div>
          <span class="level-chip">⭐ Lv.{level}</span>
          &nbsp;
          <span style="font-weight:700;color:#2d3748">{prof.get('coins',0)} 🪙</span>
          &nbsp; {combo_html} {multi_html}
        </div>
        <div style="font-size:0.85rem;color:#718096">
          XP {xp} / {lv_next} &nbsp;·&nbsp;
          🔥 打卡 {prof.get('daily_streak',0)} 天
        </div>
      </div>
      <div class="xp-bar-wrap" style="margin-top:8px">
        <div class="xp-bar-fill" style="width:{pct*100:.1f}%"></div>
      </div>
    </div>
    """, unsafe_allow_html=True)


def sample_distractors(current: dict, pool: list[dict], all_words: list, count: int = 3) -> list[dict]:
    """从候选词池中抽取干扰项。如果候选数量不足则回退到所有词池。"""
    candidates = [x for x in pool if x["id"] != current["id"]]
    if len(candidates) < count:
        fallback = [x for x in all_words if x["id"] != current["id"]]
        if len(fallback) >= count:
            candidates = fallback
    return random.sample(candidates, count) if len(candidates) >= count else candidates


def handle_answer(username: str, word_id: int, correct: bool, mode: str = "quiz"):
    """统一答题处理：更新进度、XP、连击、徽章，返回结算dict"""
    # 更新连击
    if correct:
        st.session_state.combo = st.session_state.get("combo", 0) + 1
    else:
        st.session_state.combo = 0

    combo = st.session_state.combo
    upsert_progress(username, word_id, correct)
    log_fill(username, word_id, mode, correct)
    result = award_xp(username, correct, combo)
    new_badges = check_and_award_badges(username, combo)
    result["new_badges"] = new_badges
    result["combo"] = combo
    return result


def show_result_banner(result: dict, correct_word: str = ""):
    """显示答题结果横幅 + XP提示 + 徽章弹出"""
    if result["correct"] if "correct" in result else False:
        pass  # 由调用方判断
    xp = result.get("xp_gained", 0)
    combo = result.get("combo", 0)
    multi = result.get("multiplier", 1.0)
    coins = result.get("coins_gained", 0)

    xp_parts = [f"+{xp} XP"]
    if multi > 1.0:
        xp_parts.append(f"(×{multi:.1f}连击倍率)")
    if coins:
        xp_parts.append(f"+{coins}🪙")
    st.markdown(f'<div class="xp-toast">{" ".join(xp_parts)}</div>',
                unsafe_allow_html=True)

    if result.get("leveled_up"):
        st.balloons()
        st.success(f"🎉 升级了！现在是 Lv.{result['level']} ！")

    for bid in result.get("new_badges", []):
        if bid in BADGE_DEFS:
            name, icon, desc = BADGE_DEFS[bid]
            st.toast(f"{icon} 获得徽章【{name}】：{desc}", icon="🏅")


# ── session_state 初始化 ──────────────────────────────────────────────────
def _ss(k, v):
    if k not in st.session_state:
        st.session_state[k] = v

_ss("username", None); _ss("page", "home")
_ss("study_idx", 0);   _ss("study_words", [])
_ss("combo", 0)
_ss("quiz_word", None); _ss("quiz_choices", []); _ss("quiz_answered", False); _ss("quiz_result", None)
_ss("fill_word", None); _ss("fill_answered", False); _ss("fill_result", None)
_ss("review_ids", []); _ss("review_idx", 0); _ss("review_phase", "show")
_ss("arcade_score", 0); _ss("arcade_lives", 3); _ss("arcade_word", None)
_ss("arcade_choices", []); _ss("arcade_answered", False); _ss("arcade_result", None)
_ss("perfect_streak", 0)   # 用于 perfect_quiz 徽章
_ss("topic_page", "topic_home")
_ss("topic_sel", None)
_ss("topic_practice_scope", "全部词")
_ss("topic_quiz_active", False)
_ss("topic_quiz_topic", "全部")
_ss("topic_quiz_scope", "全部词")
_ss("topic_quiz_word", None)
_ss("topic_quiz_choices", [])
_ss("topic_quiz_answered", False)
_ss("topic_quiz_result", None)


# ═══════════════════════════════════════════════════════
# 侧边栏
# ═══════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
      <div style="font-size:1.6rem">🎯</div>
      <div style="font-size:1.15rem;font-weight:800">KET 冲刺背词</div>
      <div style="font-size:0.78rem;opacity:0.85">四年级 · 4个月闭环备考</div>
    </div>
    """, unsafe_allow_html=True)

    users = list_users()
    with st.expander("👤 切换用户", expanded=(st.session_state.username is None)):
        c1, c2 = st.columns([2, 1])
        new_name = c1.text_input("用户名", placeholder="输入名字",
                                 label_visibility="collapsed")
        if c2.button("进入", use_container_width=True) and new_name.strip():
            uname = new_name.strip()
            get_or_create_user(uname, uname)
            st.session_state.username = uname
            st.session_state.page = "home"
            st.session_state.combo = 0
            st.rerun()
        for u in users:
            if st.button(f"👤 {u['display_name']}", key=f"u_{u['username']}",
                         use_container_width=True):
                st.session_state.username = u["username"]
                st.session_state.page = "home"
                st.session_state.combo = 0
                st.rerun()

    if st.session_state.username:
        uname = st.session_state.username
        prof = get_game_profile(uname)
        level, lv_start, lv_next = get_level_info(prof["xp"])
        st.markdown(f"""
        <div style="text-align:center;margin:8px 0">
          <span class="level-chip">⭐ Lv.{level}</span>
          <span style="margin-left:8px;font-weight:700">{uname}</span>
        </div>
        """, unsafe_allow_html=True)

        st.divider()
        nav_items = [
            ("🏠","今日计划","home"),
            ("📖","学新词","learn"),
            ("🔄","复习单词","review"),
            ("🧩","选择题练习","quiz"),
            ("✏️","填空练习","fill"),
            ("🕹️","闯关游戏","arcade"),
            ("📚","分主题练习","topics"),
            ("📊","我的进度","stats"),
            ("🏅","我的徽章","badges"),
            ("📋","词库浏览","wordlist"),
        ]
        for icon, label, pg in nav_items:
            active = "◀" if st.session_state.page == pg else ""
            if st.button(f"{icon} {label} {active}", key=f"nav_{pg}",
                         use_container_width=True):
                st.session_state.page = pg
                st.session_state.study_idx = 0
                st.session_state.quiz_answered = False
                st.session_state.fill_answered = False
                st.session_state.review_phase = "show"
                st.rerun()

        st.divider()
        stats = get_stats(uname)
        c1, c2 = st.columns(2)
        c1.metric("✅ 已掌握", stats["known"])
        c2.metric("🔥 打卡", f"{prof['daily_streak']}天")
        c1.metric("🪙 金币", prof["coins"])
        c2.metric("⚡ 连击", st.session_state.combo)


# ═══════════════════════════════════════════════════════
# 未登录
# ═══════════════════════════════════════════════════════

if not st.session_state.username:
    st.markdown("""
    <div style="text-align:center;padding:60px 20px">
      <div style="font-size:4rem">🎯</div>
      <h1 style="font-size:2.4rem;font-weight:900;color:#667eea">KET 冲刺背词</h1>
      <p style="font-size:1.1rem;color:#718096">四年级 · 已过剑桥三级 · 4个月闭环冲刺 KET</p>
      <p style="color:#a0aec0">← 在左侧输入名字开始学习</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

uname = st.session_state.username
user = get_or_create_user(uname)
page = st.session_state.page
all_words = load_words()
all_progress = get_all_progress(uname)
stats = get_stats(uname)
prof = get_game_profile(uname)


# ═══════════════════════════════════════════════════════
# 页面：今日计划
# ═══════════════════════════════════════════════════════

if page == "home":
    plan = get_today_plan(uname, user["start_date"])
    stage = plan["stage"]
    render_hud(prof)

    st.markdown(f"""
    <h2 style="color:#2d3748;font-weight:800;margin-bottom:2px">
      📅 今日计划 · 第 {plan['day']} 天
    </h2>
    <p style="color:#718096">备考倒计时 <b>{plan['days_left']}</b> 天 &nbsp;·&nbsp;
    <span style="color:{stage['color']};font-weight:700">{stage['name']} · {stage['label']}</span>
    &nbsp;·&nbsp; 还剩 <b>{plan['unseen_total']}</b> 个词未学</p>
    """, unsafe_allow_html=True)

    # 词库总进度（已接触 / 总词数）
    touched = stats["total"] - stats["new"]
    st.progress(
        min(touched / stats["total"], 1.0),
        text=f"词库进度 {touched}/{stats['total']}（已接触单词数）"
    )
    st.info(plan["tips"])

    # 4个数据卡片
    c1, c2, c3, c4 = st.columns(4)
    for col, num, label in [
        (c1, plan["new_count"] if not plan["all_done"] else "🎊", "今日推荐新词"),
        (c2, stats["review_due"], "待复习"),
        (c3, stats["known"], "已掌握"),
        (c4, f"{stats['accuracy']:.0%}", "正确率"),
    ]:
        with col:
            st.markdown(f"""
            <div class="stat-box">
              <div class="stat-number">{num}</div>
              <div class="stat-label">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")

    if plan["all_done"]:
        st.success("🎊 198个单词全部学过了！保持每天复习，冲刺KET！")
    else:
        st.markdown(f"### 📚 今日推荐新词（{plan['new_count']} 个）")
        cols = st.columns(4)
        for i, w in enumerate(plan["new_words"]):
            prog = all_progress.get(w["id"])
            status = prog["status"] if prog else "new"
            icon = {"known":"✅","learning":"📖","new":"🆕"}.get(status,"🆕")
            with cols[i % 4]:
                st.markdown(f"""
                <div style="background:white;border-radius:12px;padding:12px;
                            box-shadow:0 3px 10px rgba(0,0,0,0.07);margin-bottom:8px;
                            border-top:3px solid #667eea">
                  <div style="font-size:1.05rem;font-weight:800;color:#2d3748">{w['word']}</div>
                  <div style="font-size:0.78rem;color:#718096">{w['phonetic']}</div>
                  <div style="font-size:0.88rem;color:#4a5568;font-weight:600;margin-top:3px">{w['meaning']}</div>
                  <div style="font-size:0.75rem;margin-top:4px">{icon}</div>
                </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🗺️ 备考路线图")
    scols = st.columns(4)
    day = plan["day"]
    for i, s in enumerate(STAGES):
        lo, hi = s["days"]
        is_current = lo <= day <= hi
        is_done = day > hi
        icon = "✅" if is_done else ("🔥" if is_current else "⏳")
        border = "3px solid #667eea" if is_current else "2px solid #e2e8f0"
        with scols[i]:
            st.markdown(f"""
            <div style="background:white;border-radius:14px;padding:14px;
                        border:{border};text-align:center;
                        opacity:{'1' if (is_current or is_done) else '0.5'}">
              <div style="font-size:1.4rem">{icon}</div>
              <div style="font-weight:800;color:#2d3748;font-size:0.88rem">{s['name']}</div>
              <div style="font-size:0.72rem;color:#718096">Day {lo}–{hi}</div>
              <div style="font-size:0.8rem;font-weight:700;color:#667eea;margin-top:3px">{s['label']}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    b1, b2, b3, b4 = st.columns(4)
    if b1.button("📖 学新词", use_container_width=True, type="primary"):
        st.session_state.page = "learn"
        # 每次进入学新词页面，重新从未学词中取，不依赖旧session
        st.session_state.study_words = []
        st.session_state.study_idx = 0
        st.rerun()
    if b2.button("🔄 复习单词", use_container_width=True):
        st.session_state.page = "review"
        st.rerun()
    if b3.button("🧩 选择题", use_container_width=True):
        st.session_state.page = "quiz"
        st.rerun()
    if b4.button("🕹️ 闯关游戏", use_container_width=True):
        st.session_state.page = "arcade"
        st.rerun()


# ═══════════════════════════════════════════════════════
# 页面：学新词
# ═══════════════════════════════════════════════════════

elif page == "learn":
    # ── 核心修复：每次进入页面都从数据库重新取未学词 ──────────────────
    # 不依赖 session_state 缓存，确保学完一批后继续加载新词
    plan = get_today_plan(uname, user["start_date"])

    # study_words 为空或已全部标记过（都在 progress 里）→ 重新取
    if not st.session_state.study_words:
        if plan["all_done"]:
            st.success("🎊 恭喜！198个单词已全部学过！请继续保持每日复习。")
            if st.button("去复习单词 →", type="primary"):
                st.session_state.page = "review"
                st.rerun()
            st.stop()
        st.session_state.study_words = plan["new_words"]
        st.session_state.study_idx = 0

    words_to_study = st.session_state.study_words
    idx = st.session_state.study_idx
    total = len(words_to_study)

    render_hud(prof)

    # 顶部信息栏：当前批次进度 + 总剩余
    st.markdown(
        f"### 📖 学新词 &nbsp;"
        f"<span style='color:#a0aec0;font-size:1rem'>"
        f"本批 {min(idx+1,total)}/{total} &nbsp;·&nbsp; "
        f"还剩 {plan['unseen_total']} 词未学</span>",
        unsafe_allow_html=True
    )
    st.progress((idx + 1) / total)

    word = words_to_study[idx]
    # 每次翻到新词刷新进度（因为上一批学了之后 all_progress 变了）
    current_progress = get_all_progress(uname)
    prog = current_progress.get(word["id"])

    auto_play(word["word"], rate=0.8)
    render_word_card(word, prog, show_tts=True)

    # ── 掌握进度提示（让孩子知道需要连续答对5次才算掌握）──────────
    streak  = prog["streak"]  if prog else 0
    correct = prog["correct"] if prog else 0
    status  = prog["status"]  if prog else "new"
    bar_pct = min(streak / 5, 1.0)
    bar_color = "#48bb78" if status == "known" else "#667eea"
    status_label = {
        "new":      "🆕 还没学过",
        "learning": f"📖 已答对 {streak}/5 次（连续答对5次即掌握✅）",
        "known":    "✅ 已掌握！",
    }.get(status, "")
    st.markdown(f"""
    <div style="margin:10px 0 4px">
      <div style="display:flex;justify-content:space-between;
                  font-size:0.82rem;color:#718096;margin-bottom:4px">
        <span>{status_label}</span>
        <span>累计答对 {correct} 次</span>
      </div>
      <div style="background:#e2e8f0;border-radius:20px;height:8px;overflow:hidden">
        <div style="width:{bar_pct*100:.0f}%;height:100%;
                    background:{bar_color};border-radius:20px;
                    transition:width 0.4s ease"></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    c1, c2, c3, c4 = st.columns(4)

    if c1.button("⬅️ 上一个", use_container_width=True, disabled=(idx == 0)):
        st.session_state.study_idx -= 1
        st.rerun()

    if c2.button("✅ 已会了", use_container_width=True, type="primary"):
        r = handle_answer(uname, word["id"], True, "learn")
        show_result_banner({**r, "correct": True})
        if idx < total - 1:
            st.session_state.study_idx += 1
        st.rerun()

    if c3.button("🔄 再看看", use_container_width=True):
        handle_answer(uname, word["id"], False, "learn")
        if idx < total - 1:
            st.session_state.study_idx += 1
        st.rerun()

    if c4.button("➡️ 下一个", use_container_width=True, disabled=(idx >= total - 1)):
        st.session_state.study_idx += 1
        st.rerun()

    # ── 本批学完后的选项 ──────────────────────────────────────────────
    if idx >= total - 1:
        st.success(f"🎉 本批 {total} 个词学完了！")

        # 重新查剩余未学词
        fresh_plan = get_today_plan(uname, user["start_date"])
        remaining = fresh_plan["unseen_total"]

        if remaining > 0:
            st.info(f"📚 词库还有 **{remaining}** 个词等你学，继续吗？")
            ca, cb, cc = st.columns(3)
            if ca.button("📖 继续学下一批", use_container_width=True, type="primary"):
                # 清空 study_words，下次进入自动取新的一批
                st.session_state.study_words = []
                st.session_state.study_idx = 0
                st.rerun()
            if cb.button("🧩 先做选择题巩固", use_container_width=True):
                st.session_state.page = "quiz"
                st.rerun()
            if cc.button("🔄 去复习", use_container_width=True):
                st.session_state.page = "review"
                st.rerun()
        else:
            st.success("🎊 太厉害了！198个单词全部学过！")
            if st.button("🔄 去复习巩固 →", type="primary"):
                st.session_state.page = "review"
                st.rerun()


# ═══════════════════════════════════════════════════════
# 页面：复习单词（翻转卡片式）
# ═══════════════════════════════════════════════════════

elif page == "review":
    review_ids = get_today_review_ids(uname)
    if not review_ids:
        st.success("🎊 今天没有待复习单词，保持这个节奏！")
        learned = [w for w in all_words if w["id"] in all_progress]
        if learned:
            random.shuffle(learned)
            st.markdown("### 📋 随机温习 10 个")
            for w in learned[:10]:
                prog = all_progress.get(w["id"])
                with st.expander(f"**{w['word']}** — {w['meaning']}"):
                    render_word_card(w, prog)
        st.stop()

    if (not st.session_state.review_ids or
            set(st.session_state.review_ids) != set(review_ids)):
        st.session_state.review_ids = review_ids
        st.session_state.review_idx = 0
        st.session_state.review_phase = "show"

    idx = st.session_state.review_idx
    total = len(review_ids)
    render_hud(prof)

    st.markdown(f"### 🔄 复习单词 &nbsp;<span style='color:#a0aec0;font-size:1rem'>{min(idx+1,total)} / {total}</span>",
                unsafe_allow_html=True)
    st.progress(min((idx + 1) / total, 1.0))

    if idx >= total:
        st.success(f"🎉 本轮 {total} 个单词复习完成！")
        if st.button("再来一轮", type="primary"):
            st.session_state.review_idx = 0
            st.session_state.review_phase = "show"
            st.rerun()
        st.stop()

    word_id = review_ids[idx]
    word = get_word_by_id(word_id)
    if not word:
        st.session_state.review_idx += 1
        st.rerun()

    prog = all_progress.get(word["id"])
    phase = st.session_state.review_phase

    if phase == "show":
        # 先只显示单词，让孩子自己想
        st.markdown(f"""
        <div class="word-card" style="text-align:center;padding:40px">
          <div class="word-main">{word['word']}</div>
          <div class="word-phonetic">{word.get('phonetic','')}</div>
          <div style="color:#a0aec0;margin-top:16px;font-size:1rem">想一想这个词的意思…</div>
        </div>
        """, unsafe_allow_html=True)

        auto_play(word["word"], rate=0.8)

        c1, c2 = st.columns(2)
        with c1:
            tts_button(word["word"], "🔊 听发音", rate=0.8, key=f"rev_tts_{word_id}")
        with c2:
            tts_button(word["word"], "🐢 慢速", rate=0.5, key=f"rev_slow_{word_id}")

        if st.button("👀 看答案", use_container_width=True, type="primary"):
            st.session_state.review_phase = "answer"
            st.rerun()

    else:  # answer phase
        render_word_card(word, prog, show_tts=True)
        st.markdown("---")
        st.markdown("**你记得这个词吗？**")
        c1, c2, c3 = st.columns(3)
        if c1.button("✅ 完全记得！", use_container_width=True, type="primary"):
            r = handle_answer(uname, word_id, True, "review")
            show_result_banner({**r, "correct": True})
            st.session_state.review_idx += 1
            st.session_state.review_phase = "show"
            st.rerun()
        if c2.button("😅 模糊", use_container_width=True):
            r = handle_answer(uname, word_id, False, "review")
            st.session_state.review_idx += 1
            st.session_state.review_phase = "show"
            st.rerun()
        if c3.button("❌ 不记得", use_container_width=True):
            r = handle_answer(uname, word_id, False, "review")
            st.session_state.review_idx += 1
            st.session_state.review_phase = "show"
            st.rerun()

        if prog:
            st.caption(f"连续答对 {prog['streak']} 次 · 正确 {prog['correct']} / 错误 {prog['wrong']}")


# ═══════════════════════════════════════════════════════
# 页面：选择题练习（强化版，含点读）
# ═══════════════════════════════════════════════════════

elif page == "quiz":
    render_hud(prof)
    st.markdown("### 🧩 选择题练习")

    # 题目类型选择
    quiz_type = st.radio(
        "题目类型",
        ["🇨🇳 看中文选英文", "🇬🇧 看英文选中文", "👂 听发音选单词", "📝 看例句选单词"],
        horizontal=True, label_visibility="collapsed"
    )

    pool = [w for w in all_words if w["id"] in all_progress] or all_words[:40]

    def _new_quiz_word():
        w = random.choice(pool)
        same_pos = [x for x in pool if x["part"] == w["part"] and x["id"] != w["id"]]
        distractors_pool = same_pos if len(same_pos) >= 3 else pool
        distractors = sample_distractors(w, distractors_pool, all_words, 3)
        choices = [w] + distractors
        random.shuffle(choices)
        st.session_state.quiz_word = w
        st.session_state.quiz_choices = choices
        st.session_state.quiz_answered = False
        st.session_state.quiz_result = None

    if not st.session_state.quiz_word:
        _new_quiz_word()

    word = st.session_state.quiz_word
    choices = st.session_state.quiz_choices
    answered = st.session_state.quiz_answered

    # ── 题目展示 ──
    if "听发音" in quiz_type:
        st.markdown("""
        <div class="quiz-question">
          <div class="quiz-cn">👂 听发音，选出你听到的单词</div>
          <div class="quiz-hint">点击下方按钮播放发音</div>
        </div>""", unsafe_allow_html=True)
        tts_button(word["word"], "🔊 播放发音", rate=0.8, key=f"quiz_tts_{word['id']}")

    elif "看例句" in quiz_type:
        sent = word.get("sentence1", "")
        sent_blank = re.sub(r'\*\*(.+?)\*\*', '______', sent)
        sent_cn = word.get("sentence1_cn", "")
        st.markdown(f"""
        <div class="quiz-question">
          <div class="quiz-cn">📝 {sent_cn}</div>
          <div class="sentence-en" style="margin-top:12px">{sent_blank}</div>
          <div class="quiz-hint">选出空白处的正确单词</div>
        </div>""", unsafe_allow_html=True)

    elif "看中文" in quiz_type:
        st.markdown(f"""
        <div class="quiz-question">
          <div class="quiz-cn">🇨🇳 {word['meaning']}</div>
          <div class="quiz-hint">{word['part']} · 选出对应的英文单词</div>
        </div>""", unsafe_allow_html=True)

    else:  # 看英文选中文
        st.markdown(f"""
        <div class="quiz-question">
          <div class="quiz-main" style="font-size:2rem;font-weight:900;color:#667eea">
            {word['word']}
          </div>
          <div style="color:#718096;font-size:1rem">{word.get('phonetic','')}</div>
          <div class="quiz-hint">选出这个单词的中文意思</div>
        </div>""", unsafe_allow_html=True)
        tts_button(word["word"], "🔊 听发音", rate=0.8, key=f"quiz_en_tts_{word['id']}")

    # ── 四个选项 ──
    if not answered:
        bcols = st.columns(2)
        for i, c in enumerate(choices):
            with bcols[i % 2]:
                if "看中文" in quiz_type or "听发音" in quiz_type or "看例句" in quiz_type:
                    label = f"**{c['word']}**  {c['phonetic']}"
                else:
                    label = f"**{c['meaning']}**"
                if st.button(label, key=f"qc_{c['id']}", use_container_width=True):
                    is_correct = (c["id"] == word["id"])
                    r = handle_answer(uname, word["id"], is_correct, "quiz")
                    st.session_state.quiz_result = (c["id"], is_correct, r)
                    st.session_state.quiz_answered = True
                    # 完美连击计数（用于 perfect_quiz 徽章）
                    if is_correct:
                        st.session_state.perfect_streak = st.session_state.get("perfect_streak",0) + 1
                        if st.session_state.perfect_streak >= 10:
                            check_and_award_badges(uname, combo=st.session_state.combo)
                    else:
                        st.session_state.perfect_streak = 0
                    st.rerun()
    else:
        chosen_id, is_correct, r = st.session_state.quiz_result
        if is_correct:
            st.markdown('<div class="correct-banner">✅ 回答正确！</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="wrong-banner">❌ 正确答案是 <b>{word["word"]}</b>（{word["meaning"]}）</div>',
                        unsafe_allow_html=True)

        show_result_banner({**r, "correct": is_correct})

        # 显示完整单词卡
        with st.expander("📖 查看详情", expanded=True):
            render_word_card(word, all_progress.get(word["id"]), show_tts=True)

        # 选项颜色标注
        bcols = st.columns(2)
        for i, c in enumerate(choices):
            with bcols[i % 2]:
                if c["id"] == word["id"]:
                    st.success(f"✅ {c['word']} — {c['meaning']}")
                elif c["id"] == chosen_id:
                    st.error(f"❌ {c['word']} — {c['meaning']}")
                else:
                    st.markdown(f"&nbsp;&nbsp;{c['word']} — {c['meaning']}")

        if st.button("➡️ 下一题", type="primary", use_container_width=True):
            _new_quiz_word()
            st.rerun()

    # 底部连击显示
    combo = st.session_state.combo
    if combo >= 3:
        st.markdown(f'<div style="text-align:center;margin-top:8px">'
                    f'<span class="combo-badge">🔥 {combo} 连击！</span></div>',
                    unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# 页面：填空练习
# ═══════════════════════════════════════════════════════

elif page == "fill":
    render_hud(prof)
    st.markdown("### ✏️ 填空练习")
    st.caption("看中文提示和例句，写出缺失的英文单词")

    pool = [w for w in all_words if w.get("sentence1") and w["id"] in all_progress]
    if len(pool) < 4:
        pool = [w for w in all_words if w.get("sentence1")][:30]

    # ── 修复：只在 fill_word 为 None 时才重新出题 ──────────────
    # 旧逻辑 "or fill_answered" 导致答题后立刻清空，反馈界面永不显示
    if st.session_state.fill_word is None:
        w = random.choice(pool)
        st.session_state.fill_word = w
        # 固定选句存入 state，避免每次 rerun 随机结果不同
        if w.get("sentence2") and random.random() > 0.5:
            st.session_state.fill_sent    = w["sentence2"]
            st.session_state.fill_sent_cn = w["sentence2_cn"]
        else:
            st.session_state.fill_sent    = w["sentence1"]
            st.session_state.fill_sent_cn = w["sentence1_cn"]
        st.session_state.fill_answered = False
        st.session_state.fill_result   = None

    word     = st.session_state.fill_word
    answered = st.session_state.fill_answered
    # 读取固定的例句（不再随机）
    sent    = st.session_state.get("fill_sent",    word.get("sentence1", ""))
    sent_cn = st.session_state.get("fill_sent_cn", word.get("sentence1_cn", ""))

    blank_sent = re.sub(r'\*\*(.+?)\*\*', '______', sent)
    match = re.search(r'\*\*(.+?)\*\*', sent)
    correct_word = match.group(1) if match else word["word"]

    st.markdown(f"""
    <div class="quiz-question">
      <div class="quiz-cn">🇨🇳 {sent_cn}</div>
      <div class="sentence-en" style="margin-top:12px">📝 {blank_sent}</div>
      <div class="quiz-hint">提示：{word['part']} · {word['meaning']}</div>
    </div>""", unsafe_allow_html=True)

    if not answered:
        user_input = st.text_input("输入单词", placeholder="请输入…",
                                   label_visibility="collapsed", key="fill_input_box")
        c1, c2 = st.columns([1, 3])
        if c1.button("✅ 提交", type="primary", use_container_width=True):
            is_correct = user_input.lower().strip() == correct_word.lower().strip()
            r = handle_answer(uname, word["id"], is_correct, "fill")
            st.session_state.fill_result = (is_correct, r)
            st.session_state.fill_answered = True
            st.rerun()
        # 首字母提示
        if c2.button("💡 首字母提示", use_container_width=True):
            st.info(f"首字母是：**{correct_word[0].upper()}**，共 {len(correct_word)} 个字母")
    else:
        is_correct, r = st.session_state.fill_result
        if is_correct:
            st.markdown('<div class="correct-banner">✅ 正确！</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="wrong-banner">❌ 正确答案是 <b>{correct_word}</b></div>',
                        unsafe_allow_html=True)
        show_result_banner({**r, "correct": is_correct})

        # 展示完整例句 + 朗读
        full_sent_html = render_sentence_html(sent)
        st.markdown(f"""
        <div class="sentence-card">
          <div class="sentence-en">{full_sent_html}</div>
          <div class="sentence-cn">🇨🇳 {sent_cn}</div>
        </div>""", unsafe_allow_html=True)
        tts_button(re.sub(r'\*\*(.+?)\*\*', r'\1', sent),
                   "🔊 听完整例句", rate=0.8, key=f"fill_tts_{word['id']}")

        if st.button("➡️ 下一题", type="primary", use_container_width=True):
            # 置 None 即触发顶部重新出题逻辑
            st.session_state.fill_word    = None
            st.session_state.fill_sent    = None
            st.session_state.fill_sent_cn = None
            st.session_state.fill_answered = False
            st.rerun()


# ═══════════════════════════════════════════════════════
# 页面：闯关游戏 🕹️（3条命，连击得分）
# ═══════════════════════════════════════════════════════

elif page == "arcade":
    render_hud(prof)
    st.markdown("### 🕹️ 闯关游戏")
    st.caption("3条命，答错扣一条命，挑战最高分！")

    lives = st.session_state.arcade_lives
    score = st.session_state.arcade_score
    combo = st.session_state.combo

    # 生命值显示
    hearts = "❤️" * lives + "🖤" * (3 - lives)
    st.markdown(f"""
    <div style="background:white;border-radius:14px;padding:14px 20px;
                box-shadow:0 4px 14px rgba(0,0,0,0.08);margin-bottom:14px;
                display:flex;justify-content:space-between;align-items:center">
      <div style="font-size:1.5rem">{hearts}</div>
      <div style="font-size:1.4rem;font-weight:900;color:#667eea">得分 {score}</div>
      <div>
        {"" if combo < 3 else f'<span class="combo-badge">🔥 {combo} 连击</span>'}
      </div>
    </div>
    """, unsafe_allow_html=True)

    # 游戏结束
    if lives <= 0:
        st.markdown(f"""
        <div style="text-align:center;padding:40px">
          <div style="font-size:3rem">💀</div>
          <div style="font-size:2rem;font-weight:900;color:#e53e3e">游戏结束！</div>
          <div style="font-size:1.5rem;font-weight:700;color:#667eea;margin-top:8px">
            最终得分：{score} 分
          </div>
        </div>
        """, unsafe_allow_html=True)
        if score > prof.get("max_combo", 0):
            st.balloons()
            st.success("🏆 新纪录！")
        if st.button("🔄 再玩一次", type="primary", use_container_width=True):
            st.session_state.arcade_lives = 3
            st.session_state.arcade_score = 0
            st.session_state.combo = 0
            st.session_state.arcade_word = None
            st.session_state.arcade_answered = False
            st.rerun()
        st.stop()

    # 出题：只在 arcade_word 为 None 时出新题，避免答题后反馈被清空
    # get_arcade_pool 会自动排除已掌握(known)的词，3次答对即掌握
    pool = get_arcade_pool(uname, [w for w in all_words if w["id"] in all_progress] or all_words[:40])
    if not pool:
        pool = all_words[:40]
    if st.session_state.arcade_word is None:
        w = random.choice(pool)
        same_pos = [x for x in pool if x["part"] == w["part"] and x["id"] != w["id"]]
        dist_pool = same_pos if len(same_pos) >= 3 else pool
        distractors = sample_distractors(w, dist_pool, all_words, 3)
        choices = [w] + distractors
        random.shuffle(choices)
        st.session_state.arcade_word     = w
        st.session_state.arcade_choices  = choices
        st.session_state.arcade_answered = False
        st.session_state.arcade_result   = None

    word = st.session_state.arcade_word
    choices = st.session_state.arcade_choices
    answered = st.session_state.arcade_answered

    # 题型由 word_id 奇偶决定，保证同一道题前后一致
    mode = "cn2en" if word["id"] % 2 == 0 else "en2cn"

    if mode == "cn2en":
        st.markdown(f"""
        <div class="quiz-question">
          <div class="quiz-cn">🇨🇳 {word['meaning']}</div>
          <div class="quiz-hint">{word['part']} · 选出对应英文单词</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="quiz-question">
          <div style="font-size:2.2rem;font-weight:900;color:#667eea">{word['word']}</div>
          <div style="color:#718096">{word.get('phonetic','')}</div>
          <div class="quiz-hint">选出这个单词的中文意思</div>
        </div>""", unsafe_allow_html=True)
        tts_button(word["word"], "🔊 听发音", rate=0.8, key=f"arc_tts_{word['id']}")

    if not answered:
        bcols = st.columns(2)
        for i, c in enumerate(choices):
            with bcols[i % 2]:
                label = f"**{c['word']}**" if mode == "cn2en" else f"**{c['meaning']}**"
                if st.button(label, key=f"arc_{c['id']}", use_container_width=True):
                    is_correct = (c["id"] == word["id"])
                    arc_r = arcade_upsert(uname, word["id"], is_correct)
                    r = handle_answer(uname, word["id"], is_correct, "arcade")
                    if is_correct:
                        st.session_state.combo += 1
                        bonus = 1 + st.session_state.combo // 3
                        st.session_state.arcade_score += 10 * bonus
                        if arc_r["mastered"]:
                            st.toast(f"🌟 {word['word']} 已掌握！退出闯关词库", icon="✅")
                    else:
                        st.session_state.arcade_lives -= 1
                        st.session_state.combo = 0
                    st.session_state.arcade_result = (c["id"], is_correct, r, arc_r)
                    st.session_state.arcade_answered = True
                    st.rerun()
    else:
        chosen_id, is_correct, r, arc_r = st.session_state.arcade_result
        arc_cnt = arc_r.get("arcade_correct", 0)
        if is_correct:
            bonus = 1 + combo // 3
            mastered_hint = f" 🌟 已掌握！" if arc_r.get("mastered") else f" ({arc_cnt}/3次)"
            st.markdown(f'<div class="correct-banner">✅ +{10*bonus} 分！{mastered_hint}</div>',
                        unsafe_allow_html=True)
            show_result_banner({**r, "correct": True})
        else:
            st.markdown(f'<div class="wrong-banner">❌ 正确答案：{word["word"]}（{word["meaning"]}）</div>',
                        unsafe_allow_html=True)

        tts_button(word["word"], f"🔊 {word['word']}", rate=0.8,
                   key=f"arc_ans_tts_{word['id']}")

        if st.button("➡️ 继续", type="primary", use_container_width=True):
            # word 置 None 触发出新题；answered 置 False 清除答题状态
            st.session_state.arcade_word     = None
            st.session_state.arcade_answered = False
            st.rerun()


elif page == "topics":
    render_hud(prof)
    st.markdown("### 📚 分主题练习")

    topic_stats = {}
    for w in all_words:
        t = w["topic"]
        if t not in topic_stats:
            topic_stats[t] = {"total": 0, "known": 0, "wrong": 0}
        topic_stats[t]["total"] += 1
        if all_progress.get(w["id"], {}).get("status") == "known":
            topic_stats[t]["known"] += 1
        if all_progress.get(w["id"], {}).get("wrong", 0) > 0:
            topic_stats[t]["wrong"] += 1

    topics = [t for t, _ in sorted(
        topic_stats.items(),
        key=lambda item: (item[1]["known"] / item[1]["total"], item[1]["wrong"]),
        reverse=True
    )]
    sel_topic = st.selectbox("选择话题", ["全部"] + topics, key="topic_sel")
    sel_mode = st.selectbox(
        "练习模式",
        ["全部词", "错题优先", "未掌握词", "学习中词", "新词"],
        key="topic_practice_scope"
    )
    topic_words = all_words if sel_topic == "全部" else [w for w in all_words if w["topic"] == sel_topic]

    topic_total = len(topic_words)
    topic_known = sum(1 for w in topic_words if all_progress.get(w["id"], {}).get("status") == "known")
    topic_learning = sum(1 for w in topic_words if all_progress.get(w["id"], {}).get("status") == "learning")
    topic_new = topic_total - topic_known - topic_learning

    c1, c2, c3 = st.columns(3)
    c1.metric("总词数", topic_total)
    c2.metric("已掌握", topic_known)
    c3.metric("学习中", topic_learning)
    st.caption(f"未开始 {topic_new} 个单词")

    if topic_total > 0:
        st.progress(topic_known / topic_total)

    if topic_total == 0:
        st.info("当前话题暂无单词，请选择其他话题。")
    else:
        practice_words = topic_words
        if sel_mode == "错题优先":
            wrong_words = [w for w in topic_words if all_progress.get(w["id"], {}).get("wrong", 0) > 0]
            if wrong_words:
                practice_words = sorted(
                    wrong_words,
                    key=lambda w: all_progress.get(w["id"], {}).get("wrong", 0),
                    reverse=True
                )
                st.success(f"已优先选出 {len(wrong_words)} 个错题。")
            else:
                practice_words = topic_words
                st.info("本话题暂无错题，已使用全部词进行练习。")
        elif sel_mode == "未掌握词":
            practice_words = [w for w in topic_words if all_progress.get(w["id"], {}).get("status") != "known"]
        elif sel_mode == "学习中词":
            practice_words = [w for w in topic_words if all_progress.get(w["id"], {}).get("status") == "learning"]
        elif sel_mode == "新词":
            practice_words = [w for w in topic_words
                              if all_progress.get(w["id"], {}).get("status") not in ("learning", "known")]

        if sel_mode != "全部词" and not practice_words:
            st.warning("当前模式下没有可练习的词，已回退到全部词。")
            practice_words = topic_words

        if st.button("开始本话题练习", type="primary", use_container_width=True, key="topic_start"):
            st.session_state.topic_quiz_active = True
            st.session_state.topic_quiz_topic = sel_topic
            st.session_state.topic_quiz_scope = sel_mode
            st.session_state.topic_quiz_word = None
            st.session_state.topic_quiz_choices = []
            st.session_state.topic_quiz_answered = False
            st.session_state.topic_quiz_result = None
            st.rerun()

        if st.session_state.topic_quiz_active:
            if st.button("结束本话题练习", type="secondary", use_container_width=True, key="topic_stop"):
                st.session_state.topic_quiz_active = False
                st.session_state.topic_quiz_word = None
                st.session_state.topic_quiz_choices = []
                st.session_state.topic_quiz_answered = False
                st.session_state.topic_quiz_result = None
                st.rerun()

            if (st.session_state.topic_quiz_word is None or
                st.session_state.topic_quiz_topic != sel_topic or
                st.session_state.topic_quiz_scope != sel_mode):
                def _new_topic_quiz():
                    pool = practice_words or topic_words
                    w = random.choice(pool)
                    same_part = [x for x in pool if x["part"] == w["part"] and x["id"] != w["id"]]
                    distractor_pool = same_part if len(same_part) >= 3 else pool
                    distractors = sample_distractors(w, distractor_pool, all_words, 3)
                    choices = [w] + distractors
                    random.shuffle(choices)
                    st.session_state.topic_quiz_word = w
                    st.session_state.topic_quiz_choices = choices
                    st.session_state.topic_quiz_answered = False
                    st.session_state.topic_quiz_result = None

                _new_topic_quiz()

            word = st.session_state.topic_quiz_word
            choices = st.session_state.topic_quiz_choices
            answered = st.session_state.topic_quiz_answered

            mode = "cn2en" if word["id"] % 2 == 0 else "en2cn"
            if mode == "cn2en":
                st.markdown(f"""
                <div class="quiz-question">
                  <div class="quiz-cn">🇨🇳 {word['meaning']}</div>
                  <div class="quiz-hint">{word['part']} · 选出对应英文单词</div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="quiz-question">
                  <div style="font-size:2.2rem;font-weight:900;color:#667eea">{word['word']}</div>
                  <div style="color:#718096">{word.get('phonetic','')}</div>
                  <div class="quiz-hint">选出这个单词的中文意思</div>
                </div>""", unsafe_allow_html=True)
                tts_button(word["word"], "🔊 听发音", rate=0.8, key=f"topic_tts_{word['id']}")

            if not answered:
                bcols = st.columns(2)
                for i, c in enumerate(choices):
                    with bcols[i % 2]:
                        label = f"**{c['word']}**" if mode == "cn2en" else f"**{c['meaning']}**"
                        if st.button(label, key=f"topic_{c['id']}", use_container_width=True):
                            is_correct = (c["id"] == word["id"])
                            r = handle_answer(uname, word["id"], is_correct, "topics")
                            st.session_state.topic_quiz_result = (is_correct, r)
                            st.session_state.topic_quiz_answered = True
                            st.rerun()
            else:
                is_correct, r = st.session_state.topic_quiz_result
                if is_correct:
                    st.markdown(f'<div class="correct-banner">✅ 回答正确！</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="wrong-banner">❌ 正确答案：{word["word"]}（{word["meaning"]}）</div>', unsafe_allow_html=True)
                show_result_banner({**r, "correct": is_correct})
                if st.button("➡️ 下一题", type="primary", use_container_width=True, key="topic_next"):
                    st.session_state.topic_quiz_word = None
                    st.session_state.topic_quiz_choices = []
                    st.session_state.topic_quiz_answered = False
                    st.session_state.topic_quiz_result = None
                    st.rerun()


# ═══════════════════════════════════════════════════════
# 页面：我的进度
# ═══════════════════════════════════════════════════════

elif page == "stats":
    render_hud(prof)
    render_hud(prof)
    st.markdown("### 📊 我的进度")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("总词数", stats["total"])
    c2.metric("✅ 已掌握", stats["known"])
    c3.metric("📚 学习中", stats["learning"])
    c4.metric("🆕 未开始", stats["new"])

    c5, c6, c7, c8 = st.columns(4)
    c5.metric("📈 正确率", f"{stats['accuracy']:.1%}")
    c6.metric("🔥 打卡", f"{prof['daily_streak']}天")
    c7.metric("⚡ 最大连击", prof["max_combo"])
    c8.metric("🪙 金币", prof["coins"])

    # XP进度
    level, lv_start, lv_next = get_level_info(prof["xp"])
    xp_in = prof["xp"] - lv_start
    xp_need = lv_next - lv_start
    st.markdown(f"""
    <div style="background:white;border-radius:14px;padding:16px 20px;
                box-shadow:0 4px 14px rgba(0,0,0,0.07);margin:12px 0">
      <div style="display:flex;justify-content:space-between;margin-bottom:6px">
        <span style="font-weight:800">⭐ Lv.{level}</span>
        <span style="color:#718096;font-size:0.88rem">XP {prof['xp']} / {lv_next}</span>
      </div>
      <div class="xp-bar-wrap">
        <div class="xp-bar-fill" style="width:{min(xp_in/max(xp_need,1),1)*100:.1f}%"></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if stats["total"] > 0:
        kp = stats["known"] / stats["total"]
        lp = stats["learning"] / stats["total"]
        st.markdown(f"""
        <div style="background:white;border-radius:12px;padding:16px;margin:12px 0">
          <b>词库掌握分布</b>
          <div style="background:#e2e8f0;border-radius:8px;height:18px;
                      overflow:hidden;display:flex;margin-top:8px">
            <div style="width:{kp:.1%};background:#48bb78"></div>
            <div style="width:{lp:.1%};background:#ed8936"></div>
          </div>
          <div style="display:flex;gap:16px;margin-top:6px;font-size:0.82rem">
            <span>🟢 已掌握 {stats['known']}</span>
            <span>🟠 学习中 {stats['learning']}</span>
            <span>⚪ 未开始 {stats['new']}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    weak = get_weak_words(uname, 8)
    if weak:
        st.markdown("### ⚠️ 薄弱单词")
        for w in weak:
            with st.expander(f"**{w['word']}** — {w['meaning']}  ❌{w['err_rate']:.0%}错误率"):
                render_word_card(w, all_progress.get(w["id"]))

    st.markdown("---")
    st.markdown("### 📂 话题进度")
    topic_stats = {}
    for w in all_words:
        t = w["topic"]
        if t not in topic_stats:
            topic_stats[t] = {"total": 0, "known": 0}
        topic_stats[t]["total"] += 1
        if all_progress.get(w["id"], {}).get("status") == "known":
            topic_stats[t]["known"] += 1
    for t, ts in sorted(topic_stats.items()):
        p = ts["known"] / ts["total"] if ts["total"] else 0
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;
                    margin-bottom:2px;font-size:0.88rem">
          <span style="font-weight:600">{t}</span>
          <span style="color:#718096">{ts['known']}/{ts['total']}</span>
        </div>""", unsafe_allow_html=True)
        st.progress(p)


# ═══════════════════════════════════════════════════════
# 页面：我的徽章
# ═══════════════════════════════════════════════════════

elif page == "badges":
    render_hud(prof)
    st.markdown("### 🏅 我的徽章")
    earned = get_earned_badges(uname)
    earned_ids = {b["id"] for b in earned}
    st.caption(f"已获得 {len(earned)} / {len(BADGE_DEFS)} 个徽章")

    cols = st.columns(4)
    for i, (bid, (name, icon, desc)) in enumerate(BADGE_DEFS.items()):
        unlocked = bid in earned_ids
        with cols[i % 4]:
            locked_cls = "" if unlocked else "badge-locked"
            st.markdown(f"""
            <div class="badge-card {locked_cls}" style="margin-bottom:12px">
              <div class="badge-icon">{icon}</div>
              <div class="badge-name">{name}</div>
              <div class="badge-desc">{desc}</div>
              {"" if unlocked else '<div style="font-size:0.72rem;color:#c0c0c0;margin-top:4px">🔒 未解锁</div>'}
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# 页面：词库浏览
# ═══════════════════════════════════════════════════════

elif page == "wordlist":
    st.markdown("### 📋 词库浏览")
    fc1, fc2, fc3 = st.columns(3)
    topics = sorted(set(w["topic"] for w in all_words))
    sel_topic = fc1.selectbox("话题", ["全部"] + topics)
    sel_level = fc2.selectbox("级别", ["全部", "A类（衔接）", "B类（核心）", "C类（拓展）"])
    sel_status = fc3.selectbox("状态", ["全部", "未开始", "学习中", "已掌握"])
    search = st.text_input("🔍 搜索", placeholder="输入英文或中文…")

    level_map = {"A类（衔接）":"A","B类（核心）":"B","C类（拓展）":"C"}
    filtered = all_words
    if sel_topic != "全部":
        filtered = [w for w in filtered if w["topic"] == sel_topic]
    if sel_level != "全部":
        filtered = [w for w in filtered if w["level"] == level_map[sel_level]]
    if sel_status != "全部":
        sm = {"未开始":"new","学习中":"learning","已掌握":"known"}[sel_status]
        if sm == "new":
            filtered = [w for w in filtered if w["id"] not in all_progress]
        else:
            filtered = [w for w in filtered
                        if all_progress.get(w["id"],{}).get("status") == sm]
    if search:
        s = search.lower()
        filtered = [w for w in filtered
                    if s in w["word"].lower() or s in w["meaning"]]

    st.caption(f"共 {len(filtered)} 个单词")
    for w in filtered:
        prog = all_progress.get(w["id"])
        status = prog["status"] if prog else "new"
        icon = {"known":"✅","learning":"📖","new":"🆕"}.get(status,"🆕")
        with st.expander(f"{icon} **{w['word']}**  {w['phonetic']}  ·  {w['meaning']}"):
            render_word_card(w, prog, show_tts=True)
            ca, cb = st.columns(2)
            if ca.button("✅ 标记已会", key=f"wl_ok_{w['id']}", use_container_width=True):
                upsert_progress(uname, w["id"], True)
                st.rerun()
            if cb.button("🔄 加入复习", key=f"wl_rev_{w['id']}", use_container_width=True):
                upsert_progress(uname, w["id"], False)
                st.rerun()
