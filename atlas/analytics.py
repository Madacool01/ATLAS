"""per topic mastery math, multi topic questions count full points per topic."""  # yeah just saying what this file does
# yeah blank line, breathing room
# yeah one more, looks nicer
def _topic_totals(questions: dict, earned_map: dict) -> dict:  # little helper that adds up points per topic
    totals: dict = {}  # start empty, will collect earned and possible here
    for qid, q in questions.items():  # loop over every question we know
        earned = float(earned_map.get(qid, 0))  # how much was earned here, default zero if missing
        max_pts = float(q["max_points"])  # how much it was worth
        for topic in q["topics"]:  # same points count for each topic on this question
            entry = totals.setdefault(topic, {"earned": 0.0, "possible": 0.0})  # make a bucket for the topic if needed
            entry["earned"] += earned  # add what was earned
            entry["possible"] += max_pts  # add what was possible
    return totals  # ok hand the buckets back
# yeah blank line, split things up
# yeah keeps funcs from touching each other
def class_mastery(questions: dict, scores: dict) -> dict:  # hey this one does the whole class average per topic
    combined: dict = {}  # first we smash all students points together per question
    for sid_points in scores.values():  # go student by student
        for qid, pts in sid_points.items():  # go question by question
            combined[qid] = combined.get(qid, 0.0) + float(pts)  # just add it to the pile
    n_students = max(len(scores), 1)  # how many students, avoid divide by zero because why not
    totals: dict = {}  # fresh buckets for the class totals
    for qid, q in questions.items():  # again over every question
        earned = combined.get(qid, 0.0)  # total earned by everyone on this one
        for topic in q["topics"]:  # spread it to each topic it covers
            entry = totals.setdefault(topic, {"earned": 0.0, "possible": 0.0})  # make bucket if missing
            entry["earned"] += earned  # add class earned
            entry["possible"] += float(q["max_points"]) * n_students  # possible is max times num students
    return {t: (v["earned"] / v["possible"] * 100 if v["possible"] else 0.0) for t, v in totals.items()}  # turn it all into percents, safe if empty
# yeah blank line, you know the drill
# yeah another breather
def student_mastery(questions: dict, scores: dict) -> dict:  # hey this one does it per student instead
    out: dict = {}  # will hold one entry per student
    for sid, sid_points in scores.items():  # loop over students
        totals = _topic_totals(questions, sid_points)  # reuse the little helper from above
        out[sid] = {t: (v["earned"] / v["possible"] * 100 if v["possible"] else 0.0) for t, v in totals.items()}  # same percent math, just for this kid
    return out  # hand back the whole map
# yeah blank line, almost done
# yeah last gap before the tiny func
def weakest_topics(class_pct: dict) -> list:  # hey this one just sorts topics worst first
    return sorted(class_pct, key=lambda t: class_pct[t])  # lowest percent comes first, thats it
