import os
import unittest

from check_post import problems

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class CheckPostTest(unittest.TestCase):
    def test_plain_update_passes(self):
        self.assertEqual(problems("# note for operator\nDay 30. $0 revenue. 0 orders. Fixed my own rule-break."), [])

    def test_each_rule_fires(self):
        self.assertIn("link", problems("see https://example.org"))
        self.assertIn("DM ask", problems("DM me the scope"))
        self.assertIn("payment ask", problems("only 99 USDC"))
        self.assertIn("wallet address", problems("to 9xQeWvG816bUx9EPjHmaT23yvVM2ZWbrrpZb9PusVFin"))
        self.assertTrue(any("chars" in p for p in problems("a" * 300)))
        self.assertEqual(problems("# only notes"), ["empty post"])

    def test_yesterdays_reply_bank_is_caught(self):
        # 2026-11-17-0951.md broke the 11-16 rules; the checker must say so.
        with open(os.path.join(ROOT, "post-queue", "2026-11-17-0951.md"), encoding="utf-8") as f:
            found = problems(f.read())
        self.assertIn("payment ask", found)
        self.assertIn("DM ask", found)


if __name__ == "__main__":
    unittest.main()
