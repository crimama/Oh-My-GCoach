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
사용자 (텔레그램 메시지)
    ↓
Telegram Bot API (polling)
    ↓
claude --channels (Telegram plugin)
    ↓
Claude coach-agent (메시지 수신 & 판단)
    ↓
garmin_sync.py (Garmin Connect API에서 데이터 수집)
    ↓
data/ (markdown 저장) + knowledge/ (지식 베이스 참조)
    ↓
Claude coach-agent (분석 & 코칭)
    ↓
mcp__plugin_telegram_telegram__reply
    ↓
사용자 (텔레그램으로 결과 수신)
```

> 사용자는 **텔레그램으로 메시지를 보내는 것만으로** 모든 기능을 사용합니다.
> `claude --channels` 세션이 실행 중이어야 메시지를 수신합니다.

---

# Part 1: 사용자가 직접 해야 할 것

> 아래는 **사용자가 직접 준비하고 확인**해야 하는 항목입니다.
> 이 부분을 완료한 뒤, Claude Code에게 설치를 맡기면 나머지는 자동으로 진행됩니다.

## 1. 사전 준비 체크리스트

시작 전에 아래 항목을 준비해주세요:

- [ ] **Python 3.8+** 설치됨 (`python3 --version`으로 확인)
- [ ] **Garmin Connect 계정** — Garmin 워치와 페어링된 계정, 이메일/비밀번호 확인
- [ ] **Claude Code 최신 버전** — [설치 가이드](https://docs.anthropic.com/en/docs/claude-code/overview) (claude.ai 계정으로 로그인)
  - 설치: `npm install -g @anthropic-ai/claude-code`
  - 업데이트: `npm update -g @anthropic-ai/claude-code`
  - `--channels` 기능은 **v2.1.80+** 이상 필요
- [ ] **Bun 설치됨** — Telegram 플러그인 실행에 필요 ([설치](https://bun.sh))
- [ ] **Telegram Bot 토큰** — 아래 방법으로 생성

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

이후 Claude Code가 질문하는 항목에 답변만 하면 됩니다:
- **Garmin 이메일/비밀번호** — Garmin Connect 연동용
- **Telegram 봇 토큰** — 코칭 메시지 수신용
- **러닝 프로필** — 목표 기록, 예정된 대회, 추구하는 방향, 부상 이력 등

설치 마지막에 Garmin의 **최근 1년 데이터를 자동 분석**하여 현재 실력 수준과 강점/약점을 파악한 스킬 그래프를 만들어줍니다. 이후 모든 코칭은 이 분석을 기반으로 제공됩니다.

## 3. 코칭 세션 실행

설치가 완료되면, 코칭 세션을 시작합니다:

```bash
cd Oh-My-GCoach
claude --channels plugin:telegram@claude-plugins-official
```

이 명령으로 Claude Code가 텔레그램 채널에 연결되어 **봇에게 보내는 메시지를 실시간으로 수신**하고 코칭을 제공합니다.

> **초기 설정 주의사항**: 텔레그램 연결 직후 첫 메시지를 보내면 Claude Code가 터미널에서
> **permission 승인을 요청**할 수 있습니다 (파일 접근, 스크립트 실행 등).
> 이때 터미널을 확인하고 승인해주어야 봇이 정상 응답합니다.
> 첫 승인 이후에는 동일한 작업에 대해 다시 묻지 않습니다.

#### 항상 켜두기 (백그라운드 실행)

코칭 봇을 상시 실행하려면 tmux를 사용합니다:

```bash
# tmux 사용
tmux new-session -d -s gcoach "cd Oh-My-GCoach && claude --channels plugin:telegram@claude-plugins-official"

# 세션 확인 (permission 승인이 필요할 때도 여기서 확인)
tmux attach -t gcoach
```

## 4. 텔레그램에서 사용하기

세션이 실행 중이면 **텔레그램에서 봇에게 메시지를 보내는 것만으로** 모든 기능을 사용할 수 있습니다.

### 메시지 예시

```
# --- 일일 코칭 ---
오늘 훈련 데이터 동기화하고 분석해줘
오늘 컨디션 체크해줘 (수면, HRV, 스트레스)
오늘 어떤 훈련을 하면 좋을까?

# --- 주간 분석 ---
이번 주 훈련 리포트 만들어줘
지난주 대비 이번 주 훈련량 비교해줘 (10% 룰)
이번 주 심박 존 분포 분석해줘

# --- 건강 & 회복 ---
최근 회복 지표 트렌드 보여줘 (수면, HRV, 안정시심박)
최근 체중 변화 추이 분석해줘
내일 인터벌 훈련 가능한 컨디션인지 확인해줘

