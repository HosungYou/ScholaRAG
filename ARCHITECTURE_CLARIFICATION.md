# ScholaRAG Architecture Clarification
**Date**: 2025-10-31
**Author**: Design Review
**Status**: Implemented

---

## 📊 파일 역할 명확화

### 현재 파일 구조

| 파일 | 대상 사용자 | 트리거 방식 | 주요 역할 | 라인 수 |
|------|------------|------------|----------|---------|
| **CLAUDE.md** | Claude Code | 자동 (프로젝트 디렉토리 감지) | 전체 프로젝트 행동 지침 | 351 |
| **AGENTS.md** | Codex/Cursor/Copilot | 수동 (파일 명시적 읽기) | 터미널 중심 작업 가이드 | 873 |
| **SKILL.md** | Claude Code | 명시적 호출 | 대화 중심 심층 가이드 | 382 |
| **prompts/*.md** | Researchers | 복사/붙여넣기 | 단계별 대화 템플릿 | 7 files |

---

## 🔍 발견된 문제점

### 1. **SKILL.md vs CLAUDE.md 역할 중복**

**문제:**
- 둘 다 Claude Code를 대상으로 함
- 역할 구분이 불명확
- 언제 무엇을 읽어야 하는지 혼란

**해결:**
```
CLAUDE.md (Keep as is)
- 목적: 빠른 참조, 핵심 워크플로우
- 트리거: 프로젝트 디렉토리 진입 시 자동
- 내용: 기본 개념, Stage 1-7 개요

SKILL.md (Redirect role)
- 목적: 심층 참조 (on-demand)
- 트리거: Claude Code가 필요 시 명시적 호출
- 내용: 엣지 케이스, 트러블슈팅, 고급 시나리오
```

### 2. **project_type 선택 누락**

**문제:**
- CLI는 `--project-type` prompt 있음 (scholarag_cli.py:36-40)
- CLAUDE.md는 "자동으로 입력하라"고 지시 (line 107-109)
- **결과**: 사용자에게 묻지 않고 기본값(systematic_review) 사용

**해결:**
- CLAUDE.md에 **"ALWAYS ask user to choose project_type"** 추가 ✅
- AGENTS.md에도 동일 지침 추가 ✅
- Stage 1 예제 워크플로우에 명시적 질문 단계 추가 ✅

### 3. **project_type 오해: 초기 검색 수 차이로 착각**

**잘못된 이해:**
- knowledge_repository → 10K-20K papers 검색
- systematic_review → 50-300 papers 검색

**정확한 로직:**
- 둘 다 10K-20K papers 검색 (Stage 1 동일)
- 차이는 Stage 3 (AI screening threshold):
  - knowledge_repository: 50% threshold → 5K-15K papers 남음
  - systematic_review: 90% threshold → 50-300 papers 남음

**업데이트 완료:**
- CLAUDE.md Scenario 2에 명확한 설명 추가 ✅
- AGENTS.md Quick Context에 경고 추가 ✅

---

## 🔄 Prompts ↔ Scripts 연계 흐름

### 현재 흐름 (문제 있음)

```
[Researcher] 복사/붙여넣기
    ↓
[prompts/01_research_domain_setup.md]
    ↓ metadata:
    cli_commands: "scholarag init"
    auto_execute: true
    ↓
[Claude Code 읽음]
    ↓
[CLAUDE.md 지침: "echo로 자동 입력"]
    ↓
❌ project_type 건너뜀!
    ↓
[scholarag_cli.py]
    default='systematic_review'  # 기본값 사용됨
```

### 개선된 흐름 (목표)

```
[Researcher] 복사/붙여넣기
    ↓
[prompts/01_research_domain_setup.md]
    ↓ metadata (업데이트 필요):
    conversation_flow:
      - turn: 3
        user_action: "Choose project_type"
        claude_action: "Present both options, explain differences"
    ↓
[Claude Code]
    "I need to know your project type:
     Option 1: knowledge_repository (5K-15K papers)
     Option 2: systematic_review (50-300 papers)
     Which matches your goals?"
    ↓
[Researcher 선택]
    "Option 1"
    ↓
[Claude Code 실행]
    python scholarag_cli.py init \
      --project-type knowledge_repository  # ← USER CHOICE
```

---

## 📝 추가 필요한 업데이트

### 1. **prompts/01_research_domain_setup.md 수정**

현재 metadata에 project_type 질문 없음. 추가 필요:

```markdown
<!-- METADATA
stage: 1
conversation_flow:
  expected_turns: 4-8
  typical_pattern:
    - turn: 1
      user_action: "Provides research topic"
      claude_action: "Ask clarifying questions"
    - turn: 2
      claude_action: "Validate scope"
    - turn: 3  # ← 추가
      claude_action: "Present project_type options (MANDATORY)"
      user_action: "Choose knowledge_repository or systematic_review"
    - turn: 4
      claude_action: "Execute scholarag init with user choice"
validation_checklist:
  - research_question_clear: true
  - project_type_explicitly_chosen: true  # ← 추가
  - databases_selected: true
-->
```

### 2. **SKILL.md vs CLAUDE.md 명확화**

**제안: SKILL.md 앞부분에 명시**

```markdown
# SKILL.md - Claude Code Deep Dive

⚠️  **When to read this file**:
- This is an **on-demand reference**, NOT auto-loaded
- **Start with CLAUDE.md** (auto-loaded when entering ScholaRAG/)
- **Come here** when you need:
  - Edge case handling
  - Advanced troubleshooting
  - Detailed examples

**For quick start**: See [CLAUDE.md](CLAUDE.md) instead.
```

---

## 🎯 SKILL.md vs AGENTS.md vs CLAUDE.md 비교표

| Aspect | CLAUDE.md | AGENTS.md | SKILL.md |
|--------|-----------|-----------|----------|
| **대상** | Claude Code | Codex/Cursor | Claude Code |
| **트리거** | 자동 (디렉토리 진입) | 수동 (파일 읽기) | 명시적 호출 |
| **스타일** | 간결, 빠른 참조 | 터미널 명령 중심 | 대화 예제 중심 |
| **길이** | 351 lines (짧음) | 873 lines (긴 체크리스트) | 382 lines (중간) |
| **내용** | 핵심 워크플로우 | Bash scripts, validation | 엣지 케이스, 예제 |
| **로딩** | 프로젝트 시작 시 | 명령 실행 시 | 필요 시 on-demand |
| **충돌** | ❌ 없음 | ❌ 없음 | ⚠️ CLAUDE.md와 역할 중복 |

---

## ✅ 구현 완료 사항

### 1. CLAUDE.md 업데이트 ✅
- Line 21: "ALWAYS ask user to choose project_type" 추가
- Line 28: "Auto-select project_type without confirmation" 금지 명시
- Line 198-228: Stage 1 예제에 명시적 project_type 질문 추가
- Line 234-250: project_type 차이 명확한 설명 (초기 검색 수 동일 강조)

### 2. AGENTS.md 업데이트 ✅
- Line 85-100: Quick Context 섹션 재작성
- "ALWAYS present both options" 명시
- 초기 검색 수 동일함을 강조

---

## 📋 향후 작업 (TODO)

### 1. prompts/01_research_domain_setup.md 업데이트
- [ ] metadata에 turn 3 추가 (project_type 질문)
- [ ] validation_checklist에 project_type_explicitly_chosen 추가
- [ ] 예제 대화에 project_type 선택 단계 포함

### 2. SKILL.md 역할 명확화
- [ ] 파일 앞부분에 "When to read this file" 섹션 추가
- [ ] CLAUDE.md와의 관계 명시
- [ ] On-demand loading 설명

### 3. Scripts 개선
- [ ] 03_screen_papers.py: .env 로딩 버그 수정 (이미 수정됨)
- [ ] 01_fetch_papers.py: .env 로딩 개선 (이미 수정됨)
- [ ] 모든 scripts에 project .env 우선 로딩 로직 추가

---

## 🔧 기술적 세부사항

### .env 파일 로딩 우선순위

**올바른 순서:**
1. Project-level `.env` (projects/YYYY-MM-DD_Name/.env)
2. ScholaRAG root `.env` (ScholaRAG/.env)
3. System environment variables

**구현 (Python):**
```python
from pathlib import Path
from dotenv import load_dotenv

# 1. Try project .env first
project_env = Path(project_path) / ".env"
if project_env.exists():
    load_dotenv(project_env)
else:
    # 2. Fallback to root .env
    root_env = Path(__file__).parent.parent / ".env"
    if root_env.exists():
        load_dotenv(root_env)
    else:
        # 3. Use system env vars
        load_dotenv()
```

---

## 📊 영향 받는 파일 요약

| 파일 | 수정 상태 | 변경 내용 |
|------|-----------|----------|
| CLAUDE.md | ✅ 완료 | project_type 질문 의무화, 예제 추가 |
| AGENTS.md | ✅ 완료 | Quick Context 재작성, 검색 수 동일 강조 |
| SKILL.md | ⏳ 대기 | On-demand loading 설명 추가 필요 |
| prompts/01_research_domain_setup.md | ⏳ 대기 | Metadata turn 3 추가 필요 |
| scripts/03_screen_papers.py | ✅ 완료 | .env 로딩 개선 |
| scripts/01_fetch_papers.py | ✅ 완료 | .env 로딩 개선 |

---

## 🎓 디자인 원칙 재확인

### 1. **Explicit over Implicit**
- ❌ 기본값 자동 선택
- ✅ 사용자에게 명시적 질문

### 2. **Stage Transparency**
- 사용자는 항상 현재 Stage 번호를 알아야 함
- 각 Stage의 목적과 출력을 명확히 이해

### 3. **No Hidden Costs**
- API 비용보다는 **선택의 영향** 설명에 집중
- Claude Code 사용자는 이미 로그인했으므로 비용 설명 불필요

### 4. **Workflow Consistency**
- Claude Code (CLAUDE.md) vs Codex (AGENTS.md) 동일한 논리
- Prompts metadata와 Code 행동 일치

---

## 📞 질문 및 답변

### Q: SKILL.md와 CLAUDE.md 중복 문제는?

**A**: SKILL.md를 on-demand reference로 재정의.
- CLAUDE.md: 자동 로드, 빠른 시작
- SKILL.md: 명시적 호출, 심층 가이드

### Q: Prompts와 Scripts 연계가 느슨한데?

**A**: prompts/*.md metadata에 더 상세한 `conversation_flow` 추가 필요.
현재는 CLAUDE.md에만 의존하는 구조.

### Q: 왜 project_type을 자동으로 선택하지 않았나?

**A**: 디자이너의 의도를 잘못 이해함.
- CLI에는 prompt 있음 (scholarag_cli.py:36)
- 하지만 CLAUDE.md가 "echo로 건너뛰라"고 지시
- **수정**: "ALWAYS ask user" 명시

---

**마지막 업데이트**: 2025-10-31
**다음 리뷰**: prompts/*.md metadata 업데이트 후
