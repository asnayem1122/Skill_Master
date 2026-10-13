# Root Cause Tracing

Bugs often manifest deep in the call stack (e.g., a database query failing with an empty ID, a file created in the wrong directory, or a `TypeError` inside a utility helper). Fixing the line where the exception is thrown treats the symptom rather than the disease.

**Core Principle:** Trace backward through the call chain until you find the original trigger, then fix at the source.

---

## Backward Tracing Steps

1. **Observe the Symptom:** Note the exact error message and the line where execution halted.
2. **Find the Immediate Cause:** Identify which variable or state was invalid at that line.
3. **Trace One Level Up:** Find the caller that passed that invalid parameter or state.
4. **Repeat Until You Hit the Origin:** Keep walking up the call chain until you find where good state turned into bad state (e.g., unvalidated API payload, uninitialized test fixture, silent fallback returning `""` or `null`).
5. **Fix at the Source + Add Defense-in-Depth:** Fix the origin AND add guard clauses along the path.

---

## Adding Diagnostic Stack Instrumentation

When static code reading isn't enough to see which caller passed bad data, inject temporary diagnostic logging right before the failing operation:

```typescript
// Temporary diagnostic probe before the failing operation
console.error("DEBUG_TRACE:", {
  inputValue,
  cwd: process.cwd(),
  env: process.env.NODE_ENV,
  stack: new Error().stack,
});
```

> [!TIP]
> In test suites, use `console.error` or `sys.stderr.write` rather than application loggers, which are often mocked or silenced during test runs. Remove temporary probes once the root cause test is written and passing.
