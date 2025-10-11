# Vercel 프론트엔드 구성 전략: ResearcherRAG 통합 UI

## 🎯 목표

**문제 인식**:
- Gradio는 **프로토타입**에는 적합하지만 **프로덕션 협업 도구**로는 한계
- 3개 모듈(문헌/질적/노트)이 각자 독립 Gradio 앱 → 분산된 UX
- PRISMA 워크플로우, 프롬프트 템플릿 등을 시각적으로 학습할 방법 부재

**해결책**:
- **Single Page Application** (Next.js 14 App Router)
- **통합 대시보드**로 3개 RAG 모듈 접근
- **인터랙티브 학습 도구** (Prompt Studio, Workflow Canvas)
- **팀 협업** 지원 (실시간 공동 편집, 코멘트 시스템)

---

## 🏗️ 기술 스택

### Core Framework
- **Next.js 14** (App Router, React Server Components)
- **TypeScript** (엄격한 타입 안전성)
- **Tailwind CSS** + **shadcn/ui** (일관된 디자인 시스템)

### AI & 백엔드 통합
- **Vercel AI SDK** (`@vercel/ai`) - 스트리밍 답변
- **AI SDK RSC** (`ai/rsc`) - React Server Components 통합
- **tRPC** (타입 안전 API 호출)

### 시각화 & 인터랙션
- **React Flow** - LangGraph 워크플로우 시각화
- **Recharts** / **Visx** - 데이터 차트
- **React Force Graph** - 문헌 네트워크 그래프
- **Mermaid.js** - PRISMA 플로우 다이어그램

### 상태 관리 & 데이터
- **Zustand** - 클라이언트 상태
- **TanStack Query** (React Query) - 서버 상태 캐싱
- **Supabase** - 사용자 데이터, 협업 메타데이터 (optional)

### 배포 & 인프라
- **Vercel** - 프론트엔드 호스팅
- **Vercel Serverless Functions** - API Routes
- **Railway** / **Render** - Python 백엔드 (FastAPI/Gradio)

---

## 📐 아키텍처 설계

### 1. 프로젝트 구조

```
ResearcherRAG/
├── apps/
│   ├── web/                          # Next.js 프론트엔드
│   │   ├── app/
│   │   │   ├── (dashboard)/
│   │   │   │   ├── page.tsx          # 메인 대시보드
│   │   │   │   ├── literature/       # 문헌 RAG
│   │   │   │   │   ├── page.tsx
│   │   │   │   │   ├── upload/
│   │   │   │   │   ├── query/
│   │   │   │   │   └── prisma/      # PRISMA 플로우
│   │   │   │   ├── qualitative/      # 질적 코딩
│   │   │   │   ├── notes/            # 연구 노트
│   │   │   │   └── settings/
│   │   │   ├── (learning)/
│   │   │   │   ├── prompts/          # Prompt Studio
│   │   │   │   ├── workflows/        # Workflow Canvas
│   │   │   │   └── guides/           # 튜토리얼
│   │   │   ├── api/
│   │   │   │   ├── rag/[module]/route.ts  # RAG 프록시
│   │   │   │   ├── mcp/[provider]/route.ts # MCP 연동
│   │   │   │   └── trpc/[trpc]/route.ts   # tRPC 핸들러
│   │   │   └── layout.tsx
│   │   ├── components/
│   │   │   ├── rag/
│   │   │   │   ├── LiteratureRAG.tsx
│   │   │   │   ├── QualitativeRAG.tsx
│   │   │   │   └── NotesRAG.tsx
│   │   │   ├── learning/
│   │   │   │   ├── PromptCard.tsx
│   │   │   │   ├── WorkflowCanvas.tsx
│   │   │   │   └── PrismaFlow.tsx
│   │   │   ├── collaboration/
│   │   │   │   ├── CommentThread.tsx
│   │   │   │   └── LiveCursor.tsx
│   │   │   └── ui/                   # shadcn/ui
│   │   ├── lib/
│   │   │   ├── api-client.ts         # 백엔드 API 래퍼
│   │   │   ├── vercel-ai.ts          # AI SDK 설정
│   │   │   └── trpc.ts               # tRPC 클라이언트
│   │   └── public/
│   │       └── prompts/              # 프롬프트 JSON
│   └── backend/                      # 기존 Python 백엔드들
│       ├── literature-rag/           # FastAPI 변환
│       ├── qualitative-rag/
│       └── notes-rag/
└── packages/
    ├── shared/                       # 공유 TypeScript 타입
    └── prisma/                       # DB 스키마 (optional)
```

