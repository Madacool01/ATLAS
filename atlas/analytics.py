def topic_totals(questions: dict, earned_map: dict) -> dict:  # helper that adds up points per topic for one scoresheet
    totals: dict = {}  # start with an empty scoreboard, one slot per topic
    for qid, q in questions.items():  # walk through each question, like q1 then q2 then q3
        earned = float(earned_map.get(qid, 0))
        max_pts = float(q["max_points"])
        for topic in q["topics"]:  # a question can feed more than one topic so we loop through all
            entry = totals.setdefault(topic, {"earned": 0.0, "possible": 0.0})
            entry["earned"] += earned
            entry["possible"] += max_pts
    return totals


def class_mastery(questions: dict, scores: dict) -> dict:  # averages the whole class per topic
    combined: dict = {}  # add up everyone per question in this dict.
    for sid_points in scores.values(): #sid = student id
        for qid, pts in sid_points.items():  # go question by question inside that student
            combined[qid] = combined.get(qid, 0.0) + float(pts)  # add the point to the assigned question
    n_students = max(len(scores), 1)
    totals: dict = {}  # for the whole class per topic
    for qid, q in questions.items():  # one question at a time
        earned = combined.get(qid, 0.0)  # class total on this question
        for topic in q["topics"]:  # copy that total into each topic it touches
            entry = totals.setdefault(topic, {"earned": 0.0, "possible": 0.0})  # grab the row for this topic, make it if missing
            entry["earned"] += earned  # add class scored points, say fractions gets plus 22 from q1
            entry["possible"] += float(q["max_points"]) * n_students  # add class possible, say 10 times 3 kids is 30
    return {t: (v["earned"] / v["possible"] * 100 if v["possible"] else 0.0) for t, v in totals.items()}  # turn scored over possible into percents.


def student_mastery(questions: dict, scores: dict) -> dict:  #same math but separately per kid
    out: dict = {}  # will hold one mini report card per kid
    for sid, sid_points in scores.items():  # loop students, like s01 then s02
        totals = topic_totals(questions, sid_points)  # reuse the helper above on just this student sheet
        out[sid] = {t: (v["earned"] / v["possible"] * 100 if v["possible"] else 0.0) for t, v in totals.items()}  # same divide scored by possible, like s01 fractions 14 over 20 is 70
    return out


def weakest_topics(class_pct: dict) -> list:  # sorts topics so worst score comes first
    return sorted(class_pct, key=lambda t: class_pct[t])  # lowest percent first, so equations 70 comes before fractions 73

