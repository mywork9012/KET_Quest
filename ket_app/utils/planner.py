"""
4个月（120天）KET备考计划模块
按阶段自动分配每日新词、复习任务
"""

from datetime import date
from utils.db import load_words

# ── 阶段定义 ─────────────────────────────────────────────────────────────
STAGES = [
    {"name": "第一阶段", "days": (1, 30),   "label": "基础衔接",
     "desc": "过KET基础衔接词 + 入门例句，建立语感",
     "new_per_day": 8,  "color": "#4ECDC4"},
    {"name": "第二阶段", "days": (31, 60),  "label": "核心积累",
     "desc": "主攻KET核心高频词 + 常规KET例句，大量积累搭配",
     "new_per_day": 9,  "color": "#45B7D1"},
    {"name": "第三阶段", "days": (61, 90),  "label": "二轮复习",
     "desc": "全词二轮复习 + 例句仿写训练 + 固定搭配专项",
     "new_per_day": 6,  "color": "#96CEB4"},
    {"name": "第四阶段", "days": (91, 120), "label": "冲刺闯关",
     "desc": "真题词汇复盘 + 例句句型整合 + 模拟闯关自测",
     "new_per_day": 4,  "color": "#FFEAA7"},
]


def get_stage(day: int) -> dict:
    """根据第几天返回当前阶段信息"""
    for s in STAGES:
        lo, hi = s["days"]
        if lo <= day <= hi:
            return s
    return STAGES[-1]  # 超出120天仍返回第四阶段


def get_today_plan(username: str, start_date_str: str) -> dict:
    """
    计算今日学习计划
    返回: {day, stage, new_words[], review_count, tips}
    """
    start = date.fromisoformat(start_date_str)
    day = (date.today() - start).days + 1
    day = max(1, min(day, 120))
    stage = get_stage(day)

    words = load_words()

    # 按level分层：A类前40词、B类40-158词、C类159-198词
    a_words = [w for w in words if w["level"] == "A"]   # 40词
    b_words = [w for w in words if w["level"] == "B"]   # 118词
    c_words = [w for w in words if w["level"] == "C"]   # 40词

    if day <= 30:
        pool = a_words                         # 阶段一：A类词
    elif day <= 60:
        pool = b_words[:60]                    # 阶段二：B类前60
    elif day <= 90:
        pool = b_words[60:] + c_words[:20]    # 阶段三：B类后段 + C类前段
    else:
        pool = c_words[20:]                    # 阶段四：C类后段 + 复盘

    new_per_day = stage["new_per_day"]
    day_in_stage = day - stage["days"][0]

    # 今日应学新词：按日偏移从pool取
    start_idx = (day_in_stage * new_per_day) % max(len(pool), 1)
    end_idx = start_idx + new_per_day
    if end_idx <= len(pool):
        today_new = pool[start_idx:end_idx]
    else:
        today_new = pool[start_idx:] + pool[:end_idx - len(pool)]

    tips = _get_tips(day)

    return {
        "day": day,
        "days_left": max(0, 120 - day),
        "stage": stage,
        "new_words": today_new,
        "new_count": len(today_new),
        "tips": tips,
    }


def _get_tips(day: int) -> str:
    tips_map = {
        range(1, 8):   "🌱 第一周！先把每个单词大声读3遍，跟着例句朗读。",
        range(8, 15):  "📖 坚持一周了！尝试用单词造句，哪怕很简单也好。",
        range(15, 31): "🔄 做完新词再回头复习前面的，记忆更牢固！",
        range(31, 61): "💪 进入核心词阶段！每个例句都试着背下来。",
        range(61, 91): "✍️ 现在可以试着用学过的词写2-3句话了。",
        range(91, 121):"🎯 冲刺阶段！每天做模拟练习，感受KET考试节奏。",
    }
    for r, tip in tips_map.items():
        if day in r:
            return tip
    return "💡 Keep going! 坚持就是胜利！"
