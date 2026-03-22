# Oh-My-GCoach

Personal running coach pipeline: **Garmin → Claude → Telegram**

Fetches training data and health metrics from Garmin Connect, analyzes them with Claude Code's AI coaching agent, and delivers actionable insights via Telegram.

## Features

- **Garmin Sync**: Fetch running activities, HR zone distribution, health metrics
- **Training Analysis**: 80/20 zone compliance, 10% volume rule, weekly comparisons
- **Health Monitoring**: Weight, sleep, HRV, resting HR, stress, body battery, training readiness
- **Race Predictions**: 5K / 10K / Half / Full marathon time estimates
- **Telegram Delivery**: Coaching insights delivered directly to your chat

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set up Garmin credentials
cp scripts/.env.example scripts/.env
# Edit scripts/.env with your Garmin email and password

# Sync today's data
python scripts/garmin_sync.py

# Generate weekly report
python scripts/garmin_sync.py --week

# Query a date range
python scripts/garmin_sync.py --range 2026-03-01 2026-03-17
```

## Architecture

```
Garmin Watch → Garmin Connect API → garmin_sync.py → data/ (markdown)
                                                        ↓
                                            Claude coach-agent (analysis)
                                                        ↓
                                                   Telegram bot
```

## Requirements

- Python 3.8+
- Garmin Connect account
- Claude Code with Telegram MCP plugin (for coaching delivery)
