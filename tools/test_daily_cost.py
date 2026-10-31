import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import daily_cost

SAMPLE = """## 2026-10-30 09:00 UTC - Cycle
2026-10-30T09:00:00Z  cycle rc=0 cost=$0.40  log=x
2026-10-30T12:00:00Z  cycle rc=1 cost=$0.20  log=x
2026-10-30T13:00:00Z  daily-article rc=0  log=x
2026-10-31T03:00:00Z  cycle rc=0 cost=$0.50  log=x
"""


class DailyCostTest(unittest.TestCase):
    def test_groups_by_day_and_skips_articles(self):
        self.assertEqual(daily_cost.by_day(SAMPLE),
                         [("2026-10-30", 2, 0.6, 0.3), ("2026-10-31", 1, 0.5, 0.5)])

    def test_real_log_parses(self):
        log = pathlib.Path(__file__).parent.parent / "state" / "LOG.md"
        rows = daily_cost.by_day(log.read_text())
        self.assertTrue(rows)
        self.assertIn(rows[-1][0], daily_cost.report(rows))


if __name__ == "__main__":
    unittest.main()
