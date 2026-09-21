import unittest

from atlas.analytics import class_mastery, student_mastery, weakest_topics


def sample():
    questions = {
        "Q1": {"max_points": 10, "topics": ["Fractions"]},
        "Q2": {"max_points": 10, "topics": ["Equations"]},
        "Q3": {"max_points": 10, "topics": ["Fractions", "Equations"]},
    }
    scores = {
        "S01": {"Q1": 8, "Q2": 5, "Q3": 6},
        "S02": {"Q1": 4, "Q2": 9, "Q3": 7},
        "S03": {"Q1": 10, "Q2": 6, "Q3": 9},
    }
    return questions, scores


class TestAnalytics(unittest.TestCase):
    def test_class_mastery(self):
        questions, scores = sample()
        result = class_mastery(questions, scores)
        # Fractions: earned (8+6)+(4+7)+(10+9)=44, possible 3*20=60 -> 73.33
        # Equations: earned (5+6)+(9+7)+(6+9)=42, possible 60 -> 70.0
        self.assertAlmostEqual(result["Fractions"], 73.333, places=2)
        self.assertAlmostEqual(result["Equations"], 70.0, places=2)

    def test_student_mastery(self):
        questions, scores = sample()
        result = student_mastery(questions, scores)
        # S01 Fractions: (8+6)/20=70.0, Equations: (5+6)/20=55.0
        self.assertAlmostEqual(result["S01"]["Fractions"], 70.0, places=2)
        self.assertAlmostEqual(result["S01"]["Equations"], 55.0, places=2)

    def test_weakest_sorted(self):
        self.assertEqual(weakest_topics({"Fractions": 73.3, "Equations": 70.0}), ["Equations", "Fractions"])


if __name__ == "__main__":
    unittest.main()
