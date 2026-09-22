import unittest  # grab the built in test stuff

from atlas.report import label_for, render_text  # pull in the two report funcs


class TestReport(unittest.TestCase):  # yeah our little test box for the report
    def test_labels_use_teacher_thresholds(self):  # hey this checks labels follow teacher cutoffs
        th = {"failed_below": 50, "needs_practice_below": 75}  # fake cutoffs, failed under fifty
        self.assertEqual(label_for(40, th), "failed")  # forty is below fifty so failed
        self.assertEqual(label_for(70, th), "needs practice")  # seventy is in the middle zone
        self.assertEqual(label_for(80, th), "solid")  # eighty is above seventy five so solid

    def test_render_contains_weakest(self):  # hey this checks the text has the weak stuff
        class_pct = {"Fractions": 73.33, "Equations": 70.0}  # fake class averages
        per_student = {"S01": {"Fractions": 70.0, "Equations": 55.0}}  # fake one kid card
        th = {"failed_below": 50, "needs_practice_below": 75}  # same fake cutoffs
        text = render_text(class_pct, per_student, th, ["Equations", "Fractions"])  # render worst first
        self.assertIn("Equations", text)  # weakest topic should show up
        self.assertIn("70.0%", text)  # weakest percent should show up
        self.assertIn("weakest", text.lower())  # should say weakest somewhere


if __name__ == "__main__":  # only runs when you run this file directly
    unittest.main()  # kick off the tests, let it do its thing
