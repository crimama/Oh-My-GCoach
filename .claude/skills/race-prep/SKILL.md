---
name: race-prep
description: 예정된 대회에 맞춘 준비 전략을 수립한다. 대회 전 테이퍼링, 페이스 전략, 보급 계획, D-day 루틴을 포함. 사용자가 "대회 준비", "레이스 전략" 등을 요청할 때 사용.
argument-hint: [대회명 또는 날짜]
allowed-tools: Bash(python*), Read, Write, Edit, Glob, Grep
---

# Race Preparation Strategy

## 입력 확인

`$ARGUMENTS`가 제공되면 해당 대회 정보를 사용.
없으면 `data/profile/runner_profile.md`에서 가장 가까운 예정 대회를 자동 선택.

## 실행 순서

### 1. 즉시 확인 응답
텔레그램으로 "대회 준비 전략을 수립합니다 ⏳" 전송.

### 2. 정보 수집

- `data/profile/runner_profile.md` → 대회 정보 (날짜, 종목, 목표 기록)
- `data/profile/skill_graph.md` → 현재 실력 수준, 레이스 예측
- `data/knowledge/race_strategy.md` → 종목별 전략 가이드라인
- `data/knowledge/training_principles.md` → 테이퍼링 원칙
- `data/training/` → 최근 훈련 상태

### 3. D-day까지 남은 기간 계산

남은 기간에 따라 전략 범위가 달라진다:

| 남은 기간 | 전략 범위 |
|----------|----------|
| 4주+ | 마무리 훈련 + 테이퍼 계획 |
| 2~4주 | 테이퍼링 전략 |
| 1~2주 | 세부 테이퍼 + 보급/루틴 |
| 1주 미만 | D-day 루틴 + 페이스 전략 |

### 4. 전략 수립

#### 테이퍼링 계획
`knowledge/training_principles.md`의 테이퍼링 섹션 참조:
- 종목별 테이퍼 기간 (5K: 1주, 10K: 1~2주, 하프: 2주, 풀: 2~3주)
- 볼륨 감소 스케줄 (주차별 %)
- 강도는 유지, 볼륨만 감소

#### 페이스 전략
`knowledge/race_strategy.md` 참조:
- 목표 기록 기반 구간별 페이스 설정
- negative split vs even split 판단
- 현재 실력(skill_graph) 대비 목표의 현실성 평가
- 목표가 비현실적이면 대안 제시

#### 보급 계획
- 종목별 수분/에너지 보급 타이밍
- 풀마라톤: 구간별 젤/수분 계획

#### D-day 루틴
- D-7 ~ D-1 일별 가이드
- 레이스 당일 아침 루틴 (기상, 식사, 워밍업)

### 5. 전략 저장
`data/plans/<대회명>-race-prep.md`에 저장.

### 6. 텔레그램 전달

```
🏁 [대회명] 대회 준비 전략

📅 D-day: YYYY-MM-DD (D-X)
🎯 목표: [종목] [목표 기록]
📊 현재 예측: [Garmin 예측 기록]

⏬ 테이퍼링
- [주차별 볼륨 감량 계획]

🏃 페이스 전략
- [구간별 목표 페이스]

🥤 보급 계획
- [타이밍별 보급 내용]

📋 D-day 루틴
- [당일 아침 일정]

자세한 전략은 저장해두었습니다.
궁금한 부분이 있으면 물어보세요!
```
