import os
import unittest

import gonogo

HERE = os.path.dirname(os.path.abspath(__file__))


def metrics(signups=0, stars=0, forks=0, issues=0):
    return (f"- Stars: **{stars}**\n- Forks: **{forks}**\n- Open issues: **{issues}**\n"
            f"- Signups: **{signups}** of 50 target\n")


class GoNoGo(unittest.TestCase):
    def row(self, kit_post="unknown", **kw):
        return gonogo.decide(gonogo.parse(metrics(**kw)), kit_post)[0]

    def test_rows(self):
        self.assertEqual(self.row(signups=50), "50+ waitlist")
        self.assertEqual(self.row(signups=10), "10-49 waitlist")
        self.assertEqual(self.row(signups=9), "1-9 signals")
        self.assertEqual(self.row(stars=1), "1-9 signals")
        self.assertEqual(self.row(issues=1), "1-9 signals")

    def test_zero_depends_on_whether_a_post_went_out(self):
        self.assertEqual(self.row("yes"), "0 signals, kit post went out")
        self.assertEqual(self.row("no"), "0 signals, nothing went out")
        self.assertEqual(self.row("unknown"), "0 signals, post status unknown")

    def test_missing_line_fails_loudly(self):
        with self.assertRaises(ValueError):
            gonogo.parse("- Stars: **0**\n")

    def test_real_metrics_parse(self):
        with open(os.path.join(HERE, "..", "state", "METRICS.md")) as f:
            gonogo.parse(f.read())

    def test_rows_match_the_preregistered_table(self):
        with open(os.path.join(HERE, "..", "state", "GO-NO-GO-2026-10-29.md")) as f:
            table = f.read()
        for needle in ("50+ waitlist", "10-49 waitlist", "1-9 signals", "Kill the paid idea", "No verdict"):
            self.assertIn(needle, table)


if __name__ == "__main__":
    unittest.main()
