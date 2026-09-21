"""per topic mastery math, multi topic questions count full points per topic."""
#eaYh just saying what this file does from loader import.

def _topic_totals(questions: dict, earned_map: dict) -> dict:  # little helper that adds up points per topic for one scoresheet
    totals: dict = {}  # start with an empty scoreboard, one slot per topic
    for qid, q in questions.items():  # walk through each question, like q1 then q2 then q3
        earned = float(earned_map.get(qid, 0))  # points the kid actually got here, zero if blank
        max_pts = float(q["max_points"])  # points the question was worth, like 10
        for topic in q["topics"]:  # a question can feed more than one topic, like q3 feeds both
            entry = totals.setdefault(topic, {"earned": 0.0, "possible": 0.0})  # grab the scoreboard row for this topic, make it if missing
            entry["earned"] += earned  # add what was scored, say plus 6
            entry["possible"] += max_pts  # add what was possible, say plus 10
    return totals  # hand back the scoreboard, like fractions 14 out of 20


def class_mastery(questions: dict, scores: dict) -> dict:  # this one averages the whole class per topic
    combined: dict = {}  # first add up everyone per question, like q1 total across all kids
    for sid_points in scores.values():  # go kid by kid
        for qid, pts in sid_points.items():  # go question by question inside that kid
            combined[qid] = combined.get(qid, 0.0) + float(pts)  # pile it on, say q1 goes 8 plus 4 plus 10 is 22
    n_students = max(len(scores), 1)  # how many kids, use 1 if empty so math never blows up
    totals: dict = {}  # fresh scoreboard, now for the whole class
    for qid, q in questions.items():  # again one question at a time
        earned = combined.get(qid, 0.0)  # class total on this question, like q3 is 22
        for topic in q["topics"]:  # copy that total into each topic it touches
            entry = totals.setdefault(topic, {"earned": 0.0, "possible": 0.0})  # grab the row for this topic, make it if missing
            entry["earned"] += earned  # add class scored points, say fractions gets plus 22 from q1
            entry["possible"] += float(q["max_points"]) * n_students  # add class possible, say 10 times 3 kids is 30
    return {t: (v["earned"] / v["possible"] * 100 if v["possible"] else 0.0) for t, v in totals.items()}  # turn scored over possible into percent, like 44 over 60 is 73 dot 3


def student_mastery(questions: dict, scores: dict) -> dict:  # hey this one runs the same math but separately per kid
    out: dict = {}  # will hold one mini report card per kid
    for sid, sid_points in scores.items():  # loop kids, like s01 then s02
        totals = _topic_totals(questions, sid_points)  # reuse the helper above on just this kid sheet
        out[sid] = {t: (v["earned"] / v["possible"] * 100 if v["possible"] else 0.0) for t, v in totals.items()}  # same divide scored by possible, like s01 fractions 14 over 20 is 70
    return out  # hand back all report cards


def weakest_topics(class_pct: dict) -> list:  # hey this one sorts topics so worst score comes first
    return sorted(class_pct, key=lambda t: class_pct[t])  # lowest percent first, so equations 70 comes before fractions 73

