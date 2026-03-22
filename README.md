# Oh-My-GCoach

나만의 AI 러닝 코치 파이프라인: **Garmin → Claude → Telegram**

Garmin Connect에서 훈련 데이터와 건강 지표를 가져와 Claude Code의 AI 코칭 에이전트로 분석하고, 텔레그램으로 실시간 코칭을 전달합니다.

## 주요 기능

- **Garmin 동기화** — 러닝 활동, 심박 존 분포, 건강 지표 (체중, 수면, HRV, 스트레스, 바디배터리)
- **훈련 분석** — 80/20 존 준수 여부, 10% 볼륨 룰, 주간 볼륨 비교
- **건강 모니터링** — 수면, HRV, 안정시 심박, 스트레스 기반 회복 준비도
- **레이스 예측** — Garmin 기반 5K / 10K / 하프 / 풀 마라톤 예상 기록
- **텔레그램 전달** — AI 코칭 인사이트를 채팅으로 바로 전달

## 아키텍처

```
Garmin Watch → Garmin Connect API → garmin_sync.py → data/ (markdown)
                                                        ↓
                                            Claude coach-agent (분석)
                                                        ↓
                                                   Telegram bot
```

---

# Part 1: 사용자가 직접 해야 할 것

> 아래는 **사용자가 직접 준비하고 확인**해야 하는 항목입니다.
> 이 부분을 완료한 뒤, Claude Code에게 설치를 맡기면 나머지는 자동으로 진행됩니다.

## 1. 사전 준비 체크리스트

시작 전에 아래 항목을 준비해주세요:

