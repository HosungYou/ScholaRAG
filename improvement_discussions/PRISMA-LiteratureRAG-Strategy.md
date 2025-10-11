# PRISMA 파이프라인 통합: Literature Review RAG 개선 전략

## 📋 Executive Summary

**목표**: AI failure_HR 프로젝트의 PRISMA 스크리닝 방법론을 Literature Review RAG에 통합하여 **문헌 품질 자동 필터링** 및 **체계적 문헌고찰(Systematic Review)** 기능 제공

**현재 문제점**:
1. ✗ 업로드된 PDF를 무분별하게 임베딩 (품질 검증 없음)
2. ✗ 중복 문헌 탐지/제거 로직 부재
3. ✗ 연구 주제와 관련성 점수화 시스템 없음
4. ✗ HRM/HRD 같은 도메인별 분류 기능 부재
5. ✗ 임시 업로드 폴더 정리 누락 ([app.py:115](01_literature_review_rag/app.py#L115))

**기대 효과**:
- ✅ 연구 주제 관련성 기반 자동 필터링 (PRISMA Stage 1-4)
- ✅ 문헌 품질 점수 시각화 (relevance score dashboard)
- ✅ 저품질 문헌 자동 제외 및 재검토 큐 관리
- ✅ 도메인별 문헌 분류 (HRM/HRD/Both 등 확장 가능)
- ✅ PRISMA 플로우 다이어그램 자동 생성

---

## 🏗️ 아키텍처 설계

### 1. 모듈 구조 (신규 추가)

```
01_literature_review_rag/
├── backend/
│   ├── core/
│   │   ├── ingestion.py          # 기존
│   │   ├── retrieval.py           # 기존
│   │   ├── prisma_pipeline.py     # 🆕 PRISMA 스크리닝 파이프라인
│   │   └── quality_control.py     # 🆕 품질 관리 시스템
│   ├── models/
│   │   ├── document.py            # 기존
│   │   └── prisma_screening.py    # 🆕 스크리닝 결과 모델
│   └── utils/
│       ├── deduplication.py       # 🆕 중복 제거 유틸
│       └── scoring.py             # 🆕 관련성 점수 계산
├── data/
│   ├── raw_pdfs/
│   ├── screening/                 # 🆕 PRISMA 단계별 결과
│   │   ├── 01_identification/
│   │   ├── 02_screening/
│   │   ├── 03_eligibility/
│   │   └── 04_included/
│   └── vector_db/
└── tests/
    └── test_prisma.py             # 🆕 PRISMA 테스트
```

### 2. 데이터 플로우

```
📤 PDF Upload
    ↓
[1] Identification Stage
    - 파일 메타데이터 추출 (제목, 저자, 연도, DOI)
    - 중복 체크 (DOI/제목 기반)
    - 초기 통계 생성
    ↓
[2] Screening Stage (Title/Abstract)
    - 도메인 키워드 매칭 (예: HR/HRD)
    - AI/ML 기술 키워드 확인
    - 연구 주제 키워드 매칭 (예: bias, fairness)
    - Exclusion 키워드 체크 (medical, pure tech)
    - 초기 관련성 점수 계산 (0-50점)
    ↓
[3] Eligibility Stage (Full-text)
    - 섹션 분석 (Abstract, Methods, Results)
    - 컨텍스트 검증 (도메인 용어 + HR 맥락)
    - 고급 점수 계산 (다차원 평가)
    - 최종 관련성 점수 (0-100점)
    ↓
[4] Inclusion Decision
    - 점수 임계값 적용 (기본: 60점)
    - 승인 → Vector DB 임베딩
    - 보류 → 수동 검토 큐
    - 제외 → 제외 사유 기록
    ↓
🗄️ Vector Database (고품질 문헌만)
```

---

## 🔬 핵심 구현: PRISMA 파이프라인

### 3.1 `backend/core/prisma_pipeline.py`

**설계 원칙**:
- AI failure_HR의 `PRISMAScreener` 클래스를 **문헌 리뷰용으로 재설계**
- **도메인 키워드를 설정 파일로 분리** (연구 주제별 커스터마이징 가능)
- **점진적 필터링** (각 단계별 저장 → 투명성)

**핵심 기능**:

```python
class LiteratureReviewPRISMA:
    """
    문헌 리뷰를 위한 PRISMA 스크리닝 시스템

    Features:
    - 연구 주제별 키워드 프로파일 지원
    - 다차원 점수 계산 (domain, methodology, quality)
    - 중복 제거 (DOI, semantic similarity)
    - PRISMA 플로우 다이어그램 자동 생성
    """

    def __init__(self, research_profile: ResearchProfile):
        """
        Args:
            research_profile: 연구 주제 정의
                - domain_keywords: 도메인 키워드 (예: ['HRM', 'employee'])
                - method_keywords: 방법론 키워드 (예: ['machine learning'])
                - topic_keywords: 주제 키워드 (예: ['bias', 'fairness'])
                - exclusion_keywords: 제외 키워드
                - min_score: 최소 포함 점수 (0-100)
        """

    def stage1_identification(self, documents: List[Document]) -> IdentificationResult:
        """
        Stage 1: 식별
        - DOI/제목 기반 중복 제거
        - 기본 메타데이터 검증
        - 연도/언어 필터링
        """

    def stage2_screening(self, docs: List[Document]) -> ScreeningResult:
        """
        Stage 2: 초기 스크리닝 (Title/Abstract)
        - 도메인 키워드 점수 (0-30점)
        - 방법론 키워드 점수 (0-20점)
        - 주제 키워드 점수 (0-20점)
        - 제외 키워드 체크 (-30점)
        - Title 보너스 (+10점)
        """

    def stage3_eligibility(self, docs: List[Document]) -> EligibilityResult:
        """
        Stage 3: 적격성 평가 (Full-text)
        - 섹션별 분석 (abstract, methods, results)
        - 컨텍스트 검증 (도메인 용어 밀도)
        - 인용 품질 평가
        - 저널 임팩트 고려 (optional)
        """

    def stage4_inclusion(self, docs: List[Document]) -> InclusionResult:
        """
        Stage 4: 최종 포함 결정
        - 임계값 적용
        - 수동 검토 큐 생성
        - PRISMA 플로우 다이어그램 생성
        """

    def calculate_relevance_score(self, doc: Document) -> ScoringBreakdown:
        """
        관련성 점수 계산 (0-100)

        반환:
            {
                'domain_score': 0-30,      # 도메인 키워드 매칭
                'method_score': 0-20,      # 방법론 키워드
                'topic_score': 0-20,       # 주제 키워드
                'context_score': 0-20,     # 맥락 검증
                'quality_score': 0-10,     # 품질 지표
                'exclusion_penalty': 0/-30, # 제외 키워드
                'total_score': 0-100
            }
        """
```

### 3.2 연구 프로파일 예시 (HRM/AI Bias 연구)

```python
# config/research_profiles/hrm_ai_bias.yaml

name: "HRM AI Bias Research"
description: "AI bias and fairness in HR practices"

domain_keywords:
  hrm:
    - "human resource management"
    - "employee selection"
    - "recruitment"
    - "hiring"
    - "performance appraisal"
    weight: 1.0

  hrd:
    - "employee training"
    - "learning and development"
    - "skill development"
    weight: 0.8

method_keywords:
  ai_ml:
    - "artificial intelligence"
    - "machine learning"
    - "algorithmic decision"
    - "automated hiring"
    weight: 1.0

topic_keywords:
  fairness:
    - "bias"
    - "discrimination"
    - "fairness"
    - "disparate impact"
    weight: 1.0

  ethics:
    - "ethics"
    - "transparency"
    - "accountability"
    weight: 0.9

exclusion_keywords:
  medical:
    - "alzheimer"
    - "clinical trial"
    - "patient care"
  technical:
    - "edge computing"
    - "IoT sensor"

scoring:
  min_score: 60          # 최소 포함 점수
  review_threshold: 50   # 수동 검토 필요 점수
  auto_exclude: 30       # 자동 제외 점수
```

---

## 🔧 구현 단계별 플랜

### Phase 1: 기반 시스템 구축 (1-2일)

#### 1.1 PRISMA 파이프라인 핵심 클래스
```bash
# 새 파일 생성
touch backend/core/prisma_pipeline.py
touch backend/models/prisma_screening.py
touch backend/utils/deduplication.py
touch config/research_profiles/default.yaml
```

**구현 내용**:
- [ ] `LiteratureReviewPRISMA` 클래스 (AI failure_HR 코드 변형)
- [ ] `ResearchProfile` 데이터 모델 (Pydantic)
- [ ] `ScoringEngine` (다차원 점수 계산)
- [ ] `DeduplicationEngine` (DOI + 시맨틱 유사도)

#### 1.2 통합 테스트
```python
# tests/test_prisma.py

def test_end_to_end_screening():
    """샘플 PDF 5개로 전체 파이프라인 검증"""

    # 연구 프로파일 로드
    profile = ResearchProfile.from_yaml("config/research_profiles/hrm_ai_bias.yaml")

    # PRISMA 파이프라인 초기화
    prisma = LiteratureReviewPRISMA(profile)

    # 문서 처리
    raw_docs = ingest_documents("tests/fixtures/sample_pdfs")

    # Stage 1-4 순차 실행
    stage1 = prisma.stage1_identification(raw_docs)
    assert stage1.duplicates_removed > 0

    stage2 = prisma.stage2_screening(stage1.documents)
    assert stage2.excluded_count > 0

    stage3 = prisma.stage3_eligibility(stage2.documents)
    assert all(doc.score >= 50 for doc in stage3.documents)

    stage4 = prisma.stage4_inclusion(stage3.documents)
    assert len(stage4.included_docs) > 0

    # PRISMA 플로우 생성
    assert stage4.flow_diagram_path.exists()
```

### Phase 2: Ingestion 파이프라인 개선 (2-3일)

#### 2.1 `backend/core/ingestion.py` 수정

**Before (현재)**:
```python
def upload_and_process(files):
    # 1. 파일 복사
    shutil.copy(file.name, temp_dir)

    # 2. 즉시 임베딩
    documents = ingest_documents(temp_dir)
    retriever.add_documents(documents)  # ❌ 품질 검증 없음
```

**After (PRISMA 통합)**:
```python
def upload_and_process_with_prisma(files, research_profile: str = "default"):
    # 1. 기본 인제스션
    raw_docs = ingest_documents(temp_dir)

    # 2. PRISMA 스크리닝 적용
    profile = ResearchProfile.from_yaml(f"config/research_profiles/{research_profile}.yaml")
    prisma = LiteratureReviewPRISMA(profile)

    result = prisma.run_full_pipeline(raw_docs)

    # 3. 포함된 문서만 Vector DB에 추가
    retriever.add_documents(result.included_docs)

    # 4. 결과 저장
    result.save_to_disk("data/screening/")

    # 5. 상태 반환
    return {
        'total_uploaded': len(files),
        'after_dedup': result.stage1.unique_count,
        'after_screening': result.stage2.passed_count,
        'after_eligibility': result.stage3.passed_count,
        'final_included': len(result.included_docs),
        'manual_review_needed': len(result.review_queue),
        'auto_excluded': result.excluded_count,
        'flow_diagram': result.flow_diagram_path
    }
```

#### 2.2 중복 제거 전략

```python
# backend/utils/deduplication.py

class DocumentDeduplicator:
    """
    다층 중복 제거 시스템
    """

    def remove_duplicates(self, docs: List[Document]) -> DeduplicationResult:
        """
        1. DOI 기반 exact match
        2. 제목 정규화 후 exact match
        3. TF-IDF + Cosine Similarity (threshold: 0.95)
        4. MinHash LSH for scalability (1000+ papers)
        """

        # Level 1: DOI
        seen_dois = set()
        unique_docs = []

        for doc in docs:
            doi = doc.metadata.get('doi')
            if doi and doi in seen_dois:
                continue  # Skip duplicate
            if doi:
                seen_dois.add(doi)
            unique_docs.append(doc)

        # Level 2: Title normalization
        unique_docs = self._remove_title_duplicates(unique_docs)

        # Level 3: Semantic similarity (if > 100 papers)
        if len(unique_docs) > 100:
            unique_docs = self._remove_semantic_duplicates(unique_docs)

        return DeduplicationResult(
            original_count=len(docs),
            unique_count=len(unique_docs),
            duplicates_removed=len(docs) - len(unique_docs),
            documents=unique_docs
        )
```

### Phase 3: UI 개선 (1-2일)

#### 3.1 Gradio 인터페이스 업데이트

**새 기능**:
1. **연구 프로파일 선택**
   - 드롭다운으로 사전 정의된 프로파일 선택
   - 또는 커스텀 키워드 입력

2. **PRISMA 플로우 다이어그램 표시**
   - Mermaid.js로 실시간 렌더링
   ```
   Identification: 50 papers
        ↓
   Screening: 35 papers (15 excluded)
        ↓
   Eligibility: 28 papers (7 excluded)
        ↓
   Included: 25 papers (3 in manual review)
   ```

3. **문헌 품질 대시보드**
   - 점수 분포 히스토그램
   - 도메인 분류 파이 차트 (HRM/HRD/Both)
   - 제외 사유 요약

4. **수동 검토 큐**
   - 보류 문헌 목록 (점수 50-59점)
   - 승인/거부 버튼
   - 사유 입력 텍스트

**UI 레이아웃**:
```python
with gr.Tabs():
    with gr.Tab("📤 Upload & Screen"):
        gr.Dropdown(
            choices=["HRM AI Bias", "HRD Technology Adoption", "Custom"],
            label="Research Profile"
        )
        # ... 기존 업로드 UI

        # 🆕 PRISMA 플로우 표시
        gr.Mermaid(label="PRISMA Flow Diagram")

        # 🆕 스크리닝 결과 요약
        with gr.Row():
            gr.Number(label="Total Uploaded")
            gr.Number(label="After Dedup")
            gr.Number(label="Final Included")

    with gr.Tab("📊 Quality Dashboard"):
        # 점수 분포
        gr.Plot(label="Relevance Score Distribution")

        # 도메인 분류
        gr.BarPlot(label="Domain Classification")

        # 제외 사유
        gr.DataFrame(label="Exclusion Reasons")

    with gr.Tab("🔍 Manual Review Queue"):
        # 보류 문헌 목록
        review_queue = gr.DataFrame(
            headers=["Title", "Score", "Reason", "Actions"]
        )

        with gr.Row():
            gr.Button("✅ Approve Selected")
            gr.Button("❌ Reject Selected")
```

### Phase 4: 고급 기능 (Optional, 3-4일)

#### 4.1 재스크리닝 시스템
```python
def rescore_collection(new_profile: ResearchProfile):
    """
    기존 컬렉션을 새 연구 프로파일로 재평가

    Use Case:
    - 연구 범위 변경 (HRM → HRM+HRD)
    - 키워드 정제
    - 임계값 조정
    """

    # Vector DB에서 모든 문서 로드
    all_docs = retriever.get_all_documents()

    # 새 프로파일로 재스코어링
    prisma = LiteratureReviewPRISMA(new_profile)
    rescored = prisma.rescore_documents(all_docs)

    # 새로 제외된 문서 식별
    newly_excluded = [doc for doc in rescored if doc.score < new_profile.min_score]

    # Vector DB에서 제거
    retriever.remove_documents([doc.id for doc in newly_excluded])

    return RescoreResult(
        total_documents=len(all_docs),
        newly_excluded=len(newly_excluded),
        still_included=len(all_docs) - len(newly_excluded)
    )
```

#### 4.2 문헌 추천 시스템
```python
def recommend_missing_papers(current_collection: List[Document]) -> List[str]:
    """
    컬렉션 분석 후 누락 가능성 있는 주제 식별

    방법:
    1. 현재 문헌의 키워드/주제 추출
    2. 키워드 공간에서 sparse 영역 탐지
    3. 해당 영역 커버할 검색 쿼리 생성
    """

    # 주제 클러스터링 (BERTopic)
    topics = extract_topics(current_collection)

    # Coverage gap 분석
    gaps = identify_coverage_gaps(topics)

    # 검색 쿼리 제안
    queries = [
        f"{gap.topic} AND {gap.missing_aspect}"
        for gap in gaps
    ]

    return queries
```

---

## 📊 성능 최적화

### 5.1 배치 처리 전략

**대량 업로드 시나리오 (100+ papers)**:
```python
async def batch_process_with_prisma(files: List[Path], batch_size: int = 20):
    """
    비동기 배치 처리
    """

    total_batches = len(files) // batch_size + 1

    for i in range(0, len(files), batch_size):
        batch = files[i:i+batch_size]

        # 병렬 PDF 파싱
        raw_docs = await asyncio.gather(*[
            parse_pdf_async(file) for file in batch
        ])

        # PRISMA 스크리닝 (CPU-bound)
        with ProcessPoolExecutor() as executor:
            screened = await loop.run_in_executor(
                executor,
                prisma.run_full_pipeline,
                raw_docs
            )

        # 점진적 Vector DB 업데이트
        retriever.add_documents(screened.included_docs)

        # 진행 상황 업데이트
        yield {
            'progress': (i + batch_size) / len(files),
            'current_batch': i // batch_size + 1,
            'total_batches': total_batches
        }
```

### 5.2 캐싱 전략
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def calculate_relevance_score(doc_hash: str, profile_hash: str) -> float:
    """
    동일 문서 + 동일 프로파일 = 캐시된 점수 반환
    """
    pass
```

---

## 🧪 검증 전략

### 6.1 단위 테스트
```python
# tests/test_prisma.py

def test_doi_deduplication():
    """DOI 중복 제거 검증"""
    pass

def test_title_normalization():
    """제목 정규화 및 중복 탐지"""
    pass

def test_scoring_consistency():
    """동일 문서 → 동일 점수 보장"""
    pass

def test_exclusion_keywords():
    """제외 키워드 정확도"""
    pass
```

### 6.2 통합 테스트
```python
def test_full_pipeline_with_real_papers():
    """
    실제 논문 50편으로 전체 파이프라인 검증

    Fixtures:
    - 25편: HRM AI bias papers (high relevance)
    - 15편: Medical AI papers (should exclude)
    - 10편: Education AI papers (medium relevance)
    """

    # 기대 결과
    assert included_count >= 20  # HRM papers
    assert excluded_count >= 15  # Medical papers
    assert review_queue_count >= 5  # Education papers (border cases)
```

---

## 📈 향후 확장

### 7.1 메타분석 지원
- 효과크기(effect size) 추출 자동화
- Cohen's d, Correlation coefficient 탐지
- 메타분석용 데이터셋 생성

### 7.2 협업 스크리닝
- 다중 평가자 지원 (Cohen's Kappa 계산)
- 불일치 해소 워크플로우
- 스크리닝 이력 추적

### 7.3 학술 API 통합
- Semantic Scholar API로 누락 논문 자동 발견
- CrossRef로 인용 관계 매핑
- OpenAlex로 저널 메트릭 자동 수집

---

## ✅ 구현 우선순위

**Must Have (MVP)**:
1. ✅ PRISMA 4단계 파이프라인
2. ✅ 관련성 점수 계산
3. ✅ 중복 제거 (DOI + Title)
4. ✅ 연구 프로파일 시스템
5. ✅ Gradio UI 업데이트

**Should Have (v1.1)**:
6. ✅ PRISMA 플로우 다이어그램
7. ✅ 수동 검토 큐
8. ✅ 품질 대시보드
9. ✅ 재스크리닝 기능

**Nice to Have (v2.0)**:
10. ⭐ 비동기 배치 처리
11. ⭐ 문헌 추천 시스템
12. ⭐ 메타분석 지원
13. ⭐ 협업 스크리닝

---

## 🚀 실행 계획

### Week 1: 핵심 파이프라인
- Day 1-2: `prisma_pipeline.py` 구현
- Day 3: 중복 제거 시스템
- Day 4: 테스트 작성
- Day 5: `ingestion.py` 통합

### Week 2: UI & 품질 관리
- Day 1-2: Gradio UI 개선
- Day 3: 품질 대시보드
- Day 4: 수동 검토 큐
- Day 5: 문서화 & 배포

---

## 📚 참고 자료

- [PRISMA 2020 Statement](http://www.prisma-statement.org/)
- [AI failure_HR PRISMA Implementation](../AI%20failure_HR/code/collection/prisma_screening_protocol.py)
- [LangChain Document Transformers](https://python.langchain.com/docs/modules/data_connection/document_transformers/)
- [ChromaDB Metadata Filtering](https://docs.trychroma.com/usage-guide#filtering-by-metadata)

---

**작성일**: 2025-01-10
**작성자**: Claude Code
**상태**: 전략 수립 완료 → 구현 대기
