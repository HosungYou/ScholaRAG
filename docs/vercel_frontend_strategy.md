# Vercel 기반 ResearcherRAG UI 구현 전략

## 1. 목표
- 세 가지 RAG 모듈(문헌, 질적 코딩, 연구 노트)을 단일 Next.js 애플리케이션에서 탐색 가능하도록 통합.
- MCP(Multi-Context Provider)를 통해 Figma, Obsidian, PRISMA 파이프라인과 연동하여 “데이터 준비 → 분석 → 시각화” 흐름을 가시화.
- Prompt 템플릿과 LangGraph 워크플로우를 시각적으로 학습할 수 있는 인터랙티브 가이드 제공.

## 2. 아키텍처 개요
```
apps/frontend (Next.js 14, App Router)
├── pages/
│   ├── index.tsx                # 대시보드
│   ├── literature.tsx           # 문헌 RAG 인터페이스
│   ├── qualitative.tsx          # 질적 코딩 RAG 인터페이스
│   └── notes.tsx                # 연구 노트 RAG 인터페이스
├── components/
│   ├── PromptStudio/            # 프롬프트 카드 & 수정 인터랙션
│   ├── WorkflowCanvas/          # LangGraph 단계 시각화 (react-flow)
│   ├── PrismaTimeline/          # PRISMA 단계 진행 상황
│   └── MCPPanel/                # 연결된 MCP 서비스 상태(Figma, Filesystem)
├── lib/
│   ├── api.ts                   # 백엔드 FastAPI/Gradio bridge 호출 래퍼
│   ├── vercel-ai.ts             # Vercel AI SDK (Streaming UI)
│   └── providers/               # Anthropic/OpenAI provider 팩토리
└── public/assets/
    └── prompts/                 # 프롬프트 JSON 템플릿 예시
```

- **호스팅**: Vercel (Next.js Edge Functions + Serverless Functions).
- **실시간 업데이트**: Vercel AI SDK (`@vercel/ai`)의 `useChat()` 훅을 활용하여 RAG 쿼리 응답을 스트리밍.
- **후면 연동**: 각 모듈별 Python 백엔드(Gradio/FastAPI)를 `/api/*` 경유로 프록시. `vercel.json`에서 `rewrites`를 설정하여 로컬 혹은 Hugging Face Space와 안전하게 터널링.
- **파일 업로드**: Next.js `Route Handler`에서 FormData로 파일을 수신→Supabase Storage 혹은 Vercel Blob에 임시 보관→백엔드에 signed URL 전달.

## 3. 핵심 화면 설계
1. **Unified Dashboard (`/`)**
   - 모듈 상태 카드: 인덱싱된 문헌 수, 노트 청크 수, 코드북 커버리지.
   - PRISMA Progress 바: Identification → Screening → Eligibility → Inclusion.
   - 최근 MCP 활동 로그: Figma 주석, Obsidian 싱크 내역.

2. **Prompt Studio**
   - `docs/module_*` 문서에서 발췌한 프롬프트를 JSON Schema로 정리하고 카드 형태로 노출.
   - 각 카드 수정 시 우측 패널에서 Diff 미리보기 제공, “실행” 버튼으로 백엔드에 전송.
   - 수정 내역은 Git-like History 패널에 축적하여 팀 협업 시 롤백 가능.

3. **Workflow Canvas**
   - `react-flow` 기반 그래프 컴포넌트로 LangGraph 노드를 시각화.
   - 노드 클릭 시 사용되는 프롬프트, 입력/출력 샘플을 모달로 표시.
   - 실행 로그를 SSE(서버 전송 이벤트)로 받아 타임라인에 재생.

4. **Notes Explorer (`/notes`)**
   - 좌측: Obsidian 스타일 폴더 트리 + 태그 필터.
   - 중앙: 대화형 RAG 채팅 (Vercel AI SDK), 하이라이트된 근거 문단 인라인 표시.
   - 우측: 시간축 뷰 (temporal query 결과), “연결 안 된 노트” 추천 섹션.

5. **Design Companion 패널**
   - Figma MCP를 통해 현재 보드의 프레임/컴포넌트 리스트를 가져와 카드화.
   - 선택한 프레임의 메타데이터(색상, 폰트, 레이어 구조)를 추출하고 RAG 응답과 함께 표시하여 디자인-콘텐츠 연속성을 확보.

## 4. 기술 스택 & 라이브러리
- **UI**: Next.js 14 + TypeScript + Tailwind CSS + shadcn/ui.
- **데이터 시각화**: `@tanstack/react-table`, `visx`, `react-force-graph`(토픽 네트워크).
- **상태 관리**: Zustand (모듈별 상태), React Query (백엔드 호출 캐싱).
- **AI 통합**: `@vercel/ai`, `ai/rsc`를 사용해 서버 액션 기반 스트리밍 답변 구현.
- **MCP 연동**: `codex mcp` CLI로 등록한 Figma/Filesystem/Context7 서버를 프록시하는 `api/mcp/[provider].ts` 라우트 작성.

## 5. 배포 파이프라인
1. `apps/frontend` 디렉터리에 Next.js 프로젝트 생성 (`pnpm dlx create-next-app`).
2. `vercel link`로 프로젝트 연결 후 `vercel env pull`에 필요한 키(Anthropic, Qdrant, Figma) 설정.
3. GitHub 연동 시 `vercel.json`에서 프론트만 빌드하고 Python 백엔드는 Hugging Face Space 혹은 Railway로 배포.
4. PR 플로우: 프론트 변경 → Vercel Preview URL 자동 생성 → QA → `main` 병합 후 Production Promote.

## 6. 향후 확장 아이디어
- **Live Co-editing**: Liveblocks로 문헌 카드/코드북 협업 편집 제공.
- **Storybook**: Prompt 카드, LangGraph 노드 컴포넌트를 Storybook에서 문서화.
- **Custom Analytics**: PostHog로 사용자 행동을 추적, 인기 프롬프트/노트 유형 분석.
- **Mobile Companion**: Next.js App Router와 Expo Router를 공유하는 하이브리드 구조로 모바일에서도 노트 검색 지원.

## 7. 구현 로드맵 (3 Sprint 제안)
- **Sprint 1**: Next.js 기본 틀 + Notes Explorer + 백엔드 프록시.
- **Sprint 2**: Prompt Studio + Workflow Canvas + MCP 패널.
- **Sprint 3**: PRISMA Timeline, 실시간 로그 스트리밍, 디자인 컴패니언.

본 전략 문서를 따라가면 연구자들이 백엔드 코드를 직접 열람하지 않고도 프롬프트 구성, LangGraph 흐름, MCP 연계 상태를 직관적으로 이해할 수 있는 Vercel 기반 UI를 구축할 수 있습니다.
