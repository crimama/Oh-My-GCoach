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
├── index.md       # Data file index — read this first
├── knowledge/     # Running & health knowledge base (scientific principles, not rules)
├── profile/       # Runner profile & skill graph (baseline analysis)
├── training/      # Weekly reports (YYYY-WNN-weekly-report.md)
├── health/        # Monthly recovery metrics (YYYY-MM-recovery.md)
├── races/         # Race records and analysis
└── plans/         # Training plans
```

## Conventions

- Date: `YYYY-MM-DD`
- Pace: `M'SS"/km`
- Distance: km
- Weight: kg
- Time: `HH:MM:SS`

## Coaching Ground Rules

These are immutable, Garmin-data-based fundamentals. Coaching *strategy* is dynamic — see `data/knowledge/`.

1. **Data-Driven** — Every insight must be backed by Garmin data, never assumptions
2. **Profile-Aware** — Always consider user's goals, races, injury history (`data/profile/runner_profile.md`)
3. **Baseline-Referenced** — Compare against skill graph baseline (`data/profile/skill_graph.md`)
4. **Knowledge-Informed** — Reference `data/knowledge/` for scientific principles, adapt to user's current phase and state
5. **No Hardcoded Thresholds** — Thresholds (sleep, volume, intensity ratio) come from knowledge base + individual data, not fixed numbers

## Telegram Integration

This project uses Claude Code's Telegram MCP plugin to deliver coaching insights.
The coach-agent analyzes Garmin data and sends results via `mcp__plugin_telegram_telegram__reply`.

## Setup

1. `cp scripts/.env.example scripts/.env` and fill in Garmin credentials
2. `pip install -r requirements.txt`
3. Run: `python scripts/garmin_sync.py` (daily) or `python scripts/garmin_sync.py --week` (weekly)