# --- 레이스 & 계획 ---
현재 예상 레이스 기록 알려줘
하프마라톤 목표로 다음 4주 훈련 방향 제안해줘
지난 대회 기록 분석하고 개선점 알려줘
```

## 5. 문제가 생겼을 때

| 증상 | 해결 방법 |
|------|----------|
| `ModuleNotFoundError` | `pip install -r requirements.txt` 재실행 |
| Garmin 로그인 실패 | `~/.garminconnect/` 삭제 후 재시도. `scripts/.env` 확인 |
| 활동이 안 보임 | 오늘 러닝이 없으면 정상 |
| 텔레그램 봇 무응답 | `claude --channels` 세션이 실행 중인지 확인. 봇 토큰 확인 |
| 텔레그램 페어링 안 됨 | `--channels` 플래그 없이 실행 중일 수 있음. 재시작 필요 |
| Plugin not found | `/plugin marketplace update claude-plugins-official` 실행 |
| Bun 미설치 | `curl -fsSL https://bun.sh/install \| bash` |

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
  - Ubuntu/Debian: `sudo apt install python3 python3-pip`
  - Windows: https://www.python.org/downloads/

### Step 2: 의존성 설치

```bash
pip install -r requirements.txt
```

검증:
```bash
python3 -c "import garminconnect; import garth; import dotenv; import requests; print('All dependencies OK')"
```

### Step 3: Garmin 자격 증명

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

### Step 4: Garmin 연결 테스트

```bash
python scripts/garmin_auth.py
```

- **Pass**: `Login OK! Devices: [...]` 출력
- **Fail (인증)**: 이메일/비밀번호 재확인 요청
- **Fail (MFA/CAPTCHA)**: https://connect.garmin.com 에서 브라우저 로그인 후 재시도 안내

### Step 5: 첫 데이터 동기화

```bash
python scripts/garmin_sync.py
```

- **Pass**: 러닝 활동 또는 "No running activities" + 건강 지표 출력
- **Fail (토큰 만료)**: `~/.garminconnect/` 삭제 후 Step 4 재실행

주간 리포트도 생성:
```bash
python scripts/garmin_sync.py --week
```

`data/health/` 또는 `data/training/`에 파일이 생성되었는지 확인.

### Step 6: 텔레그램 채널 설정

이 시스템은 `claude --channels`를 통해 텔레그램과 연결된다.

#### 6-1. 사전 확인

Bun 설치 확인:
```bash
bun --version
```
- **Fail**: `curl -fsSL https://bun.sh/install | bash` 설치 안내

Telegram 플러그인 설치:
```
/plugin marketplace update claude-plugins-official
/plugin install telegram@claude-plugins-official
/reload-plugins
```

#### 6-2. 봇 토큰 등록

