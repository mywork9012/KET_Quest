"""
4个月（120天）KET备考计划模块
核心修复：
  - 今日新词基于"用户已学到第几个"，而非日期偏移
  - 学完每日配额后可继续学下一批，不强制截断
"""

from datetime import date
from utils.db import load_words, get_all_progress

STAGES = [
    {"name": "第一阶段", "days": (1, 30),   "label": "基础衔接",
     "desc": "过KET基础衔接词 + 入门例句，建立语感",
     "new_per_day": 8,  "color": "#4ECDC4"},
    {"name": "第二阶段", "days": (31, 60),  "label": "核心积累",
     "desc": "主攻KET核心高频词 + 常规KET例句，大量积累搭配",
     "new_per_day": 10, "color": "#45B7D1"},
    {"name": "第三阶段", "days": (61, 90),  "label": "二轮复习",
     "desc": "全词二轮复习 + 例句仿写训练 + 固定搭配专项",
     "new_per_day": 8,  "color": "#96CEB4"},
    {"name": "第四阶段", "days": (91, 120), "label": "冲刺闯关",
     "desc": "真题词汇复盘 + 例句句型整合 + 模拟闯关自测",
     "new_per_day": 6,  "color": "#FFEAA7"},
]


def get_stage(day: int) -> dict:
    for s in STAGES:
        lo, hi = s["days"]
        if lo <= day <= hi:
            return s
    return STAGES[-1]


def get_today_plan(username: str, start_date_str: str) -> dict:
    """
    计算今日学习计划。
    核心逻辑：
      - 找出所有"未接触"的单词（status=new，即从未学过的）
      - 取前 new_per_day 个作为今日推荐新词
      - 这样随着孩子学习进度自动向后推进，不会重复
    """
    start = date.fromisoformat(start_date_str)
    day = max(1, min((date.today() - start).days + 1, 120))
    stage = get_stage(day)
    new_per_day = stage["new_per_day"]

    all_words = load_words()
    progress = get_all_progress(username)

    # 未接触的词（从未出现在 word_progress 表中）
    unseen = [w for w in all_words if w["id"] not in progress]

    # 今日推荐新词：按词库顺序取前 new_per_day 个
    today_new = unseen[:new_per_day]

    # 如果全部学完了，今日新词为空
    all_done = len(unseen) == 0

    return {
        "day": day,
        "days_left": max(0, 120 - day),
        "stage": stage,
        "new_words": today_new,          # 今日推荐批次（8~10个）
        "new_count": len(today_new),
        "unseen_total": len(unseen),     # 总剩余未学词数
        "all_done": all_done,
        "tips": _get_tips(day),
    }


def get_next_batch(username: str, batch_size: int = 10) -> list:
    """
    获取下一批未学单词（用于学完今日配额后"继续学"）
    跳过已出现在 word_progress 的词
    """
    all_words = load_words()
    progress = get_all_progress(username)
    unseen = [w for w in all_words if w["id"] not in progress]
    return unseen[:batch_size]


def get_free_study_words(username: str, count: int = 20) -> list:
    """
    自由练习模式：混合返回学习中 + 少量未见词
    优先复习 learning 状态的词，补充新词
    """
    all_words = load_words()
    progress = get_all_progress(username)

    learning = [w for w in all_words
                if progress.get(w["id"], {}).get("status") == "learning"]
    unseen   = [w for w in all_words if w["id"] not in progress]

    # 70% 复习中 + 30% 新词
    review_count = min(len(learning), int(count * 0.7))
    new_count    = count - review_count

    import random
    selected = random.sample(learning, review_count) if learning else []
    selected += unseen[:new_count]
    random.shuffle(selected)
    return selected


def _get_tips(day: int) -> str:
    tips = [
        (range(1,  8),  "🌱 第一周！先把每个单词大声读3遍，跟着例句朗读。"),
        (range(8,  15), "📖 坚持一周了！尝试用单词造句，哪怕很简单也好。"),
        (range(15, 31), "🔄 做完新词再回头复习前面的，记忆更牢固！"),
        (range(31, 61), "💪 进入核心词阶段！每个例句都试着背下来。"),
        (range(61, 91), "✍️ 现在可以试着用学过的词写2~3句话了。"),
        (range(91, 121),"🎯 冲刺阶段！每天做模拟练习，感受KET考试节奏。"),
    ]
    for r, tip in tips:
        if day in r:
            return tip
    return "💡 Keep going! 坚持就是胜利！"