### 2. 데이터 플로우

```
┌─────────────────────────────────────────────────────────────┐
│                     Next.js Frontend                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Literature   │  │ Qualitative  │  │ Notes        │      │
│  │ RAG UI       │  │ RAG UI       │  │ RAG UI       │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                 │                  │              │
│         └─────────────────┴──────────────────┘              │
│                           │                                 │
│                  ┌────────▼─────────┐                       │
│                  │  tRPC Router     │                       │
│                  │  (Type-safe API) │                       │
│                  └────────┬─────────┘                       │
└───────────────────────────┼─────────────────────────────────┘
                            │
                 ┌──────────▼──────────┐
                 │ Vercel Edge Network │
                 │   (API Routes)      │
                 └──────────┬──────────┘
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
    ┌─────▼──────┐    ┌────▼─────┐    ┌─────▼──────┐
    │Literature  │    │Qualitative│    │Notes       │
    │FastAPI     │    │FastAPI    │    │FastAPI     │
    └─────┬──────┘    └────┬──────┘    └─────┬──────┘
          │                │                  │
    ┌─────▼──────┐    ┌────▼─────┐    ┌─────▼──────┐
    │ChromaDB    │    │ChromaDB   │    │ChromaDB    │
    └────────────┘    └───────────┘    └────────────┘
```

---

## 🎨 핵심 화면 설계

### 3.1 통합 대시보드 (`app/(dashboard)/page.tsx`)

**레이아웃**:
```
┌─────────────────────────────────────────────────────────┐
│  ResearcherRAG 🔬                        [User] [Settings]│
├─────────────────────────────────────────────────────────┤
│  📚 Literature Review  │  🎤 Qualitative  │  📝 Notes    │
│  ─────────────────────────────────────────────────────  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────┐ │
│  │ 📊 PRISMA Flow  │  │ 🏷️ Codebook    │  │ 📂 Vault │ │
│  │                 │  │                 │  │          │ │
│  │  Identification │  │  15 Themes      │  │ 247 Notes│ │
│  │      ↓          │  │  42 Codes       │  │          │ │
│  │   Screening     │  │                 │  │ Recent:  │ │
│  │      ↓          │  │ Top Theme:      │  │ • AI...  │ │
│  │  Eligibility    │  │ "Trust Issues"  │  │ • Ethics │ │
│  │      ↓          │  │                 │  │          │ │
│  │   25 Included   │  │                 │  │          │ │
│  └─────────────────┘  └─────────────────┘  └──────────┘ │
│                                                          │
│  📈 Recent Activity                                      │
│  ─────────────────────────────────────────────────────  │
│  • 10 papers screened (2 hours ago)                     │
│  • 3 codes added to "Bias" theme (5 hours ago)          │
│  • 12 notes tagged with #meta-analysis (1 day ago)      │
│                                                          │
│  🔧 Quick Actions                                        │
│  ─────────────────────────────────────────────────────  │
│  [Upload Papers] [Ask Question] [New Codebook] [+Note]  │
└─────────────────────────────────────────────────────────┘
```

