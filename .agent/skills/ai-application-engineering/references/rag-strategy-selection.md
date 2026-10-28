# RAG Strategy Selection & Retrieval Architecture

This reference guides the selection, design, and justification of Retrieval-Augmented Generation (RAG) architectures. It prevents both under-engineering (hallucinations from naive vector search) and over-engineering (unnecessary multi-agent RAG graphs).

---

## 1. The RAG Strategy Ladder

Select the retrieval strategy that directly addresses the observed retrieval failure mode:

```
[Level 1: Basic Vector Search]
      │ (Fails on metadata, dates, tenants)
      ▼
[Level 2: Metadata Pre/Post-Filtering]
      │ (Fails on exact keywords, serial numbers, codes, acronyms)
      ▼
[Level 3: Hybrid Search (Dense Vector + BM25 Lexical + RRF)]
      │ (Fails on conversational ambiguity, typos, short queries)
      ▼
[Level 4: Query Rewriting / HyDE / Decomposition]
      │ (Fails on precision; top-50 contains noise, context window polluted)
      ▼
[Level 5: Two-Stage Retrieval with Cross-Encoder Reranking]
      │ (Fails on chunk boundary fragmentation, loss of document context)
      ▼
[Level 6: Contextual Retrieval & Compression]
      │ (Fails on multi-step reasoning across diverse external databases)
      ▼
[Level 7: Agentic RAG (Dynamic query planning & routing)]
```

---

## 2. Strategy Comparison Matrix

| Strategy | When to Use | Failure It Addresses | Added Latency | Added Cost / Complexity |
|---|---|---|---|---|
| **1. Basic Vector** | General semantic similarity over homogeneous, non-filtered text. | Baseline retrieval. | Baseline (<50ms). | Low (Standard vector index). |
| **2. Metadata Filter** | Multi-tenant apps, role-based access, date ranges, product categories. | "Leaking" data across tenants or returning obsolete versions. | Negligible (+5ms). | Low (Requires metadata schema in DB). |
| **3. Hybrid (Dense + BM25)** | Corpora with technical jargon, error codes, SKUs, legal clauses, acronyms. | Vector search missing exact keyword or serial number matches. | Low (+20–50ms). | Medium (Requires BM25/Elasticsearch/pg_trgm + Reciprocal Rank Fusion). |
| **4. Query Rewriting / HyDE** | Ambiguous user queries, conversational follow-ups ("What about that one?"). | Poor embedding alignment between a short query and long answer passages. | Moderate (+300–800ms). | Medium (Requires 1 preliminary fast LLM call). |
| **5. Cross-Encoder Reranker** | High-precision needs; enterprise knowledge bases with overlapping topics. | Bi-encoder vector search retrieves loosely related noise in Top-5. | Moderate (+100–300ms). | Medium (Requires reranking model API or local service like BGE/Cohere). |
| **6. Contextual Compression** | Long documents where relevant facts are buried in large chunks. | Context window bloat and "lost in the middle" attention failure. | High (+500ms–1s). | High (Requires LLM extraction/compression per chunk). |
| **7. Agentic RAG** | Questions requiring multi-hop queries across distinct APIs and corpora. | Single-shot retrieval cannot synthesize disjoint information sources. | Very High (2–10s+). | High (Multi-step tool loop, state machine, branching logic). |

---

## 3. Deep-Dive Strategy Specifications

### A. Hybrid Retrieval with Reciprocal Rank Fusion (RRF)
Vector embeddings excel at semantic similarity (e.g. matching "automobile malfunction" with "car engine failure") but fail on exact identifiers (e.g. "Error code 0x80070005" or "Clause 14.2(b)").

**Solution**: Run dense vector search and sparse BM25 lexical search in parallel, then merge their rank lists using **Reciprocal Rank Fusion**:

$$RRF\_Score(d \in D) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$

Where:
- $M$ is the set of retrieval systems (Dense and Sparse).
- $r_m(d)$ is the rank of document $d$ in system $m$ (1-indexed).
- $k$ is a smoothing constant (standard default: $k = 60$).

