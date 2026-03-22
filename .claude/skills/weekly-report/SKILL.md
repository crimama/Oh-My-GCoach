---
name: weekly-report
description: 이번 주 훈련 데이터를 분석하여 주간 리포트를 생성하고 텔레그램으로 전달한다. 사용자가 "주간 리포트", "이번 주 분석" 등을 요청할 때 사용.
allowed-tools: Bash(python*), Read, Write, Edit, Glob, Grep
---

# Weekly Training Report

## 실행 순서

### 1. 즉시 확인 응답
텔레그램으로 "네, 이번 주 훈련 리포트 준비할게요 ⏳" 전송.

### 2. 주간 데이터 동기화
```bash
python scripts/garmin_sync.py --week
```

### 3. 데이터 수집
- `data/index.md` 참조하여 이번 주 리포트 파일 위치 확인
- `data/training/YYYY-WNN-weekly-report.md` 읽기
- `data/health/YYYY-MM-recovery.md`에서 이번 주 건강 지표 읽기
- `data/profile/runner_profile.md`에서 목표 확인
- `data/profile/skill_graph.md`에서 기준선 확인

### 4. 분석 항목

`data/knowledge/training_principles.md`를 참조하여:

#### 볼륨 분석
- 이번 주 총 거리, 세션 수, 총 시간
- 지난주 대비 증감률 (10% 룰 체크)
- skill_graph 기준 평균 대비 위치

#### 강도 분배
- 심박 존별 시간 분포
- Easy(Z1+Z2) : Hard(Z3+Z4+Z5) 비율
- 현재 훈련 시기에 맞는 적정 비율 대비 평가

#### 핵심 훈련 리뷰
- 이번 주 가장 좋은 훈련 (페이스/심박 효율)
- 가장 힘든 훈련 (회복 필요도)
- 롱런 여부 및 거리

#### 회복 트렌드
- 주간 평균 수면, HRV, RHR
- 주 초반 vs 후반 회복 상태 변화

#### 다음 주 방향
- 볼륨 추천 (유지/증가/디로드)
- 핵심 훈련 제안
- 대회 일정 고려 사항

### 5. 리포트 저장
분석 결과를 `data/training/YYYY-WNN-weekly-report.md`에 업데이트.

### 6. 텔레그램 전달
아래 포맷으로 전송:

```
📋 [기간] 주간 훈련 리포트

🏃 볼륨: X km / X회 (지난주 대비 +X%)
⏱ 존 분포: Easy X% / Hard X%
😴 회복: 수면 평균 X시간, HRV 평균 Xms

🔑 이번 주 하이라이트
- [핵심 훈련 요약]

📌 다음 주 방향
- [볼륨/강도 추천]
- [핵심 훈련 제안]

⚠️ 주의사항
- [해당 시에만]
```
