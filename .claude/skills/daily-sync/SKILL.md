---
name: daily-sync
description: 오늘 Garmin 데이터를 동기화하고 컨디션을 체크한 뒤 텔레그램으로 전달한다. 매일 아침 루틴 또는 사용자가 "오늘 컨디션", "오늘 분석" 등을 요청할 때 사용.
allowed-tools: Bash(python*), Read, Write, Edit, Glob, Grep
---

# Daily Sync & Condition Check

## 실행 순서

### 1. 즉시 확인 응답
텔레그램으로 "확인했습니다, 오늘 데이터 동기화 중입니다 ⏳" 전송.

### 2. 데이터 동기화
```bash
python scripts/garmin_sync.py
```

### 3. 데이터 읽기
- `data/index.md`를 참조하여 오늘 날짜의 건강 데이터 파일을 찾는다.
- `data/health/YYYY-MM-recovery.md`에서 오늘 건강 지표를 읽는다.
- `data/profile/runner_profile.md`에서 사용자 컨텍스트를 확인한다.

### 4. 컨디션 분석
`data/knowledge/recovery_health.md`를 참조하여 아래 항목을 평가:

- **수면**: 시간, 품질, 최근 트렌드 대비
- **HRV**: 7일 평균 대비 오늘 수치
- **안정시 심박**: 평소 대비 변화
- **스트레스 / 바디배터리**: 아침 수치
- **훈련 준비도**: Garmin 지표

### 5. 훈련 추천
`data/knowledge/training_principles.md`와 `data/profile/skill_graph.md`를 참조하여:

- 오늘 컨디션에 맞는 훈련 유형 추천 (이지런/템포/인터벌/휴식)
- 추천 강도와 거리 범위
- 주의사항 (부상 이력, 피로도 등)

### 6. 텔레그램 전달
아래 포맷으로 텔레그램 전송:

```
📊 [날짜] 일일 컨디션 체크

수면: X시간 Xmin (품질: 양호/주의)
HRV: Xms (평소 대비 ↑↓→)
안정시 심박: Xbpm
바디배터리: X/100
훈련 준비도: X

💡 오늘 추천: [훈련 유형]
[구체적 추천 내용]

⚠️ 주의: [해당 시에만]
```
