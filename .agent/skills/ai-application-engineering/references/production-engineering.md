# Production AI Engineering: Observability, Resilience & Cost Optimization

This reference guides the hardening of production AI infrastructure: latency profiling, cost controls, resilience against provider outages, secret hygiene, and OpenTelemetry observability.

---

## 1. Latency Optimization: Profiling the AI Pipeline

In generative applications, perceived latency is governed by **Time To First Token (TTFT)**, not total completion time.

```
Total Request Time
├─► Network & Auth Latency (~50ms)
├─► Vector & Database Retrieval (~50–150ms)
├─► Cross-Encoder Reranking (~100–250ms)
├─► TTFT (Model Prompt Processing & First Token) (~300–600ms)  <-- User sees first text here
└─► Generation Stream (~30–50 tokens/sec until complete)
```

### Levers to Reduce TTFT
1. **Ephemeral Prompt Caching**: Cache static system instructions and documentation prefixes. Reduces TTFT from ~1,200ms to ~250ms on large context prompts.
2. **Streaming Immediately**: Never buffer the LLM response on the server before transmitting to the client. Pipe the stream directly.
3. **Speculative / Small Model Routing**: Route simple intent classification or query rewrites to small, ultra-fast models (e.g. GPT-4o-mini, Claude 3.5 Haiku, Llama-3-8B).
4. **Parallel Retrieval**: Run dense vector search and sparse BM25 search concurrently using `Promise.all()` or async worker threads.

---

## 2. Resilience, Circuit Breakers & Provider Fallbacks

AI APIs experience intermittent rate limits (HTTP 429), regional outages, and degraded performance. Single-provider dependencies create single points of failure.

### Provider Fallback Pattern
```typescript
import { generateText } from 'ai';
import { openai } from '@ai-sdk/openai';
import { anthropic } from '@ai-sdk/anthropic';

export async function resilientGenerate(prompt: string, systemPrompt: string) {
  try {
    // Primary provider: OpenAI
    return await generateText({
      model: openai('gpt-4o'),
      system: systemPrompt,
      prompt,
      abortSignal: AbortSignal.timeout(8000), // 8s hard timeout
    });
  } catch (error: any) {
    console.warn('Primary model failed or timed out. Triggering fallback to Anthropic Claude...', error.message);
    
    // Fallback provider: Anthropic
    return await generateText({
      model: anthropic('claude-3-5-sonnet-20241022'),
      system: systemPrompt,
      prompt,
      abortSignal: AbortSignal.timeout(10000),
    });
  }
}
```

### Circuit Breakers
If a provider fails 5 consecutive times within 60 seconds, trip the circuit breaker and route 100% of traffic to the backup provider for 5 minutes before probing the primary provider again.

---

## 3. Cost Controls & Token Budgeting

Unmonitored AI endpoints can exhaust monthly budgets in hours due to automated scrapers or runaway agent loops.

### Defensive Safeguards
1. **Per-User Rate Limiting**: Implement token-bucket rate limiting via Redis (e.g. maximum 30 AI queries per user per hour).
2. **Hard Output Token Limits**: Explicitly specify `maxTokens: 1024` on every generation call. Never leave `max_tokens` unset.
3. **Semantic Caching**: For common, non-personalized queries (e.g. "What are your support hours?"), query a semantic cache (e.g. Redis with vector similarity threshold > 0.96) before calling an LLM. Serves instant responses at $0.00 cost.
4. **Token Usage Logging**: Calculate and log cost per request:
   $$\text{Cost} = (\text{Prompt Tokens} \times \text{Rate}_{\text{in}}) + (\text{Completion Tokens} \times \text{Rate}_{\text{out}})$$

---

## 4. Observability with OpenTelemetry (OTel)

Trace every AI request across its lifecycle using standardized OpenTelemetry semantic conventions:

```
[Span: chat_completion_request]
  ├── [Span: session_auth] (5ms)
  ├── [Span: vector_retrieval] (42ms)
  │     attributes: { "retrieval.k": 50, "retrieval.index": "pgvector_docs" }
  ├── [Span: cross_encoder_rerank] (110ms)
  │     attributes: { "reranker.model": "bge-reranker-large", "reranker.output_k": 5 }
  └── [Span: llm_generation] (850ms)
        attributes: {
          "gen_ai.system": "anthropic",
          "gen_ai.request.model": "claude-3-5-sonnet-20241022",
          "gen_ai.usage.prompt_tokens": 1420,
          "gen_ai.usage.completion_tokens": 185,
          "gen_ai.response.finish_reasons": ["stop"],
          "gen_ai.time_to_first_token_ms": 320
        }
```

### Trace Data Sanitization
- Never log raw PII (social security numbers, credit cards, health records) in trace attributes.
- Mask or redact API keys and sensitive environment variables from error traces.

---

## 5. Security & Secret Hygiene

- **Store Keys in Managed Vaults**: Load API keys from secure environment stores (AWS Secrets Manager, GCP Secret Manager, Vault).
- **Rotate Keys Programmatically**: Rotate provider keys every 90 days.
- **Client Anonymization**: Never expose backend LLM API keys to the browser/client. All requests must route through a secure, authenticated server endpoint.
