import pathlib  # need this to build file paths without pain
import unittest  # grab the built in test stuff
# yeah blank line, keep imports apart from the rest
from atlas.loader import load_questions, load_scores, load_thresholds  # pull in our three loader funcs
# yeah blank line, breathing room
# yeah one more, looks clean
class TestLoader(unittest.TestCase):  # yeah our little test box for the loader
    def test_loads_example1(self):  # hey this checks the example files load right
        base = pathlib.Path("data/example1")  # point at the example folder
        questions = load_questions(str(base / "questions.csv"))  # load the questions file
        self.assertEqual(questions["Q1"]["max_points"], 10)  # q1 should be worth ten, sanity check
        self.assertEqual(questions["Q1"]["topics"], ["Fractions"])  # q1 should be fractions only
        self.assertEqual(questions["Q3"]["topics"], ["Fractions", "Equations"])  # q3 covers both, check the split worked
        qids, scores = load_scores(str(base / "scores.csv"))  # load the scores file next
        self.assertEqual(qids, ["Q1", "Q2", "Q3"])  # should have found these three questions
        self.assertEqual(scores["S01"]["Q1"], 8)  # s01 got eight on q1 in our fake data
        thresholds = load_thresholds(str(base / "thresholds.json"))  # load the teacher cutoffs
        self.assertEqual(thresholds["failed_below"], 50)  # failed should kick in below fifty
        self.assertEqual(thresholds["needs_practice_below"], 75)  # practice zone should end at seventy five
# yeah blank line, gap before the runner bit
# yeah keeps it tidy
if __name__ == "__main__":  # only runs when you run this file directly
    unittest.main()  # kick off the tests, let it do its thing