- [ ] **Python 3.8+** 설치됨 (`python3 --version`으로 확인)
- [ ] **Garmin Connect 계정** — Garmin 워치와 페어링된 계정, 이메일/비밀번호 확인
- [ ] **Claude Code 설치됨** — [설치 가이드](https://docs.anthropic.com/en/docs/claude-code/overview)
- [ ] **Telegram Bot 생성 (선택)** — [@BotFather](https://t.me/BotFather)에서 봇을 만들고 토큰 메모

### Telegram Bot 만드는 법

1. 텔레그램에서 [@BotFather](https://t.me/BotFather)에게 `/newbot` 전송
2. 봇 이름과 username 설정 (예: `MyCoachBot`, `my_coach_123_bot`)
3. BotFather가 보내주는 토큰(`123456:ABC-DEF...`)을 메모

## 2. 설치 시작

```bash
git clone https://github.com/<your-username>/Oh-My-GCoach.git
cd Oh-My-GCoach
claude
```

Claude Code가 실행되면 아래 한 줄을 입력합니다:

```
SETUP.md를 따라 이 프로젝트를 설치해줘.
```

이후 Claude Code가 질문하면 **Garmin 이메일/비밀번호**와 **Telegram 봇 토큰**만 붙여넣으면 됩니다. 나머지는 자동입니다.

## 3. 설치 후 사용법

### 터미널 명령어

```bash
python scripts/garmin_sync.py                              # 오늘 데이터 동기화
python scripts/garmin_sync.py --date 2026-03-17            # 특정 날짜 동기화
python scripts/garmin_sync.py --week                       # 이번 주 리포트
python scripts/garmin_sync.py --week --date 2026-03-17     # 특정 주 리포트
python scripts/garmin_sync.py --range 2026-03-01 2026-03-17  # 기간별 조회
python scripts/garmin_auth.py                              # 로그인 테스트 & 디바이스 목록
```

### AI 코칭 명령어 (Claude Code 안에서)

터미널에서 `claude`를 실행한 뒤, coach agent에게 명령합니다:

```
# --- 일일 코칭 ---
@coach-agent 오늘 훈련 데이터 동기화하고 분석해줘
@coach-agent 오늘 컨디션 체크해줘 (수면, HRV, 스트레스)
@coach-agent 오늘 어떤 훈련을 하면 좋을까?

# --- 주간 분석 ---
@coach-agent 이번 주 훈련 리포트 만들어줘
@coach-agent 지난주 대비 이번 주 훈련량 비교해줘 (10% 룰)
@coach-agent 이번 주 심박 존 분포 분석해줘

# --- 건강 & 회복 ---
@coach-agent 최근 회복 지표 트렌드 보여줘 (수면, HRV, 안정시심박)
@coach-agent 최근 체중 변화 추이 분석해줘
@coach-agent 내일 인터벌 훈련 가능한 컨디션인지 확인해줘

# --- 레이스 & 계획 ---
@coach-agent 현재 예상 레이스 기록 알려줘
@coach-agent 하프마라톤 목표로 다음 4주 훈련 방향 제안해줘
@coach-agent 지난 대회 기록 분석하고 개선점 알려줘

# --- 텔레그램 전달 ---
@coach-agent 이번 주 훈련 분석해서 텔레그램으로 보내줘
@coach-agent 오늘 컨디션 체크하고 훈련 추천을 텔레그램으로 보내줘
@coach-agent 주간 리포트 생성해서 텔레그램으로 전송해줘
```

## 4. 문제가 생겼을 때

| 증상 | 해결 방법 |
|------|----------|
| `ModuleNotFoundError` | `.venv` 활성화 후 `pip install -r requirements.txt` |
| Garmin 로그인 실패 | `~/.garminconnect/` 삭제 후 재시도. `scripts/.env` 확인 |
| 활동이 안 보임 | 오늘 러닝이 없으면 정상. `--date`로 과거 날짜 조회 |
| 텔레그램 봇 무응답 | 봇 토큰 확인. `/telegram:configure` 재실행 |
| Permission denied | `chmod +x scripts/*.py` 실행 |

---

# Part 2: LLM 자동 설치 프로토콜

> 아래는 **LLM(Claude Code 등)이 읽고 자동으로 실행**하는 설치 프로토콜입니다.
> 사용자가 `SETUP.md를 따라 설치해줘`라고 하면 이 섹션의 단계를 순서대로 수행합니다.
> `[ASK USER]` 표시가 있는 곳에서만 사용자에게 질문하고, 나머지는 자동으로 진행합니다.

### Step 1: Python 확인

```bash
python3 --version
```

- **Pass**: 3.8 이상
- **Fail**: OS에 맞는 설치 명령 안내
  - macOS: `brew install python3`
  - Ubuntu/Debian: `sudo apt install python3 python3-venv python3-pip`
  - Windows: https://www.python.org/downloads/

### Step 2: 가상환경 생성

`.venv/`가 없으면:

```bash
python3 -m venv .venv
source .venv/bin/activate   # Linux/macOS
```

### Step 3: 의존성 설치

```bash
pip install -r requirements.txt
```

검증:
```bash
python3 -c "import garminconnect; import garth; import dotenv; import requests; print('All dependencies OK')"
```

### Step 4: Garmin 자격 증명

`scripts/.env`가 없으면:
```bash
cp scripts/.env.example scripts/.env
```

`[ASK USER]` Garmin Connect 이메일과 비밀번호를 물어본다.

`scripts/.env`에 작성:
```
GARMIN_EMAIL=<사용자 이메일>
GARMIN_PASSWORD=<사용자 비밀번호>
```

> `scripts/.env`는 `.gitignore`에 포함되어 있으므로 git에 올라가지 않음을 안내한다.

### Step 5: Garmin 연결 테스트

```bash
python scripts/garmin_auth.py
```

- **Pass**: `Login OK! Devices: [...]` 출력
- **Fail (인증)**: 이메일/비밀번호 재확인 요청
- **Fail (MFA/CAPTCHA)**: https://connect.garmin.com 에서 브라우저 로그인 후 재시도 안내

### Step 6: 첫 데이터 동기화

```bash
python scripts/garmin_sync.py
```

- **Pass**: 러닝 활동 또는 "No running activities" + 건강 지표 출력
- **Fail (토큰 만료)**: `~/.garminconnect/` 삭제 후 Step 5 재실행

주간 리포트도 생성:
```bash
python scripts/garmin_sync.py --week
```

`data/health/` 또는 `data/training/`에 파일이 생성되었는지 확인.

### Step 7: 텔레그램 설정

`[ASK USER]` 텔레그램 연동을 원하는지 확인.

원하면:

1. `[ASK USER]` 봇 토큰을 물어본다. 없으면 [@BotFather](https://t.me/BotFather)에서 `/newbot`으로 생성하라고 안내.
2. `/telegram:configure` 실행 후 토큰 입력.
3. `[ASK USER]` 텔레그램에서 봇에게 아무 메시지를 보내라고 안내. 보냈다고 하면 진행.
4. `/telegram:access` 실행하여 페어링 승인.
5. `mcp__plugin_telegram_telegram__reply`로 테스트 메시지 전송.

### Step 8: Coach Agent 확인

`.claude/agents/coach-agent.md` 파일 존재 확인.

```
@coach-agent 현재 사용 가능한 데이터 확인해줘
```

### Step 9: 완료 안내

사용자에게 아래 내용을 전달:

```
설치 완료! 사용 가능한 명령어:

  데이터 동기화:  python scripts/garmin_sync.py
  주간 리포트:    python scripts/garmin_sync.py --week
  기간별 조회:    python scripts/garmin_sync.py --range 시작일 종료일
  AI 코칭:       @coach-agent <질문>

데이터 저장 위치:
  data/training/  — 주간 리포트
  data/health/    — 회복 지표 (수면, HRV, 체중 등)
```

---

## 참조

### 데이터 구조

```
data/
├── training/   # 주간 리포트 (YYYY-WNN-weekly-report.md)
├── health/     # 월별 회복 지표 (YYYY-MM-recovery.md)
├── races/      # 대회 기록 및 분석
└── plans/      # 훈련 계획
```

### 코칭 철학

| 원칙 | 설명 |
|------|------|
| **80/20 원칙** | 이지런(Z1+Z2)이 전체 훈련 시간의 80% 이상이어야 함 |
| **10% 원칙** | 주간 훈련량 증가는 10%를 초과하지 않아야 함 |
| **회복 우선** | 수면 < 7.5시간, 낮은 HRV, 높은 스트레스 시 강도 높은 훈련 경고 |
| **데이터 기반** | 모든 인사이트는 Garmin 데이터로 뒷받침 |

### 스크립트 목록

| 스크립트 | 역할 |
|---------|------|
| `scripts/garmin_sync.py` | 메인 진입점 — 일별 동기화, 주간 리포트, 기간별 조회 |
| `scripts/garmin_auth.py` | Garmin Connect OAuth 인증 (garth), Bearer 토큰 API 호출 |
| `scripts/garmin_activities.py` | 러닝 활동 데이터, 심박 존, 페이스/시간 포맷팅 |
| `scripts/garmin_health.py` | 건강 지표: 체중, 수면, HRV, 스트레스, 바디배터리 |
| `scripts/garmin_report.py` | 주간 리포트 생성 및 볼륨 비교 |

## License

MIT