**구현 포인트**:
```tsx
// app/(dashboard)/page.tsx

import { LiteratureStats } from '@/components/rag/LiteratureStats'
import { QualitativeStats } from '@/components/rag/QualitativeStats'
import { NotesStats } from '@/components/rag/NotesStats'

export default async function DashboardPage() {
  // Server Component에서 통계 병렬 로드
  const [litStats, qualStats, notesStats] = await Promise.all([
    getLiteratureStats(),
    getQualitativeStats(),
    getNotesStats(),
  ])

  return (
    <div className="grid grid-cols-3 gap-6">
      <LiteratureStats data={litStats} />
      <QualitativeStats data={qualStats} />
      <NotesStats data={notesStats} />
    </div>
  )
}
```

### 3.2 Literature RAG - PRISMA 워크플로우 (`app/(dashboard)/literature/prisma/page.tsx`)

**레이아웃**:
```
┌─────────────────────────────────────────────────────────┐
│  📚 Literature Review → PRISMA Screening                │
├─────────────────────────────────────────────────────────┤
│  [Research Profile: HRM AI Bias ▼]    [New Profile +]  │
│                                                          │
│  📊 PRISMA Flow Diagram                                 │
│  ─────────────────────────────────────────────────────  │
│                                                          │
│       ┌─────────────────────────┐                       │
│       │   Identification        │                       │
│       │   50 papers uploaded    │                       │
│       └───────────┬─────────────┘                       │
│                   ↓                                      │
│       ┌─────────────────────────┐                       │
│       │    Screening            │                       │
│       │   35 papers (70%)       │ ← [View Excluded: 15] │
│       └───────────┬─────────────┘                       │
│                   ↓                                      │
│       ┌─────────────────────────┐                       │
│       │   Eligibility           │                       │
│       │   28 papers (80%)       │ ← [View Excluded: 7]  │
│       └───────────┬─────────────┘                       │
│                   ↓                                      │
│       ┌─────────────────────────┐                       │
│       │   Included              │                       │
│       │   25 papers (89%)       │ → [To Vector DB]      │
│       └─────────────────────────┘                       │
│                                                          │
│  📋 Manual Review Queue (3 papers, score 50-59)         │
│  ─────────────────────────────────────────────────────  │
│  ┌─────────────────────────────────────────────────┐   │
│  │ [Score: 57] "Machine Learning in Education..."  │   │
│  │  Reason: HR context weak, but relevant methods  │   │
│  │  [✅ Include] [❌ Exclude] [💬 Comment]          │   │
│  └─────────────────────────────────────────────────┘   │
│                                                          │
│  📈 Score Distribution                                   │
│  ─────────────────────────────────────────────────────  │
│  [Histogram: 0-100 score, bell curve around 65]         │
└─────────────────────────────────────────────────────────┘
```

**구현 포인트**:
```tsx
// components/learning/PrismaFlow.tsx

'use client'

import { ReactFlow, Node, Edge } from 'reactflow'
import { usePrismaStats } from '@/lib/hooks/usePrismaStats'

export function PrismaFlow({ sessionId }: { sessionId: string }) {
  const { data } = usePrismaStats(sessionId)

  const nodes: Node[] = [
    {
      id: '1',
      type: 'prismaStage',
      position: { x: 250, y: 0 },
      data: {
        label: 'Identification',
        count: data.stage1.total,
        color: 'blue',
      },
    },
    {
      id: '2',
      type: 'prismaStage',
      position: { x: 250, y: 150 },
      data: {
        label: 'Screening',
        count: data.stage2.passed,
        excluded: data.stage2.excluded,
        color: 'purple',
      },
    },
    // ... 나머지 스테이지
  ]

  const edges: Edge[] = [
    { id: 'e1-2', source: '1', target: '2', animated: true },
    // ...
  ]

  return (
    <div className="h-[500px] border rounded-lg">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        fitView
        nodeTypes={{ prismaStage: PrismaStageNode }}
      />
    </div>
  )
}
```

### 3.3 Prompt Studio (`app/(learning)/prompts/page.tsx`)

**목표**:
- 문서화된 프롬프트를 **인터랙티브 카드**로 제공
- 실시간 수정 → Diff 미리보기 → 백엔드에 적용
- 버전 히스토리 관리

