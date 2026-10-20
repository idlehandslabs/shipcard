# Setup: click by click (about 30 minutes, once)

## Part 1: an anonymous identity (do this first)
1. Make a **new email address** just for Idle Hands Labs. Use it for everything below.
   Never use your personal email, name or photo anywhere in this setup.
2. Go to **github.com/signup** with that new email. Username: **idlehandslabs** (or the
   closest free one). Leave name, photo, bio, location and company **empty**.
3. Top-right avatar → **Settings → Emails** → tick **Keep my email addresses private**
   and **Block command line pushes that expose my email**.

## Part 2: create the repo and upload
4. Top-right **+** → **New repository**. Name: **shipcard**. Choose **Public**. Don't tick
   anything else. Click **Create repository**.
5. On the empty repo page, click the link **uploading an existing file**.
6. On your computer: right-click `idlehandslabs-UPLOAD.zip` → **Extract All**. Open the
   `idlehandslabs` folder inside. Press **Ctrl+A** to select everything (including the
   `.github` and `.claude` folders) and **drag it all** onto the GitHub page.
7. Wait until every file shows in the list. Click **Commit changes**.
8. Check the repo page shows a `.github` folder. If not, repeat step 6 with just that folder.

## Part 3: secrets (nobody can read these once saved, not even the agent)
9. Go to **console.anthropic.com**, sign up, add a little credit under **Billing**, then
   **API Keys → Create Key**. Copy it (starts with `sk-ant-`). Don't paste it anywhere else.
10. In your repo: **Settings → Secrets and variables → Actions → New repository secret**.
    Name: `ANTHROPIC_API_KEY`. Secret: paste the key. **Add secret**.
11. **New repository secret** again. Name: `PRIVATE_TERMS`. Secret: a comma-separated list
    of everything that must never appear publicly, e.g. your full name, first name,
    personal emails, personal usernames, city, workplace, phone number. **Add secret**.
    Every push is checked against this list and blocked if anything matches. The list is
    never printed, not even in logs.

## Part 4: safety switches
12. **Settings → Actions → General**:
    - *Workflow permissions*: **Read and write permissions** → **Save**.
    - *Fork pull request workflows from outside collaborators*: **Require approval for all
      outside collaborators** → **Save**.
13. **Settings → Advanced Security** (may be called *Code security*): turn on **Secret
    Protection / Push protection** if you see it.
14. **Settings → Pages**: *Source* → **GitHub Actions**.
15. **Settings → Environments → github-pages** (refresh if it's not there yet): tick
    **Required reviewers**, add **idlehandslabs**, **Save protection rules**.

## Part 5: first run
16. Open the **Actions** tab → click **I understand my workflows, go ahead and enable them**.
17. Click **ai-founder** (left) → **Run workflow** → job: **cycle** → **Run workflow**.
    Wait 3–5 minutes for the green tick.
18. A **deploy-shipcard** run appears, waiting. Open it → **Review deployments** → tick
    **github-pages** → **Approve and deploy**.
19. Shipcard is live at `https://<your-username>.github.io/shipcard/`.

## After that, your daily routine (about 5 minutes)
- Approve deploys when GitHub emails you.
- Read the newest file in `daily-log/` (the article) and `post-queue/` (short posts).
- Post them on X from the Idle Hands Labs account (also made with the new email).

## If something goes red
Open the failed run, scroll to the red step, and copy the message to Claude. If the
**Guard** step is red, the agent tried to commit something that matched a secret, an email
or a private term, and the push was stopped. That's the guard working.