```typescript
// Deterministic Reciprocal Rank Fusion (RRF) Implementation
interface ScoredItem {
  id: string;
  content: string;
  metadata?: Record<string, any>;
}

export function reciprocalRankFusion(
  denseResults: ScoredItem[],
  sparseResults: ScoredItem[],
  k: number = 60,
  topN: number = 10
): ScoredItem[] {
  const scores = new Map<string, { item: ScoredItem; score: number }>();

  // Process dense ranking
  denseResults.forEach((item, index) => {
    const rank = index + 1;
    const rrfScore = 1 / (k + rank);
    scores.set(item.id, { item, score: rrfScore });
  });

  // Process sparse ranking
  sparseResults.forEach((item, index) => {
    const rank = index + 1;
    const rrfScore = 1 / (k + rank);
    if (scores.has(item.id)) {
      scores.get(item.id)!.score += rrfScore;
    } else {
      scores.set(item.id, { item, score: rrfScore });
    }
  });

  return Array.from(scores.values())
    .sort((a, b) => b.score - a.score)
    .slice(0, topN)
    .map(entry => entry.item);
}
```

---

### B. Two-Stage Retrieval with Cross-Encoder Reranking
Bi-encoder embedding models compute query embeddings and document embeddings independently:
$$\text{Sim}(q, d) = \cos(\mathbf{e}_q, \mathbf{e}_d)$$
This is fast, but ignores cross-attention interactions between query tokens and document tokens.

**Two-Stage Pipeline**:
1. **Stage 1 (Retrieval)**: Use fast hybrid/vector search to retrieve candidates with high recall ($K = 50$).
2. **Stage 2 (Reranking)**: Feed $(q, d_i)$ pairs to a cross-encoder model (e.g. BGE-Reranker-Large, Cohere Rerank, NVIDIA NeMo Reranker). The cross-encoder attends to all tokens simultaneously, outputting an unconstrained relevance score.
3. Select Top-$N$ (e.g. $N = 5$) for LLM generation.

---

### C. Conversational Query Rewriting & Condensation
In multi-turn chat, user follow-up questions lack explicit entities:
- User Turn 1: "How do I configure SSL certificates on Nginx?"
- User Turn 2: "What if they are expired?"

Querying a vector database with `"What if they are expired?"` fails completely.
**Solution**: Run a fast query condensation LLM call before retrieval:

```typescript
import { generateText } from 'ai';
import { openai } from '@ai-sdk/openai';

export async function rewriteConversationalQuery(
  conversationHistory: string,
  latestQuery: string
): Promise<string> {
  const { text } = await generateText({
    model: openai('gpt-4o-mini'), // Low-latency, low-cost model
    system: `Given a conversation history and a follow-up query, rephrase the follow-up query into a standalone search query.
Do NOT answer the question. Only output the rephrased search query.
If the query is already standalone, return it verbatim.`,
    prompt: `History:\n${conversationHistory}\n\nFollow-up: ${latestQuery}\n\nStandalone Query:`,
  });

  return text.trim();
}
```

---

### D. Hypothetical Document Embeddings (HyDE)
When user queries are short questions (e.g. "What causes error 504?"), their embedding often aligns poorly with technical documentation explaining gateway timeouts.

**HyDE Workflow**:
1. Instruct an LLM: *"Write a hypothetical documentation paragraph that answers: 'What causes error 504?'"*.
2. Generate an embedding of the **hypothetical answer**, not the question.
3. Search the vector database using the hypothetical answer embedding.
4. **Use Case**: Informational search across vast technical manuals where question-to-answer semantic gaps are wide.

---

## 4. Decision Framework: When to Use What

```
Is the data multi-tenant or role-restricted?
  ├── YES ──► Enforce METADATA FILTERING before vector search
  └── NO  ──► Proceed

Does the dataset contain codes, part numbers, exact terms, or acronyms?
  ├── YES ──► Implement HYBRID RETRIEVAL (Dense + BM25 + RRF)
  └── NO  ──► Dense Vector Search is sufficient

Is the user in a multi-turn chat asking contextual follow-ups?
  ├── YES ──► Implement QUERY CONDENSATION / REWRITING
  └── NO  ──► Proceed

Are the Top-10 vector results noisy or containing irrelevant passages?
  ├── YES ──► Add CROSS-ENCODER RERANKING (Retrieve 50, Rerank to 5)
  └── NO  ──► Proceed

Does the answer require multi-step lookups across disjoint APIs or databases?
  ├── YES ──► AGENTIC RAG with Tool Calling
  └── NO  ──► Standard Hybrid RAG with Reranking
```
