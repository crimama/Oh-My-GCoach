# Setup Protocol

> **This document is an automated setup protocol for LLMs (e.g. Claude Code).**
> Follow each step in order. Ask the user for input only when marked with `[ASK USER]`.
> Skip steps that are already completed. Verify each step before moving on.

---

## Step 1: Check Python

Run:
```bash
python3 --version
```

- **Pass**: Python 3.8+
- **Fail**: Tell the user to install Python 3.8+ and provide their OS-appropriate install command:
  - macOS: `brew install python3`
  - Ubuntu/Debian: `sudo apt install python3 python3-venv python3-pip`
  - Windows: Download from https://www.python.org/downloads/

---

## Step 2: Create Virtual Environment

Check if `.venv/` already exists. If not:

```bash
python3 -m venv .venv
```

Then activate (for verification commands in subsequent steps):
```bash
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows
```

---

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Verify all packages installed:
```bash
python3 -c "import garminconnect; import garth; import dotenv; import requests; print('All dependencies OK')"
```

If any import fails, retry `pip install -r requirements.txt` or install the missing package individually.

---

## Step 4: Configure Garmin Credentials

Check if `scripts/.env` exists.

If not, copy the example:
```bash
cp scripts/.env.example scripts/.env
```

`[ASK USER]` Ask the user for their Garmin Connect credentials:
- **GARMIN_EMAIL**: Their Garmin Connect login email
- **GARMIN_PASSWORD**: Their Garmin Connect password

Write these values to `scripts/.env`:
```
GARMIN_EMAIL=<user's email>
GARMIN_PASSWORD=<user's password>
```

> **Security note**: `scripts/.env` is already in `.gitignore`. Confirm this to the user.

---

## Step 5: Test Garmin Connection

```bash
python scripts/garmin_auth.py
```

- **Pass**: Output shows `Login OK! Devices: [...]`
- **Fail — wrong credentials**: Ask user to double-check email/password
- **Fail — MFA/CAPTCHA**: Garmin may require browser login first. Tell the user to:
  1. Log in to https://connect.garmin.com in their browser
  2. Complete any MFA or CAPTCHA challenges
  3. Try again

---

## Step 6: First Data Sync

Run a daily sync to verify the full pipeline:
```bash
python scripts/garmin_sync.py
```

- **Pass**: Shows today's running activities (or "No running activities") and health metrics
- **Fail**: Debug based on error message. Common issues:
  - Token expired → delete `~/.garminconnect/` and re-run Step 5
  - No data → Normal if no activities today. Try: `python scripts/garmin_sync.py --date <recent-date>`

Then generate a weekly report:
```bash
python scripts/garmin_sync.py --week
```

Verify that files were created in `data/health/` and/or `data/training/`.

---

## Step 7: Telegram Bot Setup

`[ASK USER]` Ask the user if they want to set up Telegram delivery.

If yes:

1. `[ASK USER]` Ask: "Do you already have a Telegram bot token? If not, create one by talking to @BotFather on Telegram (https://t.me/BotFather) — send `/newbot`, follow the prompts, and paste the token here."

2. Once the user provides the bot token, run the Telegram configure skill:
   ```
   /telegram:configure
   ```
   Paste the bot token when prompted.

3. `[ASK USER]` Tell the user: "Now send any message to your bot on Telegram (find it by the bot username @BotFather gave you). Then tell me here when you've sent a message."

4. Once the user confirms, run:
   ```
   /telegram:access
   ```
   Approve the pending pairing.

5. Test by sending a message:
   Use the `mcp__plugin_telegram_telegram__reply` tool to send a test message to the user's chat.

---

## Step 8: Verify Coach Agent

Confirm that `.claude/agents/coach-agent.md` exists in the project.

Test the agent by asking it a simple question:
```
@coach-agent What data do we have available?
```

The agent should be able to read files in `data/` and run `garmin_sync.py`.

---

## Step 9: Setup Complete

Summarize the available commands below to the user.

---

## Commands Reference

Setup is complete. Here are all the commands available in this system.

### Data Sync (Terminal)

```bash
# Sync today's training + health data
python scripts/garmin_sync.py

# Sync a specific date
python scripts/garmin_sync.py --date 2026-03-17

# Generate this week's report
python scripts/garmin_sync.py --week

# Generate a specific week's report
python scripts/garmin_sync.py --week --date 2026-03-17

# Query activities in a date range
python scripts/garmin_sync.py --range 2026-03-01 2026-03-17

# Test Garmin login & list devices
python scripts/garmin_auth.py
```

### AI Coaching (Claude Code)

These commands are used inside Claude Code (`claude` in terminal).

#### Daily Coaching

```
# Sync today and analyze
@coach-agent 오늘 훈련 데이터 동기화하고 분석해줘

# Check today's recovery status before training
@coach-agent 오늘 컨디션 체크해줘 (수면, HRV, 스트레스)

# Get today's training recommendation
@coach-agent 오늘 어떤 훈련을 하면 좋을까?
```

#### Weekly Analysis

```
# Weekly training summary with 80/20 analysis
@coach-agent 이번 주 훈련 리포트 만들어줘

# Check 10% volume rule compliance
@coach-agent 지난주 대비 이번 주 훈련량 비교해줘

# Weekly zone distribution analysis
@coach-agent 이번 주 심박 존 분포 분석해줘
```

#### Health & Recovery

```
# Recovery metrics overview
@coach-agent 최근 회복 지표 트렌드 보여줘 (수면, HRV, 안정시심박)

# Body composition tracking
@coach-agent 최근 체중 변화 추이 분석해줘

# Training readiness check
@coach-agent 내일 인터벌 훈련 가능한 컨디션인지 확인해줘
```

#### Race & Planning

```
# Race prediction times
@coach-agent 현재 예상 레이스 기록 알려줘

# Training plan advice
@coach-agent 하프마라톤 목표로 다음 4주 훈련 방향 제안해줘

# Race review
@coach-agent 지난 대회 기록 분석하고 개선점 알려줘
```

#### Telegram Delivery

```
# Analyze and send to Telegram
@coach-agent 이번 주 훈련 분석해서 텔레그램으로 보내줘

# Daily morning briefing via Telegram
@coach-agent 오늘 컨디션 체크하고 훈련 추천을 텔레그램으로 보내줘

# Send weekly report to Telegram
@coach-agent 주간 리포트 생성해서 텔레그램으로 전송해줘
```

### Data Location

```
data/
├── training/   # Weekly reports (YYYY-WNN-weekly-report.md)
├── health/     # Monthly recovery metrics (YYYY-MM-recovery.md)
├── races/      # Race records and analysis
└── plans/      # Training plans
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` (activate venv first) |
| Garmin login fails | Delete `~/.garminconnect/` and retry. Check credentials in `scripts/.env` |
| No activities found | Normal if no runs today. Use `--date` to query a past date |
| Telegram bot not responding | Ensure bot token is correct. Re-run `/telegram:configure` |
| Permission denied | Check file permissions. Try `chmod +x scripts/*.py` |
