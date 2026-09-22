"""cli so you can run python minus m atlas dot cli on a data folder."""  # yeah just saying what this file is about
import argparse  # grab argparse so cli flags are easy
import pathlib  # grab pathlib so folder paths are easy

from analytics import class_mastery, student_mastery, weakest_topics  # pull in the math funcs
from loader import load_questions, load_scores, load_thresholds  # pull in the loader funcs
from report import render_text  # pull in the text renderer


def main():  # hey this one runs the whole report from the command line
    parser = argparse.ArgumentParser(description="ATLAS Slice-1 topic report")  # make the arg parser with a tagline
    parser.add_argument("data_dir", help="folder with questions.csv, scores.csv")  # first arg is the data folder
    parser.add_argument("--thresholds", default=None, help="path to thresholds.json")  # optional override for thresholds file
    args = parser.parse_args()  # read what the teacher typed
    base = pathlib.Path(args.data_dir)  # turn the folder string into a path
    questions = load_questions(str(base / "questions.csv"))  # load the questions file
    _, scores = load_scores(str(base / "scores.csv"))  # load the scores, ignore the qid list
    th_path = args.thresholds or str(base / "thresholds.json")  # use override or default thresholds file
    thresholds = load_thresholds(th_path)  # load the teacher cutoffs
    class_pct = class_mastery(questions, scores)  # run the class math
    per_student = student_mastery(questions, scores)  # run the per kid math
    order = weakest_topics(class_pct)  # sort worst first
    print(render_text(class_pct, per_student, thresholds, order), end="")  # print it, no extra newline


if __name__ == "__main__":  # only runs when you run this file directly
    main()  # kick it off
