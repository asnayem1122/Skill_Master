---
name: ai-application-engineering
description: "End-to-end engineering strategy for production AI applications: conversational chatbots, streaming protocols, structured outputs, advanced RAG (hybrid search, RRF, reranking), document ingestion pipelines, narrow tool-calling agents, grounding & citation verification, deterministic evals, and production observability."
license: Apache-2.0
metadata:
  author: "Skill Master AI Architect"
  version: "1.0.0"
  domain: "ai-ml"
  tags: "ai, llm, rag, agents, streaming, embeddings, evaluation, vector-search, production, deepeval, vercel-ai"
---

# AI Application Engineering

Master engineering strategy and architectural decision framework for designing, implementing, evaluating, debugging, and operating production AI systems.

---

## 1. Purpose & Triggers

Activate this skill whenever:
- Designing or implementing **LLM-powered features**, conversational assistants, chatbots, or AI copilots.
- Architecting **Retrieval-Augmented Generation (RAG)** systems, document ingestion, embeddings, chunking, hybrid search, or reranking.
- Implementing **streaming responses** (SSE, Data Stream Protocol), structured outputs (Zod/JSON Schema), or conversation memory.
- Developing **tool-calling agents** or multi-agent workflows with state machines, tool validation, and human-in-the-loop approvals.
- Creating **AI evaluation pipelines**, measuring RAG quality (Faithfulness, Answer Relevancy, Context Recall), or building regression suites.
- Hardening production AI for **latency, cost, prompt injection, rate limits, circuit breakers, and observability (OpenTelemetry)**.

### When NOT to Use
- Generic non-AI software development (use standard full-stack or architecture skills).
- Simple static prompts with no application integration, data retrieval, or tool execution.
- IDE session context setup for Antigravity itself (use `context-engineering`).
- Database schema migration or pure SQL administration without AI retrieval (use `database-engineering`).

---

## 2. The 10-Step AI Application Engineering Lifecycle

Every production AI feature must follow this disciplined 10-step sequence:

```
[1. Intake & Constraints] ──► [2. Codebase Inspection] ──► [3. Architecture Ladder]
                                                                     │
[6. Incremental Impl]     ◄── [5. Source-Driven Docs]   ◄── [4. Minimal Design]
       │
[7. Deterministic Tests]  ──► [8. AI-Specific Evals]    ──► [9. Production Hardening]
                                                                     │
                                                        [10. Verification Gate]
```

### Step 1: Clarify Requirements & Constraints
Ask or infer:
1. **User Experience**: Is it synchronous completion, streaming text, interactive chat, background processing, or UI widget generation?
2. **Latency Target**: What is acceptable TTFT (Time To First Token) and total latency (e.g. <500ms vs <3s)?
3. **Data Scope**: Is the knowledge fixed, dynamically updated, user-specific, or multi-tenant?
4. **Cost & Volume**: What is the target request volume, token budget, and max cost per query?
5. **Security & Privacy**: Does data contain PII/PHI? What are compliance boundaries (HIPAA, GDPR)?

### Step 2: Codebase & Toolchain Inspection
- Inspect existing dependencies: Language runtime (Node/TypeScript vs Python), frameworks (Next.js, FastAPI, NestJS), and current AI libraries (Vercel AI SDK, LangChain, native SDKs).
- Verify database and vector storage infrastructure (pgvector, Milvus, Qdrant, SQLite).
- Check environment configuration for API keys, model endpoints, and secret managers.

### Step 3: Choose Minimal Architecture via the Decision Ladder
Always adopt the **lowest complexity tier** that satisfies the requirement:

```
Level 0: Deterministic Code (No LLM needed)
   │
Level 1: Single LLM Call (Zero-shot / Few-shot prompt)
   │
Level 2: Structured Output (JSON Schema / Zod validation)
   │
Level 3: Tool-Calling Function (Single step, deterministic tool execution)
   │
Level 4: Standard RAG (Dense vector search + contextual prompt)
   │
Level 5: Advanced RAG (Hybrid dense + BM25, RRF fusion, cross-encoder reranking)
   │
Level 6: Autonomous Agent (Multi-step tool execution loop with state management)
   │
Level 7: Multi-Agent System (Specialized isolated sub-agents with strict handoffs)
```

> [!CRITICAL]
> **The Law of Minimal Complexity**: Never jump to an Autonomous Agent (Level 6) or Multi-Agent System (Level 7) when a Structured Output (Level 2) or single Tool Call (Level 3) solves the task. Complexity compounds error rates exponentially.

