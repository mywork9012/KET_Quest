"""
KET 专属背词软件 - 主应用入口
运行: streamlit run app.py
Python 3.11+, Streamlit 1.35+
"""

import streamlit as st
import random
import re
from datetime import date

# ── 页面配置（必须第一行）────────────────────────────────────────────────
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
)
from utils.planner import get_today_plan, STAGES

# ── 初始化DB ─────────────────────────────────────────────────────────────
init_db()

# ── 全局CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* 导入字体 */
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&family=Noto+Sans+SC:wght@400;500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', 'Noto Sans SC', sans-serif;
}

/* 主背景 */
.stApp {
    background: linear-gradient(135deg, #667eea22 0%, #764ba222 100%);
}

/* 单词卡片 */
.word-card {
    background: white;
    border-radius: 20px;
    padding: 28px 32px;
    box-shadow: 0 8px 32px rgba(102,126,234,0.15);
    border-left: 6px solid #667eea;
    margin-bottom: 16px;
}
.word-main {
    font-size: 2.8rem;
    font-weight: 800;
    color: #2d3748;
    letter-spacing: -1px;
}
.word-phonetic {
    font-size: 1.1rem;
    color: #7c8db0;
    margin: 4px 0 8px;
}
.word-part {
    display: inline-block;
    background: #667eea;
    color: white;
    border-radius: 8px;
    padding: 2px 10px;
    font-size: 0.85rem;
    font-weight: 700;
    margin-right: 8px;
}
.word-meaning {
    font-size: 1.4rem;
    font-weight: 700;
    color: #4a5568;
    margin-top: 8px;
}

/* 例句卡片 */
.sentence-card {
    background: linear-gradient(135deg, #f8f9ff, #eef2ff);
    border-radius: 14px;
    padding: 18px 22px;
    margin: 10px 0;
    border: 1px solid #e2e8f0;
}
.sentence-en {
    font-size: 1.15rem;
    font-weight: 600;
    color: #2d3748;
    line-height: 1.8;
}
.sentence-cn {
    font-size: 0.95rem;
    color: #718096;
    margin-top: 6px;
}
.highlight {
    color: #667eea;
    font-weight: 800;
    text-decoration: underline;
    text-decoration-color: #667eeaaa;
}

/* 状态徽章 */
.badge-new      { background:#e2e8f0; color:#4a5568; }
.badge-learning { background:#fed7aa; color:#c05621; }
.badge-known    { background:#c6f6d5; color:#276749; }
.badge {
    display:inline-block; border-radius:20px;
    padding:3px 12px; font-size:0.8rem; font-weight:700;
}

/* 进度环 */
.stat-box {
    background: white;
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 4px 16px rgba(0,0,0,0.08);
}
.stat-number {
    font-size: 2.2rem;
    font-weight: 800;
    color: #667eea;
}
.stat-label {
    font-size: 0.85rem;
    color: #718096;
    margin-top: 4px;
}

/* 按钮覆盖 */
div[data-testid="stButton"] > button {
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-family: 'Nunito', 'Noto Sans SC', sans-serif !important;
    transition: transform 0.15s ease !important;
}
div[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
}

/* 练习区 */
.quiz-question {
    background: white;
    border-radius: 18px;
    padding: 28px;
    box-shadow: 0 6px 24px rgba(0,0,0,0.08);
    text-align: center;
    margin-bottom: 20px;
}
.quiz-cn {
    font-size: 1.5rem;
    font-weight: 700;
    color: #2d3748;
    margin-bottom: 8px;
}
.quiz-hint {
    font-size: 0.9rem;
    color: #a0aec0;
}
.correct-banner {
    background: linear-gradient(135deg,#48bb78,#38a169);
    color: white; border-radius: 14px; padding: 16px;
    text-align: center; font-size: 1.2rem; font-weight: 700;
    margin: 12px 0;
}
.wrong-banner {
    background: linear-gradient(135deg,#fc8181,#e53e3e);
    color: white; border-radius: 14px; padding: 16px;
    text-align: center; font-size: 1.2rem; font-weight: 700;
    margin: 12px 0;
}

/* 侧边栏 */
.sidebar-header {
    background: linear-gradient(135deg,#667eea,#764ba2);
    color: white; border-radius: 14px; padding: 16px 18px;
    margin-bottom: 12px;
    text-align: center;
}
.user-chip {
    background: #667eea22;
    border-radius: 20px;
    padding: 6px 14px;
    font-weight: 700;
    color: #667eea;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════
# 辅助函数
# ═══════════════════════════════════════════════════════════════════

def render_sentence(sentence: str) -> str:
    """把 **word** 转换为高亮HTML"""
    return re.sub(
        r'\*\*(.+?)\*\*',
        r'<span class="highlight">\1</span>',
        sentence
    )


def status_badge(status: str) -> str:
    label = {"new": "新词", "learning": "学习中", "known": "已掌握"}.get(status, status)
    cls = f"badge badge-{status}"
    return f'<span class="{cls}">{label}</span>'


def render_word_card(word: dict, progress: dict | None = None):
    """渲染单词主卡片"""
    status = progress["status"] if progress else "new"
    badge = status_badge(status)
    s1 = render_sentence(word.get("sentence1", ""))
    s2 = render_sentence(word.get("sentence2", ""))
    s1_cn = word.get("sentence1_cn", "")
    s2_cn = word.get("sentence2_cn", "")
    topic_icon = {
        "character": "😊", "school": "📚", "daily_life": "🛒",
        "travel": "✈️", "hobbies": "🎵", "states": "💡",
        "study_work": "✏️", "life_shopping": "🏠",
        "travel_weather": "🌤️", "hobbies_health": "❤️",
    }.get(word.get("topic_en", ""), "📖")

    st.markdown(f"""
    <div class="word-card">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;">
        <div>
          <div class="word-main">{word['word']}</div>
          <div class="word-phonetic">{word.get('phonetic','')}</div>
          <span class="word-part">{word.get('part','')}</span>
          {badge}
        </div>
        <div style="font-size:2rem">{topic_icon}</div>
      </div>
      <div class="word-meaning">{word.get('meaning','')}</div>
      <div style="font-size:0.8rem;color:#a0aec0;margin-top:6px;">
        {word.get('topic','')} · {word.get('level','')+'类词'}
      </div>
    </div>
    """, unsafe_allow_html=True)

    if s1:
        st.markdown(f"""
        <div class="sentence-card">
          <div class="sentence-en">① {s1}</div>
          <div class="sentence-cn">🇨🇳 {s1_cn}</div>
        </div>
        """, unsafe_allow_html=True)
    if s2:
        st.markdown(f"""
        <div class="sentence-card">
          <div class="sentence-en">② {s2}</div>
          <div class="sentence-cn">🇨🇳 {s2_cn}</div>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════
# Session State 初始化
# ═══════════════════════════════════════════════════════════════════

def _ss(key, default):
    if key not in st.session_state:
        st.session_state[key] = default


_ss("username", None)
_ss("page", "home")
_ss("study_idx", 0)
_ss("study_words", [])
_ss("quiz_word", None)
_ss("quiz_choices", [])
_ss("quiz_answered", False)
_ss("quiz_result", None)
_ss("fill_word", None)
_ss("fill_answered", False)
_ss("fill_result", None)
_ss("fill_input", "")
_ss("review_ids", [])
_ss("review_idx", 0)


# ═══════════════════════════════════════════════════════════════════
# 侧边栏：用户选择 + 导航
# ═══════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
      <div style="font-size:1.8rem">🎯</div>
      <div style="font-size:1.2rem;font-weight:800">KET 冲刺背词</div>
      <div style="font-size:0.8rem;opacity:0.85">四年级 · 4个月闭环备考</div>
    </div>
    """, unsafe_allow_html=True)

    # ── 用户登录 ──
    users = list_users()
    user_names = [u["username"] for u in users]

    with st.expander("👤 切换用户", expanded=(st.session_state.username is None)):
        col1, col2 = st.columns([2, 1])
        new_name = col1.text_input("用户名", placeholder="输入你的名字", label_visibility="collapsed")
        if col2.button("进入", use_container_width=True) and new_name.strip():
            uname = new_name.strip()
            get_or_create_user(uname, uname)
            st.session_state.username = uname
            st.session_state.page = "home"
            st.rerun()

        if user_names:
            st.markdown("**已有用户：**")
            for u in users:
                if st.button(f"👤 {u['display_name']}", key=f"u_{u['username']}",
                             use_container_width=True):
                    st.session_state.username = u["username"]
                    st.session_state.page = "home"
                    st.rerun()

    if st.session_state.username:
        uname = st.session_state.username
        st.markdown(f'<div class="user-chip">👋 {uname}</div>', unsafe_allow_html=True)
        st.divider()

        # ── 导航菜单 ──
        nav_items = [
            ("🏠", "今日计划", "home"),
            ("📖", "学新词", "learn"),
            ("🔄", "复习单词", "review"),
            ("✏️", "填空练习", "fill"),
            ("🧩", "选词练习", "quiz"),
            ("📊", "我的进度", "stats"),
            ("📋", "词库浏览", "wordlist"),
        ]
        for icon, label, pg in nav_items:
            is_active = st.session_state.page == pg
            btn_label = f"{icon} {label}" + ("  ◀" if is_active else "")
            if st.button(btn_label, key=f"nav_{pg}", use_container_width=True):
                st.session_state.page = pg
                # 重置子状态
                st.session_state.study_idx = 0
                st.session_state.quiz_answered = False
                st.session_state.fill_answered = False
                st.rerun()

        st.divider()
        # 快速统计
        stats = get_stats(uname)
        c1, c2 = st.columns(2)
        c1.metric("✅ 已掌握", stats["known"])
        c2.metric("📅 剩余天", stats["days_left"])
        c1.metric("🔄 待复习", stats["review_due"])
        c2.metric("📈 正确率", f"{stats['accuracy']:.0%}")


# ═══════════════════════════════════════════════════════════════════
# 未登录提示
# ═══════════════════════════════════════════════════════════════════

if not st.session_state.username:
    st.markdown("""
    <div style="text-align:center;padding:80px 20px;">
      <div style="font-size:4rem">🎯</div>
      <h1 style="font-size:2.5rem;font-weight:800;color:#667eea">KET 冲刺背词</h1>
      <p style="font-size:1.2rem;color:#718096;margin:16px 0">
        四年级 · 已过剑桥三级 · 4个月闭环冲刺 KET
      </p>
      <p style="color:#a0aec0">← 在左侧输入你的名字开始学习</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

uname = st.session_state.username
user = get_or_create_user(uname)
page = st.session_state.page
all_words = load_words()
all_progress = get_all_progress(uname)
stats = get_stats(uname)


# ═══════════════════════════════════════════════════════════════════
# 页面：今日计划 (home)
# ═══════════════════════════════════════════════════════════════════

if page == "home":
    plan = get_today_plan(uname, user["start_date"])
    stage = plan["stage"]

    st.markdown(f"""
    <h2 style="color:#2d3748;font-weight:800;margin-bottom:4px">
      📅 今日计划 · 第 {plan['day']} 天
    </h2>
    <p style="color:#718096;">备考倒计时 <b>{plan['days_left']}</b> 天 &nbsp;·&nbsp;
    <span style="color:{stage['color']};font-weight:700">{stage['name']} · {stage['label']}</span></p>
    """, unsafe_allow_html=True)

    # 进度条
    pct = min(plan["day"] / 120, 1.0)
    st.progress(pct, text=f"总进度 {pct:.0%}")

    # 每日提示
    st.info(plan["tips"])

    # 数据卡片行
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="stat-box">
          <div class="stat-number" style="color:#667eea">{plan['new_count']}</div>
          <div class="stat-label">今日新词</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="stat-box">
          <div class="stat-number" style="color:#f6ad55">{stats['review_due']}</div>
          <div class="stat-label">待复习</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="stat-box">
          <div class="stat-number" style="color:#48bb78">{stats['known']}</div>
          <div class="stat-label">已掌握</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="stat-box">
          <div class="stat-number" style="color:#ed64a6">{stats['accuracy']:.0%}</div>
          <div class="stat-label">正确率</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # 今日新词预览
    st.markdown("### 📚 今日新词")
    cols = st.columns(4)
    for i, w in enumerate(plan["new_words"]):
        prog = all_progress.get(w["id"])
        status = prog["status"] if prog else "new"
        with cols[i % 4]:
            st.markdown(f"""
            <div style="background:white;border-radius:12px;padding:12px 14px;
                        box-shadow:0 3px 12px rgba(0,0,0,0.07);margin-bottom:8px;
                        border-top:3px solid #667eea;">
              <div style="font-size:1.1rem;font-weight:800;color:#2d3748">{w['word']}</div>
              <div style="font-size:0.8rem;color:#718096">{w['phonetic']}</div>
              <div style="font-size:0.9rem;color:#4a5568;font-weight:600;margin-top:4px">{w['meaning']}</div>
              {status_badge(status)}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # 四阶段路线图
    st.markdown("### 🗺️ 备考路线图")
    scols = st.columns(4)
    for i, s in enumerate(STAGES):
        lo, hi = s["days"]
        day = plan["day"]
        is_current = lo <= day <= hi
        is_done = day > hi
        with scols[i]:
            border = "3px solid #667eea" if is_current else "2px solid #e2e8f0"
            opacity = "1.0" if (is_current or is_done) else "0.5"
            st.markdown(f"""
            <div style="background:white;border-radius:14px;padding:16px;
                        border:{border};opacity:{opacity};text-align:center;">
              <div style="font-size:1.5rem">{s['color'] and ('✅' if is_done else ('🔥' if is_current else '⏳'))}</div>
              <div style="font-weight:800;color:#2d3748;font-size:0.9rem">{s['name']}</div>
              <div style="font-size:0.75rem;color:#718096">Day {lo}–{hi}</div>
              <div style="font-size:0.8rem;font-weight:700;color:#667eea;margin-top:4px">{s['label']}</div>
              <div style="font-size:0.72rem;color:#a0aec0;margin-top:4px">{s['desc']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    col_a, col_b, col_c = st.columns(3)
    if col_a.button("📖 开始学新词", use_container_width=True, type="primary"):
        st.session_state.page = "learn"
        st.session_state.study_words = plan["new_words"]
        st.session_state.study_idx = 0
        st.rerun()
    if col_b.button("🔄 开始复习", use_container_width=True):
        st.session_state.page = "review"
        st.rerun()
    if col_c.button("✏️ 填空练习", use_container_width=True):
        st.session_state.page = "fill"
        st.rerun()


# ═══════════════════════════════════════════════════════════════════
# 页面：学新词 (learn)
# ═══════════════════════════════════════════════════════════════════

elif page == "learn":
    plan = get_today_plan(uname, user["start_date"])
    if not st.session_state.study_words:
        st.session_state.study_words = plan["new_words"]
        st.session_state.study_idx = 0

    words_to_study = st.session_state.study_words
    idx = st.session_state.study_idx

    if not words_to_study:
        st.warning("今天没有新词任务。")
        st.stop()

    # 顶部进度
    total = len(words_to_study)
    st.markdown(f"### 📖 学新词 &nbsp; <span style='color:#a0aec0;font-size:1rem'>{idx+1} / {total}</span>",
                unsafe_allow_html=True)
    st.progress((idx + 1) / total)

    word = words_to_study[idx]
    prog = all_progress.get(word["id"])
    render_word_card(word, prog)

    # 操作按钮
    st.markdown("---")
    c1, c2, c3, c4 = st.columns(4)

    if c1.button("⬅️ 上一个", use_container_width=True, disabled=(idx == 0)):
        st.session_state.study_idx -= 1
        st.rerun()

    if c2.button("✅ 已会了", use_container_width=True, type="primary"):
        upsert_progress(uname, word["id"], correct=True)
        if idx < total - 1:
            st.session_state.study_idx += 1
        st.rerun()

    if c3.button("🔄 再看看", use_container_width=True):
        upsert_progress(uname, word["id"], correct=False)
        if idx < total - 1:
            st.session_state.study_idx += 1
        st.rerun()

    if c4.button("➡️ 下一个", use_container_width=True, disabled=(idx >= total - 1)):
        st.session_state.study_idx += 1
        st.rerun()

    if idx >= total - 1:
        st.success("🎉 今日新词学完了！去复习一下吧。")
        if st.button("去复习 →", type="primary"):
            st.session_state.page = "review"
            st.rerun()


# ═══════════════════════════════════════════════════════════════════
# 页面：复习单词 (review)
# ═══════════════════════════════════════════════════════════════════

elif page == "review":
    review_ids = get_today_review_ids(uname)

    if not review_ids:
        st.success("🎊 今天没有待复习的单词，太棒了！")
        # 如果没有待复习，显示快速看所有学过的词
        learned = [w for w in all_words if w["id"] in all_progress]
        if learned:
            st.markdown("### 📋 你已学过的单词")
            random.shuffle(learned)
            for w in learned[:10]:
                prog = all_progress.get(w["id"])
                with st.expander(f"**{w['word']}** — {w['meaning']}"):
                    render_word_card(w, prog)
        st.stop()

    if not st.session_state.review_ids or set(st.session_state.review_ids) != set(review_ids):
        st.session_state.review_ids = review_ids
        st.session_state.review_idx = 0

    idx = st.session_state.review_idx
    total = len(review_ids)

    st.markdown(f"### 🔄 复习单词 &nbsp; <span style='color:#a0aec0;font-size:1rem'>{min(idx+1,total)} / {total}</span>",
                unsafe_allow_html=True)
    st.progress(min((idx + 1) / total, 1.0))

    if idx >= total:
        st.success(f"🎉 本轮 {total} 个单词复习完成！")
        if st.button("再来一轮", type="primary"):
            st.session_state.review_idx = 0
            st.rerun()
        st.stop()

    word_id = review_ids[idx]
    word = get_word_by_id(word_id)
    if not word:
        st.session_state.review_idx += 1
        st.rerun()

    prog = all_progress.get(word["id"])
    render_word_card(word, prog)

    st.markdown("---")
    c1, c2, c3 = st.columns(3)

    if c1.button("✅ 记得！", use_container_width=True, type="primary"):
        upsert_progress(uname, word_id, correct=True)
        st.session_state.review_idx += 1
        st.rerun()

    if c2.button("😅 模糊", use_container_width=True):
        upsert_progress(uname, word_id, correct=False)
        st.session_state.review_idx += 1
        st.rerun()

    if c3.button("❌ 不记得", use_container_width=True):
        upsert_progress(uname, word_id, correct=False)
        st.session_state.review_idx += 1
        st.rerun()

    # 进度数字
    if prog:
        streak = prog.get("streak", 0)
        st.caption(f"连续答对 {streak} 次 · 正确 {prog['correct']} / 错误 {prog['wrong']}")


# ═══════════════════════════════════════════════════════════════════
# 页面：填空练习 (fill)
# ═══════════════════════════════════════════════════════════════════

elif page == "fill":
    st.markdown("### ✏️ 句子填空练习")
    st.caption("看中文例句，写出缺失的英文单词")

    # 选取候选词：已学过的词
    learned_words = [w for w in all_words if w["id"] in all_progress and w.get("sentence1")]
    if len(learned_words) < 4:
        # 补充未学词保证有题可做
        learned_words = [w for w in all_words if w.get("sentence1")][:20]

    if not st.session_state.fill_word or st.session_state.fill_answered:
        # 选新题
        w = random.choice(learned_words)
        st.session_state.fill_word = w
        st.session_state.fill_answered = False
        st.session_state.fill_result = None
        st.session_state.fill_input = ""

    word = st.session_state.fill_word
    answered = st.session_state.fill_answered

    # 随机选例句1或2
    if word.get("sentence2") and random.random() > 0.5:
        sent = word["sentence2"]
        sent_cn = word["sentence2_cn"]
    else:
        sent = word["sentence1"]
        sent_cn = word["sentence1_cn"]

    # 把 **word** 替换为下划线
    blank_sent = re.sub(r'\*\*(.+?)\*\*', '______', sent)

    st.markdown(f"""
    <div class="quiz-question">
      <div class="quiz-cn">🇨🇳 {sent_cn}</div>
      <div class="sentence-en" style="margin-top:14px;">📝 {blank_sent}</div>
      <div class="quiz-hint" style="margin-top:8px;">填写缺失单词（{word['part']} · {word['meaning']}）</div>
    </div>
    """, unsafe_allow_html=True)

    if not answered:
        user_input = st.text_input(
            "输入单词",
            value=st.session_state.fill_input,
            placeholder=f"请输入单词…",
            label_visibility="collapsed",
            key="fill_text_input"
        )
        st.session_state.fill_input = user_input

        if st.button("✅ 提交", type="primary", use_container_width=True):
            correct_word = word["word"].lower().strip()
            user_word = user_input.lower().strip()
            # 提取**...**中的真实答案
            match = re.search(r'\*\*(.+?)\*\*', sent)
            if match:
                correct_word = match.group(1).lower().strip()
            is_correct = (user_word == correct_word)
            st.session_state.fill_result = is_correct
            st.session_state.fill_answered = True
            upsert_progress(uname, word["id"], correct=is_correct)
            log_fill(uname, word["id"], "fill", is_correct)
            st.rerun()
    else:
        result = st.session_state.fill_result
        match = re.search(r'\*\*(.+?)\*\*', sent)
        correct_word = match.group(1) if match else word["word"]

        if result:
            st.markdown(f'<div class="correct-banner">✅ 正确！答案是 <b>{correct_word}</b></div>',
                        unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="wrong-banner">❌ 正确答案是 <b>{correct_word}</b></div>',
                        unsafe_allow_html=True)

        # 显示完整例句
        full_sent = render_sentence(sent)
        st.markdown(f"""
        <div class="sentence-card">
          <div class="sentence-en">{full_sent}</div>
          <div class="sentence-cn">🇨🇳 {sent_cn}</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("➡️ 下一题", type="primary", use_container_width=True):
            st.session_state.fill_word = None
            st.session_state.fill_answered = False
            st.rerun()


# ═══════════════════════════════════════════════════════════════════
# 页面：选词练习 (quiz)  ── KET完形填空风格
# ═══════════════════════════════════════════════════════════════════

elif page == "quiz":
    st.markdown("### 🧩 选词练习")
    st.caption("四选一：根据中文提示选出正确单词")

    learned_ids = list(all_progress.keys())
    if len(learned_ids) < 4:
        pool = all_words[:40]
    else:
        pool = [w for w in all_words if w["id"] in learned_ids]

    def _new_quiz():
        word = random.choice(pool)
        # 生成3个干扰项（同词性优先）
        same_pos = [w for w in pool if w["part"] == word["part"] and w["id"] != word["id"]]
        distractors = random.sample(same_pos if len(same_pos) >= 3 else pool, 3)
        choices = [word] + distractors
        random.shuffle(choices)
        st.session_state.quiz_word = word
        st.session_state.quiz_choices = choices
        st.session_state.quiz_answered = False
        st.session_state.quiz_result = None

    if not st.session_state.quiz_word or st.session_state.quiz_answered:
        _new_quiz()
        if st.session_state.quiz_answered:   # 答完后先展示结果再刷新
            pass

    word = st.session_state.quiz_word
    choices = st.session_state.quiz_choices
    answered = st.session_state.quiz_answered

    # 随机取一句例句，挖空显示中文
    if word.get("sentence2") and random.random() > 0.6:
        sent = word["sentence2"]
        sent_cn = word["sentence2_cn"]
    else:
        sent = word["sentence1"]
        sent_cn = word["sentence1_cn"]

    blank_sent = re.sub(r'\*\*(.+?)\*\*', '______', sent)

    st.markdown(f"""
    <div class="quiz-question">
      <div class="quiz-cn">🇨🇳 {sent_cn}</div>
      <div class="sentence-en" style="margin-top:14px;">📝 {blank_sent}</div>
      <div class="quiz-hint" style="margin-top:8px;">选出空白处的正确单词</div>
    </div>
    """, unsafe_allow_html=True)

    if not answered:
        bcols = st.columns(2)
        for i, c in enumerate(choices):
            with bcols[i % 2]:
                label = f"**{c['word']}** — {c['meaning']}"
                if st.button(label, key=f"choice_{c['id']}", use_container_width=True):
                    is_correct = (c["id"] == word["id"])
                    st.session_state.quiz_result = (c["id"], is_correct)
                    st.session_state.quiz_answered = True
                    upsert_progress(uname, word["id"], correct=is_correct)
                    log_fill(uname, word["id"], "quiz", is_correct)
                    st.rerun()
    else:
        chosen_id, is_correct = st.session_state.quiz_result
        if is_correct:
            st.markdown(f'<div class="correct-banner">✅ 正确！</div>', unsafe_allow_html=True)
        else:
            correct_label = word["word"]
            st.markdown(f'<div class="wrong-banner">❌ 正确答案是 <b>{correct_label}</b></div>',
                        unsafe_allow_html=True)

        full_sent = render_sentence(sent)
        st.markdown(f"""
        <div class="sentence-card">
          <div class="sentence-en">{full_sent}</div>
          <div class="sentence-cn">🇨🇳 {sent_cn}</div>
        </div>
        """, unsafe_allow_html=True)

        # 显示选项对错
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
            _new_quiz()
            st.rerun()


# ═══════════════════════════════════════════════════════════════════
# 页面：我的进度 (stats)
# ═══════════════════════════════════════════════════════════════════

elif page == "stats":
    st.markdown("### 📊 我的进度")

    # 总体数据
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("总词数", stats["total"])
    c2.metric("✅ 已掌握", stats["known"])
    c3.metric("📚 学习中", stats["learning"])
    c4.metric("🆕 未开始", stats["new"])

    c5, c6, c7 = st.columns(3)
    c5.metric("📈 正确率", f"{stats['accuracy']:.1%}")
    c6.metric("⏰ 备考天数", stats["days_elapsed"])
    c7.metric("📅 剩余天数", stats["days_left"])

    # 掌握进度条
    if stats["total"] > 0:
        known_pct = stats["known"] / stats["total"]
        learning_pct = stats["learning"] / stats["total"]
        st.markdown(f"""
        <div style="background:#f7fafc;border-radius:12px;padding:16px;margin:16px 0">
          <div style="font-weight:700;color:#2d3748;margin-bottom:10px">📊 词库掌握分布</div>
          <div style="background:#e2e8f0;border-radius:8px;height:20px;overflow:hidden;display:flex">
            <div style="width:{known_pct:.1%};background:#48bb78;"></div>
            <div style="width:{learning_pct:.1%};background:#ed8936;"></div>
          </div>
          <div style="display:flex;gap:20px;margin-top:8px;font-size:0.85rem">
            <span>🟢 已掌握 {stats['known']}词</span>
            <span>🟠 学习中 {stats['learning']}词</span>
            <span>⚪ 未开始 {stats['new']}词</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # 薄弱单词
    weak = get_weak_words(uname, limit=10)
    if weak:
        st.markdown("### ⚠️ 薄弱单词（错误率最高）")
        for w in weak:
            err_pct = w["err_rate"] * 100
            with st.expander(f"**{w['word']}** — {w['meaning']} &nbsp;&nbsp; ❌ 错误率 {err_pct:.0f}%"):
                prog = all_progress.get(w["id"])
                render_word_card(w, prog)
                st.caption(f"答对 {w['correct']} 次 · 答错 {w['wrong']} 次")

    # 按话题进度
    st.markdown("---")
    st.markdown("### 📂 话题进度")
    topic_stats = {}
    for w in all_words:
        t = w["topic"]
        if t not in topic_stats:
            topic_stats[t] = {"total": 0, "known": 0, "learning": 0}
        topic_stats[t]["total"] += 1
        prog = all_progress.get(w["id"])
        if prog:
            if prog["status"] == "known":
                topic_stats[t]["known"] += 1
            elif prog["status"] == "learning":
                topic_stats[t]["learning"] += 1

    for topic, ts in sorted(topic_stats.items()):
        known_p = ts["known"] / ts["total"] if ts["total"] else 0
        st.markdown(f"""
        <div style="margin-bottom:8px;">
          <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
            <span style="font-weight:600;font-size:0.9rem">{topic}</span>
            <span style="color:#718096;font-size:0.85rem">
              {ts['known']}/{ts['total']} 已掌握
            </span>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(known_p)


# ═══════════════════════════════════════════════════════════════════
# 页面：词库浏览 (wordlist)
# ═══════════════════════════════════════════════════════════════════

elif page == "wordlist":
    st.markdown("### 📋 词库浏览")

    # 筛选
    fc1, fc2, fc3 = st.columns(3)
    topics = sorted(set(w["topic"] for w in all_words))
    sel_topic = fc1.selectbox("话题", ["全部"] + topics)
    sel_level = fc2.selectbox("级别", ["全部", "A类（衔接）", "B类（核心）", "C类（拓展）"])
    sel_status = fc3.selectbox("掌握状态", ["全部", "未开始", "学习中", "已掌握"])
    search = st.text_input("🔍 搜索单词", placeholder="输入英文或中文…")

    level_map = {"A类（衔接）": "A", "B类（核心）": "B", "C类（拓展）": "C"}
    status_map = {"未开始": "new", "学习中": "learning", "已掌握": "known"}

    filtered = all_words
    if sel_topic != "全部":
        filtered = [w for w in filtered if w["topic"] == sel_topic]
    if sel_level != "全部":
        filtered = [w for w in filtered if w["level"] == level_map[sel_level]]
    if sel_status != "全部":
        target_status = status_map[sel_status]
        if target_status == "new":
            filtered = [w for w in filtered if w["id"] not in all_progress]
        else:
            filtered = [w for w in filtered if
                        all_progress.get(w["id"], {}).get("status") == target_status]
    if search:
        s = search.lower()
        filtered = [w for w in filtered if
                    s in w["word"].lower() or s in w["meaning"]]

    st.caption(f"共 {len(filtered)} 个单词")

    for w in filtered:
        prog = all_progress.get(w["id"])
        status = prog["status"] if prog else "new"
        with st.expander(
            f"**{w['word']}** &nbsp; {w['phonetic']} &nbsp;·&nbsp; {w['meaning']} &nbsp;&nbsp; "
            + ("✅" if status == "known" else "📖" if status == "learning" else "🆕")
        ):
            render_word_card(w, prog)
            cc1, cc2 = st.columns(2)
            if cc1.button("✅ 标记已会", key=f"wl_ok_{w['id']}", use_container_width=True):
                upsert_progress(uname, w["id"], correct=True)
                st.rerun()
            if cc2.button("🔄 加入复习", key=f"wl_rev_{w['id']}", use_container_width=True):
                upsert_progress(uname, w["id"], correct=False)
                st.rerun()
