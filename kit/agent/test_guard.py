import os
import pathlib
import subprocess
import tempfile
import unittest

GUARD = pathlib.Path(__file__).parent / "guard.py"
GIT = ["git", "-c", "user.name=t", "-c", "user.email=t@users.noreply.github.com"]


def run(cwd, *args, env=None):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, env=env)


class GuardTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        run(self.tmp, "git", "init", "-q")
        (pathlib.Path(self.tmp) / "a.txt").write_text("hello\n")
        run(self.tmp, *GIT, "add", "-A")
        run(self.tmp, *GIT, "commit", "-qm", "base")

    def commit(self, name, text):
        path = pathlib.Path(self.tmp) / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        run(self.tmp, *GIT, "add", "-A")
        run(self.tmp, *GIT, "commit", "-qm", "change")

    def guard(self, terms=""):
        env = {**os.environ, "PRIVATE_TERMS": terms}
        return run(self.tmp, "python3", str(GUARD), "HEAD~1", env=env)

    def test_clean_diff_passes(self):
        self.commit("b.txt", "nothing to see\n")
        self.assertEqual(self.guard().returncode, 0)

    def test_blocks_secret(self):
        # built by concatenation so this test file doesn't trip the guard itself
        self.commit("b.txt", "key = AKIA" + "ABCDEFGHIJKLMNOP\n")
        r = self.guard()
        self.assertEqual(r.returncode, 1)
        self.assertIn("AWS key", r.stdout)

    def test_blocks_common_key_formats(self):
        # formats agents often paste into code; concatenated so this file stays clean
        for name, text in [
            ("OpenAI key", "OPENAI = 'sk-" + "proj-abcdefghijklmnopqrstuvwx'"),
            ("Stripe live key", "stripe = sk_" + "live_abcdefghijklmnopqrstuvwx"),
            ("Google API key", "maps=AI" + "za" + "A" * 35),
        ]:
            with self.subTest(name=name):
                self.setUp()
                self.commit("b.txt", text + "\n")
                r = self.guard()
                self.assertEqual(r.returncode, 1, r.stdout)
                self.assertIn(name, r.stdout)

    def test_blocks_tokens_and_db_urls(self):
        for name, text in [
            ("Hugging Face token", "HF = 'hf" + "_" + "a" * 34 + "'"),
            ("npm token", "//registry/:_authToken=npm" + "_" + "b" * 36),
            ("Database URL with password", "DB = 'postgres" + "://app:hunter22@db.example.com/prod'"),
            ("Telegram bot token", "BOT = '123456789" + ":AA" + "c" * 33 + "'"),
            ("SendGrid key", "SG" + "." + "d" * 22 + "." + "e" * 43),
            ("Twilio API key", "TWILIO = 'SK" + "0123456789abcdef" * 2 + "'"),
            ("Mailgun key", "MG = 'key" + "-" + "fedcba9876543210" * 2 + "'"),
            ("Mailgun key", "MAILGUN_API_KEY = '" + "0123456789abcdef" * 2 + "-1a2b3c4d" + "-5e6f7a8b'"),
            ("GitLab token", "GL = 'glpat" + "-" + "h" * 20 + "'"),
            ("Shopify token", "SHOP = 'shpat" + "_" + "0123456789abcdef" * 2 + "'"),
            ("PyPI token", "TWINE_PASSWORD = 'pypi" + "-" + "AgEIcHlwaS5vcmc" + "Ab1_-" * 12 + "'"),
            ("Linear API key", "LINEAR = 'lin" + "_api_" + "Ab3" * 13 + "x'"),
            ("Notion token", "NOTION = 'ntn" + "_" + "12345678901" + "Zq9" * 12 + "'"),
            ("DigitalOcean token", "DO = 'dop" + "_v1_" + "0123456789abcdef" * 4 + "'"),
            ("Webhook URL", "SLACK ='https://hooks.slack" + ".com/services/T0123/B0456/" + "f" * 24 + "'"),
            ("Webhook URL", "HOOK = 'https://discord" + ".com/api/webhooks/123456789012345678/" + "g" * 68 + "'"),
        ]:
            with self.subTest(name=name):
                self.setUp()
                self.commit("b.txt", text + "\n")
                r = self.guard()
                self.assertEqual(r.returncode, 1, r.stdout)
                self.assertIn(name, r.stdout)

    def test_allows_db_url_without_password(self):
        self.commit("b.txt", "DB = 'postgres" + "://localhost:5432/dev'\nurl = 'https://example.com/a@b'\n")
        self.assertEqual(self.guard().returncode, 0, self.guard().stdout)

    def test_blocks_env_file_but_not_example(self):
        self.commit("app/.env", "DEBUG=1\n")
        r = self.guard()
        self.assertEqual(r.returncode, 1)
        self.assertIn("env file", r.stdout)
        self.setUp()
        self.commit(".env.example", "API_KEY=\n")
        self.assertEqual(self.guard().returncode, 0)

    def test_blocks_key_files_but_not_public_key(self):
        for name in ["deploy/id_ed25519", "id_rsa", "certs/app.p12", "signing.pfx"]:
            self.setUp()
            self.commit(name, "binary-ish\n")
            r = self.guard()
            self.assertEqual(r.returncode, 1, name)
            self.assertIn("key file", r.stdout)
        self.setUp()
        self.commit("deploy/id_ed25519.pub", "ssh-ed25519 AAAA test\n")
        self.assertEqual(self.guard().returncode, 0)

    def test_clean_lookalikes_pass(self):
        # false-positive corpus: lines that look secret-ish but are normal code and docs.
        # A guard that blocks these would stall every cycle that touches config.
        corpus = "\n".join([
            "token = os.environ['GITHUB_TOKEN']",
            "password: ''",
            "api_key = get_secret('OPENAI_API_KEY')",
            "Keys start with sk-ant- or sk-proj- (see docs).",
            "from huggingface_hub import hf_hub_download",
            "npm_config_cache=/tmp/npm",
            "REDIS_URL=redis://localhost:6379/0",
            "mongodb+srv://cluster0.mongodb.net/test",
            "postgres://user@localhost/dev",
            "Stripe test keys look like sk_test_... and are fine here.",
            "git clone https://github.com/idlehandslabs/founder-kit",
            "Set CLAUDE_CODE_OAUTH_TOKEN in repo secrets.",
            "Uptime 12:30:45, build 20261030:AA (see SG.md).",
            "TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']",
            "Create one at https://api.slack.com/messaging/webhooks (hooks.slack.com/services/...).",
            "Use a key-value store; SKU SK12 ships with monkey-patched key-rotation docs.",
            "TWILIO_API_KEY = os.environ['TWILIO_API_KEY']  # starts with SK, Mailgun keys with key-",
            "SLACK_WEBHOOK_URL = os.environ['SLACK_WEBHOOK_URL']  # discord.com/api/webhooks/<id>/<token>",
            "Request 123e4567-e89b-12d3-a456-426614174000 failed at commit 0123456789abcdef0123456789abcdef01234567-dirty",
            "GITLAB_TOKEN = os.environ['GITLAB_TOKEN']  # glpat-..., DigitalOcean uses dop_v1_...",
        ]) + "\n"
        self.commit("docs/setup.md", corpus)
        r = self.guard()
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_blocks_email(self):
        self.commit("b.txt", "mail me: someone@" + "gmail.com\n")
        self.assertEqual(self.guard().returncode, 1)

    def test_blocks_private_term_without_printing_it(self):
        self.commit("b.txt", "lives in Springfield\n")
        r = self.guard("springfield")
        self.assertEqual(r.returncode, 1)
        self.assertNotIn("springfield", r.stdout.lower())

    def test_blocks_protected_file(self):
        self.commit("agent/guard.py", "# weakened\n")
        self.assertEqual(self.guard().returncode, 1)


if __name__ == "__main__":
    unittest.main()
