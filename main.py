from atlas.loader import *
from atlas.analytics import *
from atlas.report import *

questions = load_questions("data/example1/questions.csv")
_, s = load_scores("data/example1/scores.csv")
print(class_mastery(questions, s))