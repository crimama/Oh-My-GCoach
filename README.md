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

## 사전 준비

| 요구사항 | 비고 |
|---------|------|
| Python 3.8+ | `python3 --version`으로 확인 |
| Garmin Connect 계정 | Garmin 워치와 페어링된 계정 |
| Claude Code | [설치 가이드](https://docs.anthropic.com/en/docs/claude-code/overview) |
| Telegram Bot Token | [@BotFather](https://t.me/BotFather)에서 생성 |

## 빠른 시작 (자동 설치)

> **가장 쉬운 방법: Claude Code에게 설치를 맡기세요.**

1. 레포를 클론합니다:
   ```bash
   git clone https://github.com/<your-username>/Oh-My-GCoach.git
   cd Oh-My-GCoach
   ```

2. Claude Code를 실행하고 설치를 요청합니다:
   ```bash
   claude
   ```
   그리고 다음과 같이 입력:
   ```
   SETUP.md를 따라 이 프로젝트를 설치해줘.
   ```

3. Claude Code가 각 단계를 안내합니다 — 자격 증명, 의존성 설치, 텔레그램 봇 연동, 테스트 동기화까지 자동으로 진행됩니다.

## 빠른 시작 (수동 설치)

```bash
# 1. 클론
git clone https://github.com/<your-username>/Oh-My-GCoach.git
cd Oh-My-GCoach

# 2. 가상환경 생성 (권장)
python3 -m venv .venv
source .venv/bin/activate

# 3. 의존성 설치
pip install -r requirements.txt

# 4. Garmin 자격 증명 설정
cp scripts/.env.example scripts/.env
# scripts/.env 파일에 Garmin 이메일과 비밀번호 입력

# 5. Garmin 연결 테스트
python scripts/garmin_auth.py

# 6. 오늘 데이터 동기화
python scripts/garmin_sync.py

# 7. 주간 리포트 생성
python scripts/garmin_sync.py --week
```

### 텔레그램 설정

1. [@BotFather](https://t.me/BotFather)에서 봇을 생성합니다
2. Claude Code에서 `/telegram:configure`를 실행하고 봇 토큰을 붙여넣습니다
3. 텔레그램에서 봇에게 아무 메시지나 보낸 뒤, Claude Code에서 `/telegram:access`로 페어링을 승인합니다

## 사용법

### 데이터 동기화 (터미널)

```bash
python scripts/garmin_sync.py                              # 오늘 데이터
python scripts/garmin_sync.py --date 2026-03-17            # 특정 날짜
python scripts/garmin_sync.py --week                       # 이번 주 리포트
python scripts/garmin_sync.py --week --date 2026-03-17     # 특정 주 리포트
python scripts/garmin_sync.py --range 2026-03-01 2026-03-17  # 기간별 조회
python scripts/garmin_auth.py                              # 로그인 테스트 & 디바이스 목록
```

### AI 코칭 (Claude Code)

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

## 데이터 구조

```
data/
├── training/   # 주간 리포트 (YYYY-WNN-weekly-report.md)
├── health/     # 월별 회복 지표 (YYYY-MM-recovery.md)
├── races/      # 대회 기록 및 분석
└── plans/      # 훈련 계획
```

## 코칭 철학

| 원칙 | 설명 |
|------|------|
| **80/20 원칙** | 이지런(Z1+Z2)이 전체 훈련 시간의 80% 이상이어야 함 |
| **10% 원칙** | 주간 훈련량 증가는 10%를 초과하지 않아야 함 |
| **회복 우선** | 수면 < 7.5시간, 낮은 HRV, 높은 스트레스 시 강도 높은 훈련 경고 |
| **데이터 기반** | 모든 인사이트는 Garmin 데이터로 뒷받침 |

## 스크립트 참조

| 스크립트 | 역할 |
|---------|------|
| `scripts/garmin_sync.py` | 메인 진입점 — 일별 동기화, 주간 리포트, 기간별 조회 |
| `scripts/garmin_auth.py` | Garmin Connect OAuth 인증 (garth), Bearer 토큰 API 호출 |
| `scripts/garmin_activities.py` | 러닝 활동 데이터, 심박 존, 페이스/시간 포맷팅 |
| `scripts/garmin_health.py` | 건강 지표: 체중, 수면, HRV, 스트레스, 바디배터리 |
| `scripts/garmin_report.py` | 주간 리포트 생성 및 볼륨 비교 |

## License

MIT
