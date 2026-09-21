import pathlib
import unittest

from atlas.loader import load_questions, load_scores, load_thresholds


class TestLoader(unittest.TestCase):
    def test_loads_example1(self):
        base = pathlib.Path("data/example1")
        questions = load_questions(str(base / "questions.csv"))
        self.assertEqual(questions["Q1"]["max_points"], 10)
        self.assertEqual(questions["Q1"]["topics"], ["Fractions"])
        self.assertEqual(questions["Q3"]["topics"], ["Fractions", "Equations"])
        qids, scores = load_scores(str(base / "scores.csv"))
        self.assertEqual(qids, ["Q1", "Q2", "Q3"])
        self.assertEqual(scores["S01"]["Q1"], 8)
        thresholds = load_thresholds(str(base / "thresholds.json"))
        self.assertEqual(thresholds["failed_below"], 50)
        self.assertEqual(thresholds["needs_practice_below"], 75)


if __name__ == "__main__":
    unittest.main()
