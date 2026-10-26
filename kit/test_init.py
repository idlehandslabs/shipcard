import pathlib
import re
import shutil
import tempfile
import unittest

import init

HERE = pathlib.Path(__file__).parent


class InitTest(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        shutil.copy(HERE / "CLAUDE.md", self.tmp / "CLAUDE.md")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_fills_every_placeholder(self):
        init.main(["--name", "Acme", "--budget", "50", "--root", str(self.tmp)])
        text = (self.tmp / "CLAUDE.md").read_text()
        self.assertNotIn("{{", text)
        self.assertIn("# Acme", text)
        self.assertIn("$50", text)

    def test_creates_state_and_keeps_existing(self):
        (self.tmp / "state").mkdir()
        (self.tmp / "state" / "LOG.md").write_text("mine")
        init.main(["--name", "Acme", "--root", str(self.tmp)])
        self.assertEqual((self.tmp / "state" / "LOG.md").read_text(), "mine")
        self.assertIn("Total: $100", (self.tmp / "state" / "BUDGET.md").read_text())
        self.assertTrue((self.tmp / "post-queue" / "published").is_dir())

    def test_rules_survive(self):
        init.main(["--name", "Acme", "--root", str(self.tmp)])
        text = (self.tmp / "CLAUDE.md").read_text()
        self.assertIn("NEVER post, publish, or send anything yourself", text)

    def test_bad_budget_rejected(self):
        with self.assertRaises(SystemExit):
            init.main(["--name", "A", "--budget", "1;rm", "--root", str(self.tmp)])

    def test_demo_lists_the_real_state_files(self):
        demo = (HERE / "DEMO.md").read_text()
        listed = set(re.findall(r"^    state/(\w+\.md)$", demo, re.M))
        self.assertEqual(listed, set(init.STATE_FILES))

    def test_docs_only_use_real_flags(self):
        real = set(re.findall(r'add_argument\("(--[a-z]+)"', (HERE / "init.py").read_text()))
        for doc in ("README.md", "DEMO.md"):
            for line in (HERE / doc).read_text().splitlines():
                if "init.py" in line or "--voice" in line:
                    for flag in re.findall(r"(?<![\w-])--[a-z]+", line):
                        self.assertIn(flag, real, f"{doc} uses unknown flag {flag}")

    def test_license_present_and_named_in_readme(self):
        self.assertIn("MIT License", (HERE / "LICENSE").read_text())
        self.assertIn("`LICENSE`", (HERE / "README.md").read_text())

    def test_docs_skip_files_the_sync_drops(self):
        # The founder-kit repo copies kit/ minus workflow/ and EXTRACT.md
        # (the workflow lands at .github/workflows/agent.yml instead).
        for doc in ("README.md", "DEMO.md"):
            text = (HERE / doc).read_text()
            self.assertNotRegex(text, r"(?<![./\w])workflow/agent\.yml", doc)
            self.assertNotIn("EXTRACT.md", text, doc)

    def test_readme_test_count_is_real(self):
        loader = unittest.TestLoader()
        own = loader.discover(str(HERE), pattern="test_*.py", top_level_dir=str(HERE))
        agent = loader.discover(str(HERE / "agent"), pattern="test_*.py",
                                top_level_dir=str(HERE / "agent"))
        n_own, n_agent = own.countTestCases(), agent.countTestCases()
        m = re.search(r"## Tests \((\d+): (\d+) setup/docs \+ (\d+) agent\)",
                      (HERE / "README.md").read_text())
        self.assertIsNotNone(m, "README Tests heading lost its count")
        self.assertEqual((int(m[1]), int(m[2]), int(m[3])),
                         (n_own + n_agent, n_own, n_agent))
        # Any other "all N tests" claim must also be today's number.
        for n in re.findall(r"all (\d+) tests", (HERE / "README.md").read_text()):
            self.assertEqual(int(n), n_own + n_agent, f"README says 'all {n} tests'")

    def test_readme_schedule_matches_workflow(self):
        # kit/workflow/ here; .github/workflows/ in the standalone founder-kit repo.
        wf = next(p for p in (HERE / "workflow" / "agent.yml",
                              HERE / ".github" / "workflows" / "agent.yml") if p.exists())
        crons = re.findall(r'cron: "([^"]+)"', wf.read_text())
        self.assertEqual(crons, ["0 */6 * * *", "15 6 * * *"],
                         "workflow schedule changed; update README 'Schedule, pause, stop'")

    def test_readme_explains_every_workflow_secret(self):
        wf = next(p for p in (HERE / "workflow" / "agent.yml",
                              HERE / ".github" / "workflows" / "agent.yml") if p.exists())
        readme = (HERE / "README.md").read_text()
        for name in set(re.findall(r"secrets\.([A-Z_]+)", wf.read_text())):
            self.assertIn(f"`{name}`", readme, f"README never tells users to add {name}")
        self.assertIn("claude setup-token", readme, "README must say how to get the OAuth token")


if __name__ == "__main__":
    unittest.main()
