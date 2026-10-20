import unittest

from redirectcheck.parser import parse


class ParserTest(unittest.TestCase):
    def test_basic_rows_with_header(self):
        redirects, problems = parse("source,target\n/a,/b\n/c,https://x.com/d\n")
        self.assertEqual([(r.row, r.source, r.target) for r in redirects],
                         [(2, "/a", "/b"), (3, "/c", "https://x.com/d")])
        self.assertEqual(problems, [])

    def test_no_header_and_blank_lines(self):
        redirects, problems = parse("/a,/b\n\n /c , /d \n")
        self.assertEqual([(r.row, r.source, r.target) for r in redirects],
                         [(1, "/a", "/b"), (3, "/c", "/d")])
        self.assertEqual(problems, [])

    def test_malformed_rows(self):
        redirects, problems = parse("/a\n,/b\nold,/new\n/ok,/fine\n")
        self.assertEqual(len(redirects), 1)
        self.assertEqual([(p.kind, p.row) for p in problems],
                         [("malformed", 1), ("malformed", 2), ("malformed", 3)])


if __name__ == "__main__":
    unittest.main()
