import csv  # grab csv helper so we can read spreadsheet files
import json  # grab json helper so we can read the thresholds file

def load_questions(path: str) -> dict:  # loads the questions file
    questions: dict = {}  # start empty, will fill it up below
    with open(path, newline="", encoding="utf-8") as f:  # open the file
        reader = csv.DictReader(f)  # read it as rows you can access by name
        for row in reader:  # go through each question one by one
            qid = row["question_id"].strip()  # grab the id and clean up extra spaces
            max_points = float(row["max_points"])  # grab max points and make it a number
            topics = [t.strip() for t in row["topics"].split(";") if t.strip()]  # split topics by semicolon and clean them
            questions[qid] = {"max_points": max_points, "topics": topics}  #store it in the dictionarz
    return questions


def load_scores(path: str) -> tuple:  # loads points of students
    with open(path, newline="", encoding="utf-8") as f:  # open the scoresheet
        reader = csv.DictReader(f)  #
        fieldnames = reader.fieldnames or []  # grab the header row so we know the question ids
        qids = [c for c in fieldnames if c != "student_id"]  # everything except student id is a question
        scores: dict = {}
        for row in reader:  # one row per student
            sid = row["student_id"].strip()  # grab the alias and clean it
            scores[sid] = {qid: float(row[qid]) for qid in qids}  # turn all their points into numbers
    return qids, scores  # question list and the scores


def load_thresholds(path: str) -> dict:  # teacher's thresholds
    with open(path, encoding="utf-8") as f:  # open the little json file
        data = json.load(f) #dict
    return {"failed_below": float(data["failed_below"]), "needs_practice_below": float(data["needs_practice_below"])}  
