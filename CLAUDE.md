# Oh-My-GCoach

Garmin → Claude → Telegram running coach pipeline.

## Architecture

```
Garmin Connect (watch data)
    ↓
scripts/garmin_sync.py (fetch & format)
    ↓
data/ (markdown files)
    ↓
Claude coach-agent (analyze & advise)
    ↓
Telegram (deliver to user)
```

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/garmin_sync.py` | Main entry point — daily sync, weekly report, date range query |
| `scripts/garmin_auth.py` | Garmin Connect OAuth via garth, Bearer token API calls |
| `scripts/garmin_activities.py` | Running activity data, HR zones, pace/duration formatting |
| `scripts/garmin_health.py` | Health metrics: weight, sleep, HRV, stress, body battery |
| `scripts/garmin_report.py` | Weekly report generation with volume comparison |

## Data

```
data/
├── profile/    # Runner profile & skill graph (baseline analysis)
├── training/   # Weekly reports (YYYY-WNN-weekly-report.md)
├── health/     # Monthly recovery metrics (YYYY-MM-recovery.md)
├── races/      # Race records and analysis
└── plans/      # Training plans
```

## Conventions

- Date: `YYYY-MM-DD`
- Pace: `M'SS"/km`
- Distance: km
- Weight: kg
- Time: `HH:MM:SS`

## Coaching Rules

1. **80/20 Rule** — Easy (Z1+Z2) should be >= 80% of training time
2. **10% Rule** — Weekly volume increase must not exceed 10%
3. **Recovery First** — Flag sleep < 7.5h, low HRV, high stress before hard sessions
4. **Data-Driven** — Every insight backed by Garmin data

## Telegram Integration

This project uses Claude Code's Telegram MCP plugin to deliver coaching insights.
The coach-agent analyzes Garmin data and sends results via `mcp__plugin_telegram_telegram__reply`.

## Setup

1. `cp scripts/.env.example scripts/.env` and fill in Garmin credentials
2. `pip install -r requirements.txt`
3. Run: `python scripts/garmin_sync.py` (daily) or `python scripts/garmin_sync.py --week` (weekly)
