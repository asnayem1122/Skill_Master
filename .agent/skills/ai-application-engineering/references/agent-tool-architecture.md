# Agent & Tool Architecture

This reference guides the engineering of tool-calling assistants, autonomous agents, execution loops, state machines, and multi-agent coordination.

---

## 1. Tool Design Principles: The Narrow Schema Rule

A tool provided to an LLM must be a **narrow, purpose-built interface**, not a raw database client or wide-open REST proxy.

### Golden Rules of Tool Schema Engineering
1. **Minimal Surface Area**: Expose only the exact parameters the model needs to complete the specific sub-task.
2. **Explicit Type Constraints**: Use Zod or JSON Schema with strict enums, regex patterns, minimums, maximums, and string lengths.
3. **Comprehensive Descriptions**: Explain not just what the tool does, but when to use it, what units are expected (e.g. `currencyInCents`, `timestampIso8601`), and what errors mean.
4. **No Free-Form Code Execution Without Sandboxes**: Never expose tools that execute shell commands or arbitrary SQL queries directly against production databases.

### Schema Example (TypeScript / Zod)
```typescript
import { z } from 'zod';
import { tool } from 'ai';

export const refundCustomerTool = tool({
  description: 'Initiate a partial or full refund for a customer order. Requires customer confirmation.',
  parameters: z.object({
    orderId: z.string().regex(/^ord_[a-zA-Z0-9]+$/, 'Order ID must start with ord_'),
    amountInCents: z.number().int().positive().max(500000, 'Refunds cannot exceed $5,000 per transaction'),
    reason: z.enum(['defective_item', 'customer_request', 'duplicate_charge', 'fraud']),
    idempotencyKey: z.string().uuid().describe('Client-generated UUID to prevent duplicate charges'),
  }),
  execute: async ({ orderId, amountInCents, reason, idempotencyKey }, { abortSignal }) => {
    // Deterministic execution logic with auth checks
    return await processRefundService({ orderId, amountInCents, reason, idempotencyKey });
  },
});
```

---

## 2. Authorization & Security: The Out-of-Model Rule

> [!CRITICAL]
> **Keep Permissions & Business Logic Outside the LLM.**
> Never prompt the model: *"You are only allowed to see data for tenant 42"*. An LLM prompt is not an authorization boundary. Prompt injections can bypass instruction-based access control trivially.

### Correct Architectural Pattern:
1. The user authenticates via JWT / session cookie.
2. The server extracts `userId` and `tenantId` from the verified session token.
3. When the LLM decides to call `getInvoice({ invoiceId })`:
   - The tool execution handler intercepts the call.
   - The handler automatically binds `tenantId` from the verified session:
     ```sql
     SELECT * FROM invoices WHERE id = :invoiceId AND tenant_id = :sessionTenantId;
     ```
   - If the invoice belongs to another tenant, the backend returns a 403 error. The LLM cannot access unauthorized data regardless of prompt injection.

---

## 3. Idempotency & Execution Safety

LLM agents frequently retry actions or call tools multiple times when responses are delayed or ambiguous.

### Idempotency Keys
For any state-mutating tool (creating records, charging credit cards, sending emails, deleting resources):
- Require an `idempotencyKey` in the tool parameter schema.
- Store execution records in a cache/database (`idempotency_keys: { key, result, timestamp }`).
- If a tool is called twice with the same key within a time window (e.g. 5 minutes), return the cached previous result without re-executing the underlying mutation.

### Human-in-the-Loop (HITL) Confirmation Pattern
Categorize tools into **Read-Only (Auto-Execute)** vs **Mutating / Dangerous (Requires Confirmation)**:

```
[Agent plans action]
        │
Is tool mutating/dangerous? (e.g. deleteResource, chargePayment, sendPublicEmail)
   ├── NO  ──► Execute immediately ──► Return result to Agent
   └── YES ──► Emit `requires_action` event with payload to client
                    │
               [User sees UI confirmation modal: Approve / Reject]
                    │
               ├── APPROVED ──► Server executes tool ──► Agent resumes
               └── REJECTED ──► Server returns rejection error ──► Agent adapts
```

---

## 4. Single Orchestrator vs Multi-Agent Systems

A widespread anti-pattern in AI engineering is creating complex multi-agent graphs with 5+ agents talking to each other for simple features.

### When to Use a Single Orchestrator (Default, 95% of use cases):
- Task can be solved by one LLM coordinating a set of 3–8 focused tools.
- Faster, lower cost, significantly easier to test, trace, and debug.
- Deterministic error handling.

### When Multi-Agent Systems Are Justified (5% of use cases):
1. **Strict Context Isolation**: Agent A operates on confidential financial data; Agent B writes public marketing copy. They must not share context windows.
2. **Conflicting System Instructions**: Two tasks require diametrically opposed personas or reasoning styles (e.g. an aggressive Red Team penetration testing agent vs a conservative Blue Team defensive hardening agent).
3. **Independent Specialization & Model Routing**: Step 1 requires a large multimodal reasoning model (Gemini 1.5 Pro / GPT-4o), while Step 2 performs thousands of fast text classifications where a tiny local model (Llama-3-8B / Mistral) is 100x cheaper.

### Multi-Agent Governance Rules
- Enforce strict typed contracts at agent handoffs (JSON schemas, not open prose).
- Cap the total interaction steps across the entire network (e.g. global `maxNetworkSteps = 15`).
- Maintain a single central audit log tracking which agent made which decision.
