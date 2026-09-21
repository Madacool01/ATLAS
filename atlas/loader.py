"""Load questions, scores, thresholds from CSV/JSON."""
import csv
import json


def load_questions(path: str) -> dict:
    questions: dict = {}
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            qid = row["question_id"].strip()
            max_points = float(row["max_points"])
            topics = [t.strip() for t in row["topics"].split(";") if t.strip()]
            questions[qid] = {"max_points": max_points, "topics": topics}
    return questions


def load_scores(path: str) -> tuple:
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        qids = [c for c in fieldnames if c != "student_id"]
        scores: dict = {}
        for row in reader:
            sid = row["student_id"].strip()
            scores[sid] = {qid: float(row[qid]) for qid in qids}
    return qids, scores


def load_thresholds(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return {"failed_below": float(data["failed_below"]), "needs_practice_below": float(data["needs_practice_below"])}