**레이아웃**:
```
┌─────────────────────────────────────────────────────────┐
│  🎨 Prompt Studio                      [Import] [Export]│
├─────────────────────────────────────────────────────────┤
│  [All Modules ▼] [Search prompts...]                    │
│                                                          │
│  📚 Literature Review Prompts                           │
│  ─────────────────────────────────────────────────────  │
│                                                          │
│  ┌──────────────────────────────────────────┐           │
│  │ 🔹 Query Decomposer                      │ [Edit]    │
│  │                                          │           │
│  │  You are a research assistant...         │           │
│  │  Break down complex questions into...    │           │
│  │                                          │           │
│  │  Temperature: 0.3  │  Max Tokens: 500   │           │
│  │  Model: claude-3-5-sonnet               │           │
│  │                                          │           │
│  │  📊 Usage: 247 calls | Avg latency: 1.2s│           │
│  │  ⭐ User Rating: 4.5/5 (12 reviews)      │           │
│  └──────────────────────────────────────────┘           │
│                                                          │
│  ┌──────────────────────────────────────────┐           │
│  │ 🔹 Synthesizer                           │ [Edit]    │
│  │  ...                                     │           │
│  └──────────────────────────────────────────┘           │
│                                                          │
│  [+ Create New Prompt]                                  │
│                                                          │
│  📝 Prompt Editor (when "Edit" clicked)                 │
│  ─────────────────────────────────────────────────────  │
│  ┌─────────────────┬─────────────────────────────────┐  │
│  │ Original        │ Modified (Live Preview)         │  │
│  ├─────────────────┼─────────────────────────────────┤  │
│  │ You are a...    │ You are an expert research...   │  │
│  │                 │                                 │  │
│  │ [Diff highlighting in both panels]                │  │
│  └─────────────────┴─────────────────────────────────┘  │
│                                                          │
│  [🧪 Test with Sample Query] [💾 Save] [↩️ Revert]      │
└─────────────────────────────────────────────────────────┘
```

**구현 포인트**:
```tsx
// app/(learning)/prompts/page.tsx

import { PromptCard } from '@/components/learning/PromptCard'
import { PromptEditor } from '@/components/learning/PromptEditor'

export default async function PromptsPage() {
  const prompts = await getPrompts()

  return (
    <div className="grid grid-cols-1 gap-4">
      {prompts.map((prompt) => (
        <PromptCard
          key={prompt.id}
          prompt={prompt}
          onEdit={(id) => showEditor(id)}
        />
      ))}
    </div>
  )
}

// components/learning/PromptEditor.tsx
'use client'

import { useDiff } from '@/lib/hooks/useDiff'
import { CodeMirror } from '@uiw/react-codemirror'

export function PromptEditor({ promptId }: { promptId: string }) {
  const { original, modified, setModified, diff } = useDiff(promptId)

  return (
    <div className="grid grid-cols-2 gap-4">
      {/* Original */}
      <div>
        <h3>Original</h3>
        <CodeMirror value={original} editable={false} />
      </div>

      {/* Modified */}
      <div>
        <h3>Modified</h3>
        <CodeMirror
          value={modified}
          onChange={setModified}
          extensions={[diff]} // Diff highlighting
        />
      </div>
    </div>
  )
}
```

### 3.4 Workflow Canvas (`app/(learning)/workflows/page.tsx`)

**목표**: LangGraph 워크플로우를 시각화하고 실행 로그 재생

