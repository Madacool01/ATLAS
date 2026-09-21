import unittest  # grab the built in test stuff
# yeah blank line, breathing room
from atlas.analytics import class_mastery, student_mastery, weakest_topics  # pull in the three math funcs
# yeah blank line, keep things airy
# yeah one more for looks
def sample():  # hey this just makes fake data so we dont need files here
    questions = {  # tiny fake question set, three questions
        "Q1": {"max_points": 10, "topics": ["Fractions"]},  # q1 is fractions only
        "Q2": {"max_points": 10, "topics": ["Equations"]},  # q2 is equations only
        "Q3": {"max_points": 10, "topics": ["Fractions", "Equations"]},  # q3 covers both, the spicy one
    }  # ok questions done
    scores = {  # tiny fake scores for three kids
        "S01": {"Q1": 8, "Q2": 5, "Q3": 6},  # s01 did ok on q1, meh on the rest
        "S02": {"Q1": 4, "Q2": 9, "Q3": 7},  # s02 flipped it, rough on q1
        "S03": {"Q1": 10, "Q2": 6, "Q3": 9},  # s03 is vibing, solid almost everywhere
    }  # ok scores done
    return questions, scores  # hand both back to whoever called
# yeah blank line, split helper from tests
# yeah breathing room again
class TestAnalytics(unittest.TestCase):  # yeah our little test box for the math
    def test_class_mastery(self):  # hey this checks the class averages are right
        questions, scores = sample()  # grab the fake data
        result = class_mastery(questions, scores)  # run the class math
        # yeah fractions math worked out on paper, trust it
        # yeah equations math too, same deal
        self.assertAlmostEqual(result["Fractions"], 73.333, places=2)  # fractions should land around here
        self.assertAlmostEqual(result["Equations"], 70.0, places=2)  # equations should land bang on seventy
    def test_student_mastery(self):  # hey this checks one kid in detail
        questions, scores = sample()  # same fake data again
        result = student_mastery(questions, scores)  # run the per kid math
        # yeah s01 fractions is eight plus six over twenty, equations is five plus six over twenty
        self.assertAlmostEqual(result["S01"]["Fractions"], 70.0, places=2)  # s01 fractions should be seventy
        self.assertAlmostEqual(result["S01"]["Equations"], 55.0, places=2)  # s01 equations should be fifty five
    def test_weakest_sorted(self):  # hey this checks worst first sorting
        self.assertEqual(weakest_topics({"Fractions": 73.3, "Equations": 70.0}), ["Equations", "Fractions"])  # equations is lower so it should come first
# yeah blank line, gap before runner
# yeah last breather
if __name__ == "__main__":  # only runs when you run this file directly
    unittest.main()  # kick off the tests, let it do its thing