`[ASK USER]` 봇 토큰을 물어본다. 없으면 [@BotFather](https://t.me/BotFather)에서 `/newbot`으로 생성하라고 안내.

토큰을 받으면:
```
/telegram:configure <BOT_TOKEN>
```

이 명령은 토큰을 `~/.claude/channels/telegram/.env`에 저장한다.

#### 6-3. 채널 모드로 재시작

토큰 등록 후, 현재 세션을 종료하고 `--channels` 플래그로 재시작해야 한다.
**이 단계가 없으면 텔레그램 메시지를 수신할 수 없다.**

`[ASK USER]` 아래 안내를 **그대로** 전달한다:

```
✅ 텔레그램 봇 토큰이 등록되었습니다!

이제 텔레그램 채널을 연결하기 위해 Claude Code를 재시작해야 합니다.
아래 두 단계를 따라해주세요:

1. 현재 세션을 종료합니다 (Ctrl+C 또는 /exit)
2. 터미널에서 아래 명령어를 실행합니다:

   cd Oh-My-GCoach
   claude --channels plugin:telegram@claude-plugins-official

재시작 후 "설치 이어서 해줘"라고 입력하면 나머지 설정을 자동으로 진행합니다.
```

> 재시작 후 이 프로토콜의 Step 6-4부터 이어서 진행한다.
> 사용자가 "설치 이어서 해줘" 또는 유사한 요청을 하면, Step 6-4로 점프한다.

#### 6-4. 페어링

`[ASK USER]` 텔레그램에서 봇에게 아무 메시지를 보내라고 안내.

봇이 페어링 코드를 응답한다. 사용자에게 코드를 알려달라고 한 뒤:

```
/telegram:access pair <페어링코드>
```

페어링 완료 후 접근 정책을 allowlist로 설정:
```
/telegram:access policy allowlist
```

#### 6-5. 테스트

`mcp__plugin_telegram_telegram__reply`를 사용해 테스트 메시지를 전송하여 연결을 확인한다.

### Step 7: 러너 프로필 수집

`data/profile/runner_profile.example.md`를 템플릿으로 참조하여, 사용자와 대화를 통해 프로필을 수집한다.

`[ASK USER]` 아래 항목을 **하나의 메시지로 묶어서** 자연스럽게 질문한다:

1. **기본 정보**: 이름, 나이, 성별, 러닝 경력, 주간 러닝 횟수/볼륨
2. **추구하는 방향**: 마라톤 기록 단축? 건강 유지? 트레일? 울트라?
3. **목표 기록**: 종목별(5K/10K/하프/풀) 현재 기록과 목표 기록
4. **예정된 대회**: 대회명, 날짜, 종목, 목표
5. **부상 이력 & 주의사항**: 과거 부상, 현재 통증 부위 등
6. **훈련 환경**: 선호 시간대, 장소, 가능한 요일

수집한 정보를 `data/profile/runner_profile.md`에 저장한다.
모든 항목을 채울 필요는 없다 — 사용자가 모르거나 없다고 하면 빈칸으로 남긴다.

### Step 8: 히스토리 데이터 수집 & 스킬 그래프 생성

Garmin Connect에서 **최근 1년**의 러닝 데이터를 수집하고 분석한다.

#### 8-1. 데이터 수집

```bash
# 1년 전부터 오늘까지의 러닝 활동 조회
python scripts/garmin_sync.py --range <1년전 날짜> <오늘 날짜>
```

추가로 아래 데이터를 직접 API로 수집한다 (garmin_sync.py의 기능 활용):
- 최근 12개월의 주간 볼륨 추이
- 심박 존 분포 (활동별)
- 레이스 예측 기록
- 체중 변화 추이

> 데이터가 많으면 3~4개월 단위로 나눠서 조회한다.
> API 에러 시 기간을 줄여서 재시도한다.

#### 8-2. 분석 & 스킬 그래프 작성

수집된 데이터를 기반으로 `data/profile/skill_graph.example.md` 템플릿을 참조하여
`data/profile/skill_graph.md`를 작성한다.

분석해야 할 항목:

1. **볼륨 프로필**: 주간 평균/최대 거리, 세션 수, 10% 룰 준수율, 볼륨 트렌드
2. **페이스 프로필**: 존별 페이스 범위, 80/20 비율, 이지런 페이스 트렌드
3. **심박 프로필**: RHR 평균/트렌드, HRV 평균/트렌드, 심박 존 시간 분포
4. **건강 & 회복**: 평균 수면, 체중 변화, 스트레스/바디배터리 평균
5. **레이스 예측**: Garmin 예측 vs 사용자 목표 기록 갭 분석
6. **강점 & 약점**: 데이터 기반 강점 3가지, 개선 필요 영역 3가지
7. **코칭 권장사항**: 단기(4주)/중기(3개월)/장기(6개월+) 방향 제시

> `runner_profile.md`의 사용자 목표와 대조하여 권장사항을 작성한다.

#### 8-3. 결과 전달

텔레그램으로 **3개의 메시지로 나누어** 상세 분석 결과를 전달한다.

**메시지 1: 전체 요약 & 볼륨/페이스 분석**

```
📊 지난 1년 훈련 분석 리포트 (1/3)

📅 분석 기간: YYYY-MM-DD ~ YYYY-MM-DD
🏃 총 활동: N회 | 총 거리: N km | 총 시간: N시간

━━ 볼륨 프로필 ━━
• 주간 평균: N km / N회
• 최대 주간: N km (YYYY-WNN)
• 최근 4주 평균: N km (전체 평균 대비 ↑↓)
• 볼륨 트렌드: 증가/유지/감소
• 10% 룰 준수율: N%
• 평균 연속 훈련: N주 (디로드 주기: N주마다)

━━ 페이스 프로필 ━━
• 이지런 평균: M'SS"/km (최근 트렌드: ↑↓→)
• 템포런 평균: M'SS"/km
• 인터벌 평균: M'SS"/km
• 최고 페이스: M'SS"/km (날짜)

━━ 강도 분배 (80/20) ━━
• Easy (Z1+Z2): N%
• Hard (Z3+Z4+Z5): N%
• 평가: 양호/개선필요/과훈련위험
```

**메시지 2: 심박 & 건강/회복 분석**

```
📊 지난 1년 훈련 분석 리포트 (2/3)

━━ 심박 프로필 ━━
• 안정시 심박 (RHR): 평균 N bpm (범위 N~N)
• RHR 트렌드: 하락↓/유지→/상승↑
• HRV 평균: N ms
• HRV 트렌드: 상승↑/유지→/하락↓
• 최대 심박: N bpm

━━ 건강 & 회복 ━━
• 평균 수면: N시간 N분
• 7.5h+ 비율: N%
• 체중: N kg → N kg (변화: ±N kg)
• 평균 스트레스: N
• 평균 바디배터리 (아침): N/100
• 훈련 준비도 평균: N

━━ 레이스 예측 (Garmin) ━━
• 5K: HH:MM:SS (목표: HH:MM:SS, 갭: ±M:SS)
• 10K: HH:MM:SS (목표: HH:MM:SS, 갭: ±M:SS)
• 하프: H:MM:SS (목표: H:MM:SS, 갭: ±M:SS)
• 풀: H:MM:SS (목표: H:MM:SS, 갭: ±M:SS)
```

**메시지 3: 강점/약점 & 코칭 방향**

```
📊 지난 1년 훈련 분석 리포트 (3/3)

━━ 강점 💪 ━━
1. [데이터 기반 구체적 강점]
2. [데이터 기반 구체적 강점]
3. [데이터 기반 구체적 강점]

━━ 개선 필요 📌 ━━
1. [데이터 기반 구체적 약점 + 개선 방향]
2. [데이터 기반 구체적 약점 + 개선 방향]
3. [데이터 기반 구체적 약점 + 개선 방향]

━━ 코칭 방향 🎯 ━━

▸ 단기 (4주)
  [구체적 훈련 조정 사항]

▸ 중기 (3개월)
  [목표 달성을 위한 단계별 계획 방향]

▸ 장기 (6개월+)
  [최종 목표를 향한 큰 그림]

━━━━━━━━━━━━━━━━━
설치 완료! 앞으로 이 채팅에서 자유롭게 질문하세요.
"오늘 컨디션 체크해줘", "이번 주 리포트 만들어줘" 등
자연어로 메시지를 보내면 AI 코치가 응답합니다.
```

> 각 메시지의 수치는 실제 분석 데이터로 채운다.
> 목표 기록이 없는 종목은 레이스 예측에서 생략한다.
> 데이터가 부족한 항목은 "데이터 부족"으로 표시하고 생략하지 않는다.

### Step 9: Coach Agent 확인

`.claude/agents/coach-agent.md` 파일 존재 확인.

```
@coach-agent 현재 사용 가능한 데이터 확인해줘
```

### Step 10: 완료 안내

`[ASK USER]` 아래 안내를 **Claude Code 세션에서** 전달한다:

```
설치가 모두 완료되었습니다!

앞으로 코칭 세션을 시작할 때는 아래 명령으로 실행하세요:

  cd Oh-My-GCoach
  claude --channels plugin:telegram@claude-plugins-official

이 명령으로 시작해야 텔레그램 메시지를 수신할 수 있습니다.

항상 켜두려면:
  tmux new-session -d -s gcoach "cd Oh-My-GCoach && claude --channels plugin:telegram@claude-plugins-official"
```

---

## 참조

### 데이터 구조

```
data/
├── index.md                 # 데이터 파일 인덱스 (coach-agent가 먼저 읽음)
├── knowledge/               # 러닝 & 건강 지식 베이스 (과학적 원칙)
│   ├── training_principles.md   # 주기화, 볼륨, 강도, 테이퍼링
│   ├── recovery_health.md       # 수면, HRV, RHR, 부상 예방
│   └── race_strategy.md         # 종목별 전략, 페이스, 보급
├── profile/
│   ├── runner_profile.md    # 사용자 목표, 대회, 부상 이력 (초기 설정 시 생성)
│   └── skill_graph.md       # 1년치 데이터 기반 실력 분석 (주기적 업데이트)
├── training/                # 주간 리포트 (YYYY-WNN-weekly-report.md)
├── health/                  # 월별 회복 지표 (YYYY-MM-recovery.md)
├── races/                   # 대회 기록 및 분석
└── plans/                   # 훈련 계획
```

### 코칭 방식

고정된 규칙이 아닌, **지식 + 개인 데이터 기반 동적 코칭**을 제공합니다.

```
knowledge/ (과학적 원칙·가이드라인 범위)
    ×
profile/ (사용자 목표·실력 기준선)
    ×
health/ + training/ (현재 상태·최근 데이터)
    ↓
맞춤 코칭 판단
```

| 원칙 | 설명 |
|------|------|
| **데이터 기반** | 모든 인사이트는 Garmin 데이터로 뒷받침 |
| **개인화** | 고정 임계값 없이, 사용자의 개인 데이터 패턴에 맞춰 판단 |
| **시기 인식** | 훈련 시기(기초기/강화기/대회준비기/테이퍼/회복기)에 따라 기준이 달라짐 |
| **목표 정렬** | 모든 조언은 사용자의 목표와 대회 일정에 맞춤 |

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