### Step 4: Minimal System Design & Trade-offs
Document the selected architecture:
- Model selection (Fast reasoning vs High-throughput vs Small local model).
- Memory strategy (None vs Sliding Window vs Vector Summary).
- Ingestion/retrieval strategy (Chunk size, overlap, embedding model, reranker).
- Tool definitions (Strict JSON schemas, idempotency keys, execution timeouts).

### Step 5: Consult Official Documentation
Before writing framework-specific code, verify current API specifications against official documentation (e.g. Vercel AI SDK v4+, Anthropic API, OpenAI API, DeepEval, pgvector). Avoid deprecated patterns (e.g. legacy LangChain `LLMChain` or obsolete AI SDK methods).

### Step 6: Implement in Small, Verifiable Increments
Deliver in thin vertical slices:
1. Core provider client and type definitions.
2. Ingestion or prompt assembly pipeline.
3. API route / streaming endpoint.
4. Client hook or consuming interface.

### Step 7: Create Deterministic Unit & Contract Tests
Prior to any LLM evaluation:
- Test schema parsing: Ensure Zod/Pydantic models reject invalid JSON.
- Test tool execution: Verify business logic with mocked tool arguments.
- Test stream framing: Verify SSE or Data Stream chunk formatting.

### Step 8: Measure AI Quality & Grounding
- Execute golden dataset evaluations (minimum 10-20 curated test queries).
- Measure the **RAG Triad**: Context Recall, Context Precision, Faithfulness, and Answer Relevancy.
- Verify explicit citations linking generated answers to source chunk IDs.

### Step 9: Harden Production Operations
- **Prompt Injection Defense**: Wrap untrusted retrieved content in isolated XML tags (`<retrieved_context>`).
- **Resilience**: Set hard model timeouts (AbortSignal), retry with exponential backoff, and configure fallback models.
- **Cost & Speed**: Implement ephemeral prompt caching for static prompts/documents; enforce strict token ceilings.
- **Observability**: Instrument OpenTelemetry spans capturing TTFT, total duration, token counts, and cost.

### Step 10: Verification Gate & Limitation Reporting
Verify end-to-end in the terminal or browser before completion. Report:
- Verified latency (TTFT and completion time).
- Observed token usage and estimated cost.
- Known boundary conditions and edge-case abstention behavior.

---

## 3. Specialized References & Intent Routing

When executing specific technical domains, read the corresponding reference file:

| Domain | When to Read | Reference File |
|---|---|---|
| **Chatbots & Streaming** | Implementing streaming endpoints, chat state, conversation history, cancellation, or structured generation. | [`references/chatbot-engineering.md`](references/chatbot-engineering.md) |
| **RAG Strategy** | Choosing retrieval methods: vector search, metadata filtering, hybrid search (dense + BM25), RRF, reranking, HyDE. | [`references/rag-strategy-selection.md`](references/rag-strategy-selection.md) |
| **Document Ingestion** | Parsing files (PDF, HTML, DOCX), semantic chunking, chunk overlap, deduplication, and embedding selection. | [`references/document-ingestion.md`](references/document-ingestion.md) |
| **Grounding & Quality** | Citation enforcement, abstention thresholds, prompt injection defense in retrieved docs, diagnostic triage. | [`references/grounding-and-quality.md`](references/grounding-and-quality.md) |
| **Agent & Tools** | Narrow tool schemas, argument validation, idempotency, step caps (`maxSteps`), human-in-the-loop approvals. | [`references/agent-tool-architecture.md`](references/agent-tool-architecture.md) |
| **AI Evaluation** | Evaluating Faithfulness, Answer Relevancy, G-Eval rubrics, synthetic goldens, CI/CD regression suites. | [`references/evaluation-and-metrics.md`](references/evaluation-and-metrics.md) |
| **Production Ops** | Ephemeral prompt caching, TTFT optimization, rate limiting, circuit breakers, OpenTelemetry spans. | [`references/production-engineering.md`](references/production-engineering.md) |

---

## 4. Golden Rules of AI Application Engineering

1. **Keep Permissions & Business Logic Outside the LLM**: Never ask the model "Does this user have permission to delete this file?". Validate auth in deterministic application code before calling the tool.
2. **Abstain Rather Than Fabricate**: When retrieval context does not contain the answer, instruct the model to explicitly state "I do not have sufficient information to answer this question".
3. **Always Bound Agent Loops**: Every tool-calling loop must have a hard `maxSteps` (e.g. 5-10) and a hard execution timeout. Unbounded loops lead to runaway billing and hanging processes.
4. **Never Pass Raw External Input to Evaluators Unchecked**: Sanitize and truncate inputs before LLM-as-a-judge evaluations to prevent evaluation prompt injection.
5. **Cache Static Prefixes**: Place large system instructions and reference documentation at the start of prompts with cache markers to eliminate 80%+ of latency and cost.