**레이아웃**:
```
┌─────────────────────────────────────────────────────────┐
│  🔄 Workflow Canvas                    [Literature RAG] │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │                                                  │   │
│  │    [Query Decomposer] ──→ [Retriever] ───┐      │   │
│  │           │                               ↓      │   │
│  │           ↓                          [Reranker]  │   │
│  │    [Sub-queries]                          │      │   │
│  │           │                               ↓      │   │
│  │           └─────→ [Parallel Retrieval] →[Join]  │   │
│  │                                           │      │   │
│  │                                           ↓      │   │
│  │                                    [Synthesizer] │   │
│  │                                           │      │   │
│  │                                           ↓      │   │
│  │                                      [Response]  │   │
│  │                                                  │   │
│  └──────────────────────────────────────────────────┘   │
│                                                          │
│  📜 Execution Log (Live Replay)                         │
│  ─────────────────────────────────────────────────────  │
│  [▶️ Play] [⏸️ Pause] [⏭️ Next Step]   Speed: [1x ▼]   │
│                                                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │ [00:00.123] Query Decomposer                    │   │
│  │   Input: "What are AI bias mitigation..."       │   │
│  │   Output: 3 sub-queries                         │   │
│  │   • "AI bias types in HR"                       │   │
│  │   • "Bias mitigation techniques"                │   │
│  │   • "Case studies..."                           │   │
│  │                                                  │   │
│  │ [00:01.456] Parallel Retrieval (x3)             │   │
│  │   Retrieved: 15 documents (5 per query)         │   │
│  │   Top scores: 0.89, 0.87, 0.85                  │   │
│  │                                                  │   │
│  │ [00:02.789] Reranker                            │   │
│  │   Reranked to: 8 documents                      │   │
│  │   Dropped 7 duplicates/low-relevance            │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

**구현 포인트**:
```tsx
// components/learning/WorkflowCanvas.tsx

'use client'

import ReactFlow, { Node, Edge } from 'reactflow'
import { useExecutionLog } from '@/lib/hooks/useExecutionLog'

export function WorkflowCanvas({ workflowId }: { workflowId: string }) {
  const { nodes, edges, currentStep, play, pause, next } = useExecutionLog(workflowId)

  // 현재 실행 중인 노드 하이라이트
  const highlightedNodes = nodes.map(node => ({
    ...node,
    style: {
      ...node.style,
      border: node.id === currentStep ? '3px solid #10b981' : '1px solid #ccc'
    }
  }))

  return (
    <div>
      <ReactFlow nodes={highlightedNodes} edges={edges} />

      <div className="mt-4">
        <button onClick={play}>▶️ Play</button>
        <button onClick={pause}>⏸️ Pause</button>
        <button onClick={next}>⏭️ Next</button>
      </div>
    </div>
  )
}
```

---

## 🔌 백엔드 통합 전략

### 4.1 Python 백엔드 → FastAPI 변환

**현재 상태**: Gradio 기반 단독 앱
**목표**: FastAPI REST API로 변환 → Next.js가 호출

**예시: Literature RAG**

```python
# apps/backend/literature-rag/main.py

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# CORS 설정 (Vercel 도메인 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://researcherrag.vercel.app", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str
    research_profile: str = "default"
    top_k: int = 5

class QueryResponse(BaseModel):
    answer: str
    citations: List[dict]
    execution_log: List[dict]  # 🆕 워크플로우 로그

@app.post("/api/literature/upload")
async def upload_papers(files: List[UploadFile] = File(...)):
    # PRISMA 파이프라인 실행
    result = prisma_pipeline.run(files)
    return {
        "status": "success",
        "stages": {
            "identification": result.stage1,
            "screening": result.stage2,
            "eligibility": result.stage3,
            "included": result.stage4,
        }
    }

@app.post("/api/literature/query")
async def query_rag(req: QueryRequest) -> QueryResponse:
    # LangGraph 실행 + 로그 캡처
    answer, citations, log = run_langgraph_with_logging(req.question)

    return QueryResponse(
        answer=answer,
        citations=citations,
        execution_log=log  # 프론트에서 재생
    )

@app.get("/api/literature/stats")
async def get_stats():
    return retriever.get_collection_stats()
```

### 4.2 Next.js → 백엔드 API 호출

**tRPC로 타입 안전 API**

```typescript
// apps/web/lib/trpc.ts

import { createTRPCProxyClient, httpBatchLink } from '@trpc/client'
import type { AppRouter } from '../api/trpc/[trpc]/route'

export const trpc = createTRPCProxyClient<AppRouter>({
  links: [
    httpBatchLink({
      url: '/api/trpc',
    }),
  ],
})

