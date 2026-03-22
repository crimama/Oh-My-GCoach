# Data Index

> Claude가 데이터에 접근할 때 이 파일을 먼저 읽는다.
> 각 파일의 용도와 경로를 정리하여 빠르게 필요한 데이터를 찾는다.

## 사용자 프로필

| 파일 | 용도 | 참조 시점 |
|------|------|----------|
| `profile/runner_profile.md` | 사용자 목표, 대회 일정, 부상 이력, 훈련 환경 | 조언/계획 수립 전 항상 |
| `profile/skill_graph.md` | 1년치 데이터 기반 실력 분석 (볼륨/페이스/심박/강점·약점) | 계획 수립, 진행 상황 평가 시 |

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
오늘 컨디션 체크     → health/YYYY-MM-recovery.md (해당 월)
이번 주 훈련 분석    → training/YYYY-WNN-weekly-report.md (해당 주)
사용자 목표 확인     → profile/runner_profile.md
실력 기준선 확인     → profile/skill_graph.md
대회 준비 상황       → profile/runner_profile.md (예정 대회) + plans/
지난 대회 리뷰       → races/
```
