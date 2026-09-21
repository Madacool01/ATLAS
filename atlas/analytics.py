"""Per-topic mastery math. Multi-topic questions count full points per topic."""


def _topic_totals(questions: dict, earned_map: dict) -> dict:
    totals: dict = {}
    for qid, q in questions.items():
        earned = float(earned_map.get(qid, 0))
        max_pts = float(q["max_points"])
        for topic in q["topics"]:
            entry = totals.setdefault(topic, {"earned": 0.0, "possible": 0.0})
            entry["earned"] += earned
            entry["possible"] += max_pts
    return totals


def class_mastery(questions: dict, scores: dict) -> dict:
    combined: dict = {}
    for sid_points in scores.values():
        for qid, pts in sid_points.items():
            combined[qid] = combined.get(qid, 0.0) + float(pts)
    n_students = max(len(scores), 1)
    totals: dict = {}
    for qid, q in questions.items():
        earned = combined.get(qid, 0.0)
        for topic in q["topics"]:
            entry = totals.setdefault(topic, {"earned": 0.0, "possible": 0.0})
            entry["earned"] += earned
            entry["possible"] += float(q["max_points"]) * n_students
    return {t: (v["earned"] / v["possible"] * 100 if v["possible"] else 0.0) for t, v in totals.items()}


def student_mastery(questions: dict, scores: dict) -> dict:
    out: dict = {}
    for sid, sid_points in scores.items():
        totals = _topic_totals(questions, sid_points)
        out[sid] = {t: (v["earned"] / v["possible"] * 100 if v["possible"] else 0.0) for t, v in totals.items()}
    return out


def weakest_topics(class_pct: dict) -> list:
    return sorted(class_pct, key=lambda t: class_pct[t])