// apps/web/api/trpc/[trpc]/route.ts

import { initTRPC } from '@trpc/server'
import { fetchRequestHandler } from '@trpc/server/adapters/fetch'

const t = initTRPC.create()

const appRouter = t.router({
  literature: t.router({
    upload: t.procedure
      .input(z.object({ files: z.array(z.instanceof(File)) }))
      .mutation(async ({ input }) => {
        // Python FastAPI 호출
        const res = await fetch('https://lit-rag.railway.app/api/literature/upload', {
          method: 'POST',
          body: formData,
        })
        return res.json()
      }),

    query: t.procedure
      .input(z.object({ question: z.string() }))
      .mutation(async ({ input }) => {
        const res = await fetch('https://lit-rag.railway.app/api/literature/query', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(input),
        })
        return res.json()
      }),
  }),
})

export type AppRouter = typeof appRouter

// Next.js Route Handler
export async function GET(req: Request) {
  return fetchRequestHandler({
    endpoint: '/api/trpc',
    req,
    router: appRouter,
    createContext: () => ({}),
  })
}
```

**프론트엔드 사용**:
```tsx
// app/(dashboard)/literature/query/page.tsx

'use client'

import { trpc } from '@/lib/trpc'

export default function LiteratureQuery() {
  const queryMutation = trpc.literature.query.useMutation()

  const handleSubmit = async (question: string) => {
    const result = await queryMutation.mutateAsync({ question })
    console.log(result.answer) // 타입 안전!
  }

  return <QueryForm onSubmit={handleSubmit} />
}
```

---

## 🚀 배포 전략

### 5.1 Vercel 배포

**설정 파일**: `vercel.json`
```json
{
  "buildCommand": "pnpm build",
  "outputDirectory": "apps/web/.next",
  "framework": "nextjs",
  "rewrites": [
    {
      "source": "/api/literature/:path*",
      "destination": "https://lit-rag.railway.app/api/literature/:path*"
    },
    {
      "source": "/api/qualitative/:path*",
      "destination": "https://qual-rag.railway.app/api/qualitative/:path*"
    },
    {
      "source": "/api/notes/:path*",
      "destination": "https://notes-rag.railway.app/api/notes/:path*"
    }
  ],
  "env": {
    "ANTHROPIC_API_KEY": "@anthropic-key",
    "OPENAI_API_KEY": "@openai-key"
  }
}
```

### 5.2 Python 백엔드 배포 (Railway/Render)

**Railway 배포**:
```bash
# apps/backend/literature-rag/railway.json
{
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "pip install -r requirements.txt"
  },
  "deploy": {
    "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/health",
    "restartPolicyType": "ON_FAILURE"
  }
}
```

**환경 변수 설정**:
```bash
railway variables set ANTHROPIC_API_KEY=xxx
railway variables set CHROMA_DB_PATH=/app/data/vector_db
railway up
```

### 5.3 CI/CD 파이프라인

**GitHub Actions** (`.github/workflows/deploy.yml`)
```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: pnpm install
      - run: pnpm build
      - uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}

  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: railway/deploy-action@v1
        with:
          railway-token: ${{ secrets.RAILWAY_TOKEN }}
          service: literature-rag
```

---

## 🎨 디자인 시스템

### 6.1 shadcn/ui 컴포넌트

**사용 컴포넌트**:
- `Button`, `Input`, `Select` - 폼 요소
- `Card`, `Tabs`, `Accordion` - 레이아웃
- `Dialog`, `Sheet`, `Popover` - 오버레이
- `Table`, `DataTable` - 데이터 표시
- `Progress`, `Skeleton` - 로딩 상태

**설치**:
```bash
pnpm dlx shadcn-ui@latest init
pnpm dlx shadcn-ui@latest add button card tabs dialog table
```

**커스텀 테마**:
```css
/* apps/web/app/globals.css */

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --primary: 262 83% 58%;  /* ResearcherRAG purple */
    --primary-foreground: 210 40% 98%;
    --secondary: 217 91% 60%;  /* Accent blue */
    /* ... */
  }
}
```

### 6.2 반응형 디자인

**Breakpoints** (Tailwind 기본):
- `sm`: 640px (태블릿)
- `md`: 768px (태블릿 landscape)
- `lg`: 1024px (데스크톱)
- `xl`: 1280px (대형 데스크톱)

**모바일 우선 설계**:
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* 모바일: 1열, 태블릿: 2열, 데스크톱: 3열 */}
</div>
```

