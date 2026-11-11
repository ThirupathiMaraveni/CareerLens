import unittest
from matcher import find_skills, analyze_match

class MatcherTests(unittest.TestCase):
    def test_detects_skills(self):
        found = find_skills("I use Python, SQL and machine learning.")
        self.assertEqual(found, {"python", "sql", "machine learning"})

    def test_match_and_gap(self):
        result = analyze_match(
            "Python developer with SQL and Pandas experience.",
            "Python intern. Required: Python, SQL, Pandas and Flask."
        )
        self.assertEqual(set(result["matched_skills"]), {"python", "sql", "pandas"})
        self.assertEqual(result["missing_skills"], ["flask"])
        self.assertGreaterEqual(result["similarity"], 0)

    def test_empty_input_rejected(self):
        with self.assertRaises(ValueError):
            analyze_match("", "Python intern")

if __name__ == "__main__":
    unittest.main()
