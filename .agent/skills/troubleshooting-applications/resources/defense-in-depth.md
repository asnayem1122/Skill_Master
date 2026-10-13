# Defense-in-Depth & Condition-Based Waiting

Once you identify a root cause, single-point fixes can still be bypassed by alternative code paths, refactors, or mocks. Make the bug structurally impossible by validating at every layer, and eliminate timing guesses in async code.

---

## 1. The Four Validation Layers

When fixing bugs caused by invalid data or state, add checks across all four layers:

1. **Layer 1: Entry Point Validation (API / CLI / UI Boundary)**
   - Reject malformed, empty, or out-of-range inputs immediately with a `ValidationError` before any domain work begins.
2. **Layer 2: Business Logic Invariants**
   - Assert preconditions inside domain services and state machines so internal callers or mocks cannot pass invalid state.
3. **Layer 3: Environment & Safety Guards**
   - Prevent destructive operations (e.g., deleting files, dropping tables, calling live billing APIs) when running in `test` or `development` environments.
4. **Layer 4: Structured Forensic Telemetry**
   - Log key identifiers (`requestId`, `userId`, `orderId`, target path) before high-risk operations so future failures are immediately localizable.

---

## 2. Condition-Based Waiting (Fixing Flaky Async Tests & Race Conditions)

Flaky tests and async bugs frequently stem from guessing how long an operation takes (`setTimeout(r, 100)` or `time.sleep(0.5)`). Fast machines pass; loaded CI runners fail.

**Rule:** Wait for the observable condition you care about, not an arbitrary wall-clock delay.

```typescript
// ❌ BAD: Guessing how long async work takes
await new Promise((r) => setTimeout(r, 100));
expect(worker.status).toBe("ready");

// ✅ GOOD: Poll for the condition with a clear timeout message
export async function waitFor<T>(
  predicate: () => T | undefined | null | false,
  description: string,
  timeoutMs = 5000,
  intervalMs = 10
): Promise<T> {
  const start = Date.now();
  while (true) {
    const result = predicate();
    if (result) return result;
    if (Date.now() - start > timeoutMs) {
      throw new Error(`Timeout waiting for ${description} after ${timeoutMs}ms`);
    }
    await new Promise((r) => setTimeout(r, intervalMs));
  }
}
```