---

## 🔐 보안 & 인증

### 7.1 사용자 인증 (Optional)

**Clerk.com 통합**:
```tsx
// apps/web/app/layout.tsx

import { ClerkProvider } from '@clerk/nextjs'

export default function RootLayout({ children }) {
  return (
    <ClerkProvider>
      <html>
        <body>{children}</body>
      </html>
    </ClerkProvider>
  )
}

// Protected route
import { auth } from '@clerk/nextjs'

export default async function DashboardPage() {
  const { userId } = auth()

  if (!userId) {
    redirect('/sign-in')
  }

  // ...
}
```

### 7.2 API 키 보안

**Vercel Environment Variables**:
- `ANTHROPIC_API_KEY` - Encrypted
- `OPENAI_API_KEY` - Encrypted
- `RAILWAY_API_URL` - Encrypted

**클라이언트 노출 방지**:
```typescript
// ❌ 잘못된 예
const apiKey = process.env.NEXT_PUBLIC_ANTHROPIC_API_KEY // 클라이언트 노출!

// ✅ 올바른 예 (Server Component/API Route만)
const apiKey = process.env.ANTHROPIC_API_KEY
```

---

## 📊 성능 최적화

### 8.1 React Server Components

**데이터 페칭 최적화**:
```tsx
// app/(dashboard)/literature/page.tsx

// ✅ 서버에서 병렬 페칭
export default async function LiteraturePage() {
  const [papers, stats, prismaFlow] = await Promise.all([
    getPapers(),
    getStats(),
    getPrismaFlow(),
  ])

  return (
    <>
      <PapersTable data={papers} />
      <StatsCard data={stats} />
      <PrismaFlowDiagram data={prismaFlow} />
    </>
  )
}
```

### 8.2 스트리밍 UI (Vercel AI SDK)

**실시간 답변 스트리밍**:
```tsx
// app/(dashboard)/literature/query/page.tsx

'use client'

import { useChat } from 'ai/react'

export default function ChatInterface() {
  const { messages, input, handleInputChange, handleSubmit } = useChat({
    api: '/api/literature/chat',  // Edge Function
  })

  return (
    <div>
      {messages.map(m => (
        <div key={m.id}>
          {m.role}: {m.content}  {/* 스트리밍으로 단어씩 표시 */}
        </div>
      ))}

      <form onSubmit={handleSubmit}>
        <input value={input} onChange={handleInputChange} />
      </form>
    </div>
  )
}

// app/api/literature/chat/route.ts

import { StreamingTextResponse, LangChainStream } from 'ai'
import { ChatAnthropic } from 'langchain/chat_models/anthropic'

export async function POST(req: Request) {
  const { messages } = await req.json()
  const { stream, handlers } = LangChainStream()

  const llm = new ChatAnthropic({
    streaming: true,
    callbacks: [handlers],
  })

  llm.call(messages)

  return new StreamingTextResponse(stream)
}
```

### 8.3 이미지 최적화

**Next.js Image 컴포넌트**:
```tsx
import Image from 'next/image'

<Image
  src="/prisma-flow.png"
  alt="PRISMA Flow"
  width={800}
  height={600}
  priority  // LCP 최적화
/>
```

---

## 🧪 테스팅 전략

### 9.1 단위 테스트 (Vitest)

