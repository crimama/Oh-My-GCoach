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

This project uses `claude --channels` to connect with Telegram.

### How It Works

```
claude --channels plugin:telegram@claude-plugins-official
```

- Claude Code starts with the Telegram plugin as a channel
- Plugin polls the Telegram Bot API for incoming messages
- Messages arrive as `<channel source="telegram">` tags in the session
- Claude processes the message and replies via `mcp__plugin_telegram_telegram__reply`
- Channel is only active while the session is running

### Key Files

- `~/.claude/channels/telegram/.env` — Bot token (`TELEGRAM_BOT_TOKEN=...`)
- `~/.claude/channels/telegram/access.json` — Sender allowlist

### Access Control

- `/telegram:access pair <code>` — Approve a pairing code
- `/telegram:access policy allowlist` — Only paired users can send messages
- `/telegram:access list` — Show approved senders

## Permissions

`.claude/settings.json`에 정의된 permission 정책:

### 자동 허용 (permission 요청 없음)
- `scripts/garmin_sync.py`, `scripts/garmin_auth.py` 실행
- `pip install -r requirements.txt`
- `data/` 하위 파일 읽기/쓰기/수정
- 파일 검색 (Glob, Grep, Read)

### 수동 승인 필요
- `scripts/*.py` 소스 코드 수정
- `data/` 외부 파일 생성/수정
- 시스템 명령어 실행
- 패키지 추가 설치

> 일상적인 데이터 동기화, 분석, 사용자 질의 응답은 중단 없이 자동 처리된다.
> 코드 변경이 필요한 경우에만 터미널에서 permission을 요청한다.

## Setup

1. `cp scripts/.env.example scripts/.env` and fill in Garmin credentials
2. `pip install -r requirements.txt`
3. Run: `claude --channels plugin:telegram@claude-plugins-official`
