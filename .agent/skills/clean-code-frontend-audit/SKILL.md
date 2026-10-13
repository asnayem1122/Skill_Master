---
name: clean-code-frontend-audit
description: >-
  Provides end-to-end auditing and quality assurance procedures for Next.js 14 App Router, TanStack Query, and FastAPI backends. Use this skill when verifying dynamic data flows, eliminating mock fallbacks and hardcoded placeholders, testing Fast Refresh and production builds, running Vitest unit tests, and verifying live pages with Chrome DevTools.
---

# Clean Code & Frontend Audit Playbook

This skill outlines the standard operating procedure for auditing fintech full-stack web applications for hardcoding, mock leakage, broken data pipelines, and visual regressions.

---

## 1. Zero Hardcoding Audit Matrix

Ensure every data field rendered on the screen originates from the database through the API client.

### Common Hardcoding Pitfalls to Eliminate:
1. **Fallback Provider Defaulting**:
   - `mfs_provider: "bkash"` in API client mapping: Must use `t.mfs_provider || "upay"`.
2. **Hardcoded User IDs**:
   - Using static `"user-001"` or `"default-user"` in query endpoints: Must extract `current_user.id` from JWT session.
3. **Hardcoded Form Submissions**:
   - Omitting user-selected dropdown channels when sending requests to `/transactions` or `/cashouts`.
4. **Mock Dates**:
   - Hardcoding current timestamps like `"2024-01-01"`: Always use `datetime.now(timezone.utc)`.

---

## 2. TanStack Query Cache Invalidation Rules

When a user performs any write operation:
```typescript
// Example: Creating transaction or cash-out
onSuccess: () => {
  queryClient.invalidateQueries({ queryKey: ["dashboard-overview"] });
  queryClient.invalidateQueries({ queryKey: ["transactions"] });
  queryClient.invalidateQueries({ queryKey: ["anomalies"] });
}
```
*Never rely on page reload (`window.location.reload()`)*.

---

## 3. Chrome DevTools E2E Verification Protocol

Run through this procedure whenever changes are applied:
1. **Console Check**:
   - Call `list_console_messages` on each page (`/`, `/dashboard`, `/transactions`, `/coach`).
   - Confirm 0 errors and 0 accessibility warnings.
2. **DOM Snapshot**:
   - Call `take_snapshot` to inspect generated hierarchy and confirm values are dynamic.
3. **Visual Proof**:
   - Call `take_screenshot` to confirm CSS gradients, margins, and typography align with Upay Navy/Yellow theme.
4. **Unit Test Gate**:
   - Run `npm test -- --run` in `frontend/`. All tests must pass before committing.