```typescript
// apps/web/lib/__tests__/api-client.test.ts

import { describe, it, expect, vi } from 'vitest'
import { uploadPapers } from '../api-client'

describe('uploadPapers', () => {
  it('should call FastAPI endpoint with correct payload', async () => {
    global.fetch = vi.fn().mockResolvedValue({
      json: async () => ({ status: 'success' }),
    })

    const files = [new File(['test'], 'paper.pdf')]
    const result = await uploadPapers(files)

    expect(result.status).toBe('success')
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining('/api/literature/upload'),
      expect.any(Object)
    )
  })
})
```

### 9.2 E2E 테스트 (Playwright)

```typescript
// apps/web/e2e/literature-upload.spec.ts

import { test, expect } from '@playwright/test'

test('upload and query literature', async ({ page }) => {
  await page.goto('/literature/upload')

  // 파일 업로드
  await page.setInputFiles('input[type="file"]', 'fixtures/sample.pdf')
  await page.click('button:has-text("Upload")')

  // PRISMA 플로우 확인
  await expect(page.locator('text=Identification')).toBeVisible()
  await expect(page.locator('text=1 papers')).toBeVisible()

  // 쿼리 테스트
  await page.goto('/literature/query')
  await page.fill('textarea', 'What is AI bias?')
  await page.click('button:has-text("Search")')

  await expect(page.locator('text=AI bias refers to')).toBeVisible()
})
```

---

## 📦 패키지 구조 (Monorepo)

**pnpm Workspaces** (`pnpm-workspace.yaml`)
```yaml
packages:
  - 'apps/*'
  - 'packages/*'
```

**공유 타입 패키지** (`packages/shared`)
```typescript
// packages/shared/src/types/literature.ts

export interface PrismaStageResult {
  stage: 'identification' | 'screening' | 'eligibility' | 'inclusion'
  total: number
  passed: number
  excluded: number
  exclusion_reasons: { reason: string; count: number }[]
}

export interface Document {
  id: string
  title: string
  abstract: string
  metadata: {
    doi?: string
    year?: number
    authors?: string[]
  }
  score?: number
}
```

**프론트/백엔드에서 공유**:
```typescript
// apps/web/lib/api-client.ts
import type { PrismaStageResult } from '@researcherrag/shared'

// apps/backend/literature-rag/main.py
# from packages.shared.types import PrismaStageResult  # Python도 동일 타입 사용
```

---

## 🚧 로드맵

### Phase 1: MVP (2주)
- [x] Next.js 프로젝트 생성
- [ ] 통합 대시보드 UI
- [ ] Literature RAG 인터페이스
- [ ] FastAPI 백엔드 변환
- [ ] tRPC 통합
- [ ] Vercel 배포

### Phase 2: 고급 기능 (3주)
- [ ] PRISMA 플로우 시각화
- [ ] Prompt Studio
- [ ] Workflow Canvas
- [ ] 스트리밍 응답
- [ ] 반응형 디자인

### Phase 3: 협업 기능 (2주)
- [ ] 사용자 인증 (Clerk)
- [ ] 실시간 공동 편집 (Liveblocks)
- [ ] 코멘트 시스템
- [ ] 알림 시스템

### Phase 4: 최적화 (1주)
- [ ] 성능 프로파일링
- [ ] 번들 크기 최적화
- [ ] E2E 테스트 커버리지
- [ ] 문서화 완성

---

## 📚 학습 리소스

**필수 문서**:
- [Next.js 14 Docs](https://nextjs.org/docs)
- [Vercel AI SDK](https://sdk.vercel.ai/docs)
- [shadcn/ui](https://ui.shadcn.com/)
- [React Flow](https://reactflow.dev/)
- [tRPC](https://trpc.io/)

**참고 프로젝트**:
- [v0.dev](https://v0.dev/) - AI UI 생성기
- [ChatGPT UI](https://github.com/mckaywrigley/chatbot-ui) - Next.js 채팅 UI
- [Novel](https://novel.sh/) - Notion 스타일 에디터

---

**작성일**: 2025-01-10
**작성자**: Claude Code
**상태**: 전략 수립 완료 → 구현 준비 중
