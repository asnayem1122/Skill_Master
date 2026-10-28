# Chatbot Engineering & Conversational Architecture

This reference guides the engineering of robust, production-grade conversational interfaces, streaming pipelines, structured generations, and conversation memory.

---

## 1. Architectural Tiers: Conversational Classification

Before implementing conversational features, categorize the interaction pattern:

| Category | Definition | State Needs | Execution Latency | Recommended Architecture |
|---|---|---|---|---|
| **Simple Chatbot** | Single or multi-turn text generation with persona and domain instructions. No tool execution. | Ephemeral or DB message history. | Fast (<500ms TTFT). | Single streaming LLM call with sliding-window history. |
| **Tool-Using Assistant** | Conversational flow that can query APIs, databases, or calculators during generation to fetch facts. | Message history + tool execution records. | Moderate (1–2s depending on tool calls). | Deterministic tool-calling loop (`maxSteps: 3–5`) with schema validation. |
| **Autonomous Agent** | Goal-oriented task execution with open-ended planning, retries, self-correction, and multiple tools. | Graph/State machine + persistent task memory. | Asynchronous (multi-second/minutes). | State machine / orchestrator with human checkpoints and event bus. |

---

## 2. Streaming Protocol & Lifecycle Management

In production web applications, raw synchronous completions degrade UX and trigger cloud function timeouts (e.g., 10s or 15s serverless limits). Streaming is mandatory for interactive chats.

### Standard Streaming Protocol (Server-Sent Events)
Use standardized SSE or the Data Stream Protocol to transmit distinct chunk types:
- `text-delta`: Incremental text tokens for smooth typewriter rendering.
- `tool-call`: Tool identification and streaming argument chunks.
- `tool-result`: Output from executed backend tools.
- `reasoning-delta`: Extended thinking/scratchpad tokens (rendered in collapsible UI).
- `error`: Structured error codes without terminating the HTTP channel silently.

### Implementation Pattern (TypeScript / Node / Vercel AI SDK)
```typescript
import { streamText, tool } from 'ai';
import { openai } from '@ai-sdk/openai';
import { z } from 'zod';

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = streamText({
    model: openai('gpt-4o'),
    system: 'You are a technical support assistant. Be concise and accurate.',
    messages,
    maxSteps: 5, // Allow multi-step tool loops
    tools: {
      getAccountStatus: tool({
        description: 'Fetch status for an account ID',
        parameters: z.object({ accountId: z.string().min(1) }),
        execute: async ({ accountId }) => {
          // Deterministic backend call
          return { accountId, active: true, tier: 'enterprise' };
        },
      }),
    },
    abortSignal: req.signal, // Propagate client cancellation
  });

  return result.toDataStreamResponse();
}
```

### Client Request Cancellation & Resource Cleanup
Always bind the HTTP `AbortController` to the model call:
- When a user navigates away or clicks "Stop Generating", the frontend calls `abort()`.
- The server receives `req.signal.aborted` and immediately closes the provider LLM connection.
- **Benefit**: Halts token billing instantly and prevents dangling headless executions.

---

## 3. Conversation Memory Management

Feeding raw, unbounded message history into every turn causes token inflation, degrades reasoning quality ("lost in the middle" effect), and eventually exceeds the model's context window.

### Memory Strategies

```
A. Sliding Window (Last N Turns)
   [System Prompt] + [Turn N-3] + [Turn N-2] + [Turn N-1] + [Current Turn]
   - Best for: Transactional, task-oriented chats (customer support, booking).
   - Pros: Zero latency overhead, strictly bounded token budget.
   - Cons: Loses context from turns prior to window.

B. Summarization Window
   [System Prompt] + [Rolling Summary of Turns 1..N-4] + [Turns N-3..Current]
   - Best for: Long, exploratory discussions (coaching, tutoring, long research).
   - Pros: Preserves key decisions across hours of dialogue.
   - Cons: Adds an extra background LLM summarization call; can drop subtle details.

C. Semantic Vector Memory
   [System Prompt] + [Vector-Retrieved Relevant Historical Messages] + [Current Turn]
   - Best for: Multi-session personalized assistants with weeks of history.
   - Pros: Scalable to infinite historical conversations.
   - Cons: Complex vector indexing; retrieved past messages may lack conversational coherence.
```

### Ephemeral Prompt Caching
Modern providers (Anthropic Claude, Google Gemini, OpenAI) support prompt caching for static prefixes.
- Keep the `System Prompt`, domain knowledge, and static tool definitions at the very beginning of the prompt.
- Append dynamic conversation turns at the end.
- Mark static blocks with provider cache control headers.
- **Result**: Up to 90% cost savings on multi-turn conversations and 80% reduction in TTFT.

---

## 4. Structured Outputs & Form Generation

When an AI chatbot must collect data or trigger actions, never rely on unstructured prose parsing or regex.

### Schema Enforcement
Use JSON Schema / Zod with native provider constrained decoding (`response_format: { type: "json_schema" }` or `generateObject` / `streamObject`):

```typescript
import { generateObject } from 'ai';
import { z } from 'zod';
import { anthropic } from '@ai-sdk/anthropic';

const TicketSchema = z.object({
  category: z.enum(['billing', 'technical', 'sales']),
  priority: z.enum(['low', 'medium', 'high', 'urgent']),
  summary: z.string().max(100),
  actionItems: z.array(z.string()),
});

export async function extractTicket(conversationTranscript: string) {
  const { object } = await generateObject({
    model: anthropic('claude-3-5-sonnet-20241022'),
    schema: TicketSchema,
    prompt: `Analyze the following transcript and generate a support ticket:\n\n${conversationTranscript}`,
  });

  return object; // Guaranteed to match TicketSchema at runtime
}
```

---

## 5. Common Failure Modes & Mitigations

| Failure Mode | Root Cause | Engineering Mitigation |
|---|---|---|
| **Infinite Tool Loop** | Model repeatedly calls tools with minor parameter variations when an error is returned. | Enforce `maxSteps: 5`. Implement loop detection: if identical tool arguments occur twice consecutively, terminate and return an error to user. |
| **Context Window Overflow** | Unbounded chat array sent on turn 30+. | Implement a sliding window retaining the system prompt + last 10 messages max. Count tokens with a fast tokenizer prior to API dispatch. |
| **Hanging Client Streams** | Serverless function terminates or drops TCP connection before emitting stream end marker. | Wrap stream generators in `try/catch/finally` blocks with explicit error frames and client-side heartbeat timeouts (e.g. 15s). |
| **Prompt Injection via Past History** | Attacker injects fake "assistant" messages into the request body history array to bypass instructions. | Sanitize history: Validate that incoming client messages strictly conform to the expected user role, and never trust unverified history records. |
