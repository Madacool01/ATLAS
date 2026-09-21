"""load questions, scores, thresholds from csv and json."""  # yeah just saying what this file is about
import csv  # grab csv helper so we can read spreadsheet files
import json  # grab json helper so we can read the thresholds file
# yeah blank line, just breathing room
# yeah another one, keeps things readable
def load_questions(path: str) -> dict:  # hey this one loads the questions file
    questions: dict = {}  # start empty, will fill it up below
    with open(path, newline="", encoding="utf-8") as f:  # open the file nicely so csv is happy
        reader = csv.DictReader(f)  # read it as rows you can access by name
        for row in reader:  # go through each question one by one
            qid = row["question_id"].strip()  # grab the id and clean up extra spaces
            max_points = float(row["max_points"])  # grab max points and make it a number
            topics = [t.strip() for t in row["topics"].split(";") if t.strip()]  # split topics by semicolon and clean them
            questions[qid] = {"max_points": max_points, "topics": topics}  # stash it away in our little dict
    return questions  # ok done, hand it back
# yeah blank line, separating the next bit
# yeah keeps the file from looking cramped
def load_scores(path: str) -> tuple:  # hey this one loads who got what points
    with open(path, newline="", encoding="utf-8") as f:  # same deal, open it nicely
        reader = csv.DictReader(f)  # again rows by name, super handy
        fieldnames = reader.fieldnames or []  # grab the header row so we know the question ids
        qids = [c for c in fieldnames if c != "student_id"]  # everything except student id is a question
        scores: dict = {}  # start empty, fill with students in a sec
        for row in reader:  # one row per student here
            sid = row["student_id"].strip()  # grab the alias and clean it
            scores[sid] = {qid: float(row[qid]) for qid in qids}  # turn all their points into numbers
    return qids, scores  # hand back both the question list and the scores
# yeah blank line again, same reason
# yeah last breather before the last func
def load_thresholds(path: str) -> dict:  # hey this one loads the teacher cutoffs
    with open(path, encoding="utf-8") as f:  # open the little json file
        data = json.load(f)  # parse it into a dict, easy
    return {"failed_below": float(data["failed_below"]), "needs_practice_below": float(data["needs_practice_below"])}  # just keep the two numbers we care about
