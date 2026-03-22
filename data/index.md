# Data Index

> Claude가 데이터에 접근할 때 이 파일을 먼저 읽는다.
> 각 파일의 용도와 경로를 정리하여 빠르게 필요한 데이터를 찾는다.

## 사용자 프로필

| 파일 | 용도 | 참조 시점 |
|------|------|----------|
| `profile/runner_profile.md` | 사용자 목표, 대회 일정, 부상 이력, 훈련 환경 | 조언/계획 수립 전 항상 |
| `profile/skill_graph.md` | 1년치 데이터 기반 실력 분석 (볼륨/페이스/심박/강점·약점) | 계획 수립, 진행 상황 평가 시 |

## 지식 베이스 (Knowledge Base)

| 파일 | 내용 | 참조 시점 |
|------|------|----------|
| `knowledge/training_principles.md` | 주기화, 볼륨 관리, 강도 분배, 핵심 훈련 유형, 테이퍼링 | 훈련 계획 수립, 볼륨/강도 판단 시 |
| `knowledge/recovery_health.md` | 수면, HRV, RHR 해석, 스트레스, 영양, 부상 예방 | 회복 상태 평가, 컨디션 체크 시 |
| `knowledge/race_strategy.md` | 종목별 페이스 전략, 대회 준비, 보급, 기록 분석 | 대회 관련 조언 시 |

> 지식 베이스는 과학적 원칙과 가이드라인 범위를 제공한다.
> 코칭 판단은 이 범위 내에서 사용자의 개인 데이터(profile + health + training)에 맞춰 동적으로 이루어진다.

## 훈련 데이터

| 파일 패턴 | 용도 | 예시 |
|----------|------|------|
| `training/YYYY-WNN-weekly-report.md` | 주간 훈련 리포트 (거리, 세션, 80/20, 볼륨 비교) | `training/2026-W12-weekly-report.md` |

## 건강 & 회복

| 파일 패턴 | 용도 | 예시 |
|----------|------|------|
| `health/YYYY-MM-recovery.md` | 월별 일일 회복 지표 (수면, HRV, 체중, 스트레스, 바디배터리) | `health/2026-03-recovery.md` |

## 대회 기록

| 파일 패턴 | 용도 | 예시 |
|----------|------|------|
| `races/<대회명>.md` | 대회 결과 분석, 구간 기록, 회고 | `races/2026-서울마라톤.md` |

## 훈련 계획

| 파일 패턴 | 용도 | 예시 |
|----------|------|------|
| `plans/<계획명>.md` | 대회 목표 기반 주차별 훈련 계획 | `plans/2026-하프마라톤-12주.md` |

## 빠른 접근 가이드

```
오늘 컨디션 체크     → health/YYYY-MM-recovery.md + knowledge/recovery_health.md
이번 주 훈련 분석    → training/YYYY-WNN-weekly-report.md + knowledge/training_principles.md
사용자 목표 확인     → profile/runner_profile.md
실력 기준선 확인     → profile/skill_graph.md
훈련 계획 수립       → profile/ + knowledge/training_principles.md + plans/
대회 준비 상황       → profile/runner_profile.md + knowledge/race_strategy.md + plans/
지난 대회 리뷰       → races/ + knowledge/race_strategy.md
```
