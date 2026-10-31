import contextlib
import io
import pathlib
import re
import shutil
import tempfile
import unittest

import costs
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

    def test_prints_next_steps(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            init.main(["--name", "Acme", "--root", str(self.tmp)])
        text = out.getvalue()
        self.assertIn("git push", text)
        self.assertNotIn("Warning", text)
        for secret in ("CLAUDE_CODE_OAUTH_TOKEN", "PRIVATE_TERMS"):
            self.assertIn(secret, text)
        # DEMO.md quotes the printout; it must match what init.py really prints.
        self.assertIn(init.NEXT_STEPS.splitlines()[0], (HERE / "DEMO.md").read_text())

    def test_warns_on_leftover_placeholders(self):
        (self.tmp / "CLAUDE.md").write_text("Run {{COMPANY_NAME}}; also {{CUSTOM_THING}}.\n")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            init.main(["--name", "Acme", "--root", str(self.tmp)])
        self.assertIn("still has placeholders: CUSTOM_THING", out.getvalue())

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

    def test_tried_it_issue_template(self):
        # The founder-kit repo's first outside signal; README must point at it.
        tpl = (HERE / ".github" / "ISSUE_TEMPLATE" / "tried-it.md").read_text()
        self.assertTrue(tpl.startswith("---\nname: I tried it\n"))
        self.assertIn("python3 costs.py state/LOG.md", tpl)
        readme = (HERE / "README.md").read_text()
        self.assertIn('"I tried it" issue', readme)
        # Direct link + blank-issue fallback, in case the sync skips kit/.github/.
        self.assertIn("founder-kit/issues/new?template=tried-it.md", readme)
        self.assertIn("a blank issue is fine", readme)

    def test_readme_cost_line_is_self_consistent(self):
        # Caught 2026-10-28: "55 logged cycles" next to "2 of the 50".
        readme = (HERE / "README.md").read_text()
        cycles = re.search(r"(\d+) logged cycles", readme).group(1)
        found = re.findall(r"of the (\d+) ", readme)
        self.assertTrue(found)
        self.assertEqual(set(found), {cycles}, "README cost line disagrees with itself")

    def test_readme_monthly_cost_matches_its_average(self):
        # The monthly figure must follow from the average the README quotes.
        readme = (HERE / "README.md").read_text()
        avg = float(re.search(r"\$([0-9.]+) average", readme).group(1))
        month = re.search(r"about \$([0-9.]+) a month", readme).group(1)
        self.assertEqual(float(month), costs.monthly({"average": avg}))

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

    def test_readme_says_who_it_is_not_for(self):
        readme = (HERE / "README.md").read_text()
        self.assertIn("## Is this for you?", readme)
        section = readme.split("## Is this for you?", 1)[1].split("\n## ", 1)[0]
        self.assertIn("Not a fit:", section)
        # Honest about money: the only revenue claim is the real $0.
        self.assertIn("$0", section)
        self.assertLess(readme.index("## Is this for you?"), readme.index("## Setup"))

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

    def test_readme_explains_every_state_file(self):
        readme = (HERE / "README.md").read_text()
        missing = [f for f in init.STATE_FILES if f"`{f}`" not in readme]
        self.assertEqual(missing, [], f"README never explains: {missing}")

    def test_readme_failure_messages_match_scripts(self):
        # The troubleshooting section quotes real output; fail if the scripts' wording drifts.
        readme = (HERE / "README.md").read_text()
        capture = (HERE / "agent" / "capture.py").read_text()
        guard = (HERE / "agent" / "guard.py").read_text()
        cycle = (HERE / "agent" / "run-cycle.sh").read_text()
        self.assertIn("## When a cycle fails", readme)
        for msg, src in (("Run failed", capture), ("Blocked by a guardrail", capture),
                         ("PUSH BLOCKED by guard.py", guard),
                         ("NOT RUN: CLAUDE.md still has", cycle)):
            self.assertIn(msg, src, f"{msg!r} no longer printed by the scripts")
            self.assertIn(msg, readme, f"README doesn't explain {msg!r}")

    def test_readme_pre_push_hook_calls_real_guard(self):
        # The standalone-hook snippet must point at the real script and its real usage.
        readme = (HERE / "README.md").read_text()
        guard = (HERE / "agent" / "guard.py").read_text()
        self.assertIn("## Use guard.py on its own", readme)
        self.assertIn("exec python3 agent/guard.py", readme)
        self.assertIn("Usage: guard.py <base_commit>", guard)


if __name__ == "__main__":
    unittest.main()
