# Collision & Overlap Analysis: AI Application Engineering

**Author**: Senior AI Application Architect & Agent-Skill Engineer  
**Date**: October 2026  
**Repository**: [Skill Master](https://github.com/asnayem1122/Skill_Master)  
**Governance Compliance**: Commandment 1 (*Never Duplicate Skills — Merge overlapping capabilities into existing master skills rather than creating splinter directories*).

---

## 1. Objective

Before introducing `ai-application-engineering` into the Skill Master catalog, this analysis audits the existing 72 skills in `.agent/skills/` to:
1. Identify all potential functional and thematic overlaps.
2. Determine whether the proposed capabilities should be merged into existing skills or established as a distinct master skill.
3. Establish clear boundaries and integration contracts between skills.

---

## 2. Audit of Candidate Skills & Thematic Overlaps

| Existing Skill | Primary Scope | Overlap with AI App Engineering | Collision Decision |
|---|---|---|---|
| **`agent-orchestrator`** | Multi-agent coordination for **coding tasks** (splitting complex tasks into researcher, writer, coder, verifier sub-agents). | Multi-agent orchestration concepts. | **No Merge — Distinct Domains.** `agent-orchestrator` governs how Antigravity orchestrates its internal development subagents. `ai-application-engineering` governs how software engineers design customer-facing AI applications, runtime tool loops, and production multi-agent workflows. Cross-referenced as a design pattern. |
| **`context-engineering`** | Optimizing **agent context** in IDE sessions (rules, instruction files, memory management for coding assistants). | Context window management, token limits. | **No Merge — Distinct Domains.** `context-engineering` optimizes the developer's agent session environment. `ai-application-engineering` manages runtime conversation memory (sliding window, summarization, prompt caching) inside the application being built. |
| **`database-engineering`** | PostgreSQL/SQLite architecture, schema migrations, SQLAlchemy, pgvector indexing, Row-Level Security (RLS). | Vector storage, pgvector queries, similarity search. | **No Merge — Layer Separation.** `database-engineering` operates at the database infrastructure layer (SQL, connection pools, index types like HNSW/IVFFlat). `ai-application-engineering` operates at the application and retrieval layer (chunking, hybrid RRF, reranking, RAG evals). It treats vector DBs as pluggable retrieval stores. |
| **`security-and-hardening`** | OWASP Top 10:2025, ASVS 5.0, OWASP LLM & Agentic Top 10 vulnerabilities (ASI01-ASI10), supply chain security. | AI security, prompt injection, tool authorization. | **No Merge — Complementary Partnership.** `security-and-hardening` provides the exhaustive compliance catalog and threat checklists. `ai-application-engineering` provides the concrete implementation patterns (isolated XML delimiter tagging, schema sanitization, deterministic authorization walls outside LLMs) to prevent these vulnerabilities in production code. |
| **`api-engineering`** | REST/GraphQL endpoint contracts, TypeScript type sync, RFC 7807 error semantics. | Streaming endpoints, API routes for AI. | **No Merge — Composed Integration.** `api-engineering` provides general web API conventions. `ai-application-engineering` specializes in SSE/Data Stream protocols, model timeouts, token budgeting, and tool payload contracts. |
| **`observability-and-instrumentation`** | General application tracing, metrics, logging, alerting. | LLM tracing, token tracking. | **No Merge — Specialized Domain.** `ai-application-engineering` introduces AI-specific metrics (TTFT, ITL, Faithfulness, Context Recall, Token Cost) and exports them via standard OpenTelemetry traces, delegating generic telemetry setup to `observability-and-instrumentation`. |
| **`source-driven-development`** | Grounding implementation decisions in official framework documentation. | Reading official AI SDK docs. | **Complementary Workflow.** Embedded directly into Step 5 of the `ai-application-engineering` workflow. |
| **`verifying-before-completion`** | Anti-hallucination evidence gate before declaring tasks done. | Quality gates for AI code. | **Complementary Workflow.** Embedded directly into Step 10 of the `ai-application-engineering` workflow. |

---

## 3. Synthesis & Architectural Boundary Definition

### The Gap in Skill Master
Prior to this skill, Skill Master had:
- Meta-skills for Antigravity's own agent operations (`agent-orchestrator`, `context-engineering`).
- Low-level database and SQL guidance (`database-engineering`).
- Threat compliance lists (`security-and-hardening`).
- Frontend UI and full-stack orchestration (`frontend-ui-engineering`, `full-stack-orchestration`).

However, Skill Master lacked an **authoritative, end-to-end AI Application Engineering master skill** that teaches coding agents how to:
1. Discriminate between basic LLM calls, structured generation, tool use, RAG, and autonomous agents.
2. Build resilient streaming chatbots with cancellation and memory sliding windows.
3. Design and benchmark enterprise RAG systems (multimodal ingestion, semantic chunking, dense + BM25 hybrid search, RRF, cross-encoder rerankers).
4. Enforce strict grounding, citation linking, and defense against prompt injection in retrieved contexts.
5. Engineer narrow, validated tool schemas with human-in-the-loop safeguards.
6. Build deterministic evaluation suites measuring Faithfulness, Answer Relevancy, Context Recall/Precision, and G-Eval rubrics.
7. Implement production AI operations (ephemeral prompt caching, latency budgets, circuit breakers, fallback providers).

### Conclusion & Approval
Merging this vast domain into `agent-orchestrator` or `database-engineering` would severely bloat those focused skills and violate Commandment 2 (*Positive Updates Only: Never degrade or bloat existing skills*).

Therefore, establishing `ai-application-engineering` as a dedicated master skill in the **Architecture & Full-Stack / AI-ML** domain is fully justified, maintains strict clean boundaries, and enriches the global Skill Master ecosystem.
