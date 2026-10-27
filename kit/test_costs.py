import unittest

import costs

SAMPLE = """## 2026-10-25 12:15 UTC - Cycle (something)
- did a thing, cost=$9.99 in prose must not count
2026-10-25T12:15:24Z  cycle rc=0 cost=$0.42  log=logs/a.json
2026-10-25T18:13:00Z  cycle rc=1 cost=$0  log=logs/b.json
2026-10-26T06:57:37Z  daily-article rc=0  log=logs/c.json
2026-10-26T09:30:06Z  cycle rc=0 cost=$0.11000000000000001  log=logs/d.json
"""


class CostsTest(unittest.TestCase):
    def test_counts_only_cycle_lines(self):
        s = costs.summarize(SAMPLE)
        self.assertEqual(s, {"cycles": 3, "total": 0.53, "average": 0.18,
                             "min": 0.11, "max": 0.42, "free": 1})

    def test_empty_log(self):
        s = costs.summarize("")
        self.assertEqual((s["cycles"], s["total"], s["average"]), (0, 0.0, 0.0))

    def test_sentence(self):
        self.assertEqual(costs.sentence(costs.summarize(SAMPLE)),
                         "3 logged cycles, $0.53 total, $0.18 average, "
                         "$0.11-$0.42 range (1 of the 3 cost $0)")


if __name__ == "__main__":
    unittest.main()
