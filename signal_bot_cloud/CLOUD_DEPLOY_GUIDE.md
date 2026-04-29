# 🚀 Signal Bot — Cloud Deployment Guide (Railway)

## What this achieves
Your bot runs 24/7 on Railway's servers in the cloud.
Signals arrive on your Telegram even when your phone and laptop are completely off.

---

## You will need (all free)
- A Gmail or GitHub account
- Your Telegram Bot Token (from @BotFather)
- Your Telegram Chat ID (from @userinfobot)
- An Alpha Vantage API key (from alphavantage.co)

---

## STEP 1 — Create a free GitHub account
1. Go to https://github.com
2. Click "Sign up" → use your email → confirm account
3. Click "New repository" (green button)
4. Name it: `signal-bot`
5. Set it to **Private**
6. Click "Create repository"

---

## STEP 2 — Upload your bot files to GitHub
1. Inside your new empty repo, click **"uploading an existing file"**
2. Drag ALL files from this folder into the upload area:
   - `bot.py`
   - `Procfile`
   - `runtime.txt`
   - `requirements.txt`
   - The entire `config/` folder
   - The entire `signals/` folder
3. Scroll down → click **"Commit changes"**

---

## STEP 3 — Create a free Railway account
1. Go to https://railway.app
2. Click **"Start a New Project"**
3. Click **"Login with GitHub"** → authorize Railway
4. Click **"Deploy from GitHub repo"**
5. Select your `signal-bot` repository
6. Railway will detect it's a Python project automatically

---

## STEP 4 — Add your secret credentials
In the Railway dashboard:
1. Click your project → click the **"Variables"** tab
2. Add these 3 variables one by one:

| Variable Name          | Your Value                    |
|------------------------|-------------------------------|
| `TELEGRAM_BOT_TOKEN`   | Your token from @BotFather    |
| `CHAT_ID`              | Your numeric ID from @userinfobot |
| `ALPHA_VANTAGE_API_KEY`| Your key from alphavantage.co |

3. Click **"Deploy"** after adding all 3

---

## STEP 5 — Confirm it's running
1. Click the **"Deployments"** tab in Railway
2. Click the latest deployment → click **"View Logs"**
3. You should see:
   ```
   ✅ Bot is live! Listening for commands...
   ⏰ Scheduler started. 5 signals/day scheduled (WAT timezone).
   ```
4. Open Telegram → find your bot → send `/start`

---

## Done! 🎉
Your bot now runs forever in the cloud. Railway's free tier gives you
$5 of free credit monthly — more than enough for a simple bot like this.

Signals will arrive at: 6am, 9am, 12pm, 3pm, 6pm (WAT) every day.

---

## If something goes wrong
- **Bot not responding**: Check the Variables tab — make sure all 3 are set correctly
- **Deployment failing**: Check Logs for error messages and share them for help
- **No signals arriving**: Confirm your CHAT_ID is correct (must be numbers only)
