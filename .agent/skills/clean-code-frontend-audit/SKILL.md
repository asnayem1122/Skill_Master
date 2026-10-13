---
name: clean-code-frontend-audit
description: >-
  Provides end-to-end auditing and systematic de-hardcoding procedures across full-stack applications. Use this skill when asked to remove hardcoded values, eliminate mock fallbacks and fake placeholders, extract magic numbers into constants, replace hardcoded URLs/secrets with dynamic configs and environment variables, verify dynamic data pipelines, or audit clean code with Chrome DevTools.
---

# Clean Code & De-Hardcoding Playbook

This skill provides the comprehensive standard operating procedure for identifying, auditing, and systematically eliminating hardcoding, mock leakage, magic numbers, static fallbacks, and broken data pipelines across full-stack codebases.

---

## 1. The Zero-Hardcoding Master Matrix

Every piece of data rendered on the screen or processed in business logic must originate from a verified, single source of truth (database, validated environment variable, or typed constant registry).

### The 6 Archetypes of Hardcoding & How to Eliminate Them:

| Archetype | Common Antipattern | Remediation / Clean Code Pattern |
|:---|:---|:---|
| **1. Mock Data & Placeholders** | Hardcoded arrays, static `"user-001"`, dummy cards, `"John Doe"` | Replace with dynamic ORM/API queries. Render proper Loading Skeletons while fetching and Empty States if null. |
| **2. Magic Numbers & Literals** | `if (status === 3)`, `timeout = 5000`, `fee = 0.0185`, `limit = 20` | Extract to typed enum or frozen constant registry: `const HTTP_TIMEOUT_MS = 5000 as const;` or `class Status(IntEnum)`. |
| **3. URLs, Hostnames & Ports** | `fetch("http://localhost:8000/api/v1")` or hardcoded IP addresses | Centralize into environment config with runtime validation (Zod / Pydantic): `const API_URL = env.NEXT_PUBLIC_API_URL`. |
| **4. Secrets & Credentials** | API keys, JWT secrets, database connection URIs in source code | Move to `.env` + `.env.example`, ensure `.env` is in `.gitignore`, and access via secure configuration managers. |
| **5. Design Tokens & Styling** | Inline arbitrary styles: `style={{ width: "384px", color: "#1e3a8a" }}` | Use Tailwind design token classes (`w-96`, `text-primary`) or CSS custom properties (`var(--color-primary)`). |
| **6. Static Dates & Timestamps** | Hardcoding `"2024-01-01"` or fixed year strings | Use dynamic ISO/UTC utilities: `datetime.now(timezone.utc)` in Python, or `new Date().toISOString()` in JavaScript. |

---

## 2. Systematic De-Hardcoding Workflow

When executing a de-hardcoding refactor on a file or module:

### Step 1: Automated & Manual Detection Scan
Search for telltale signs of hardcoding:
```bash
# Search for hardcoded local/remote URLs:
rg "(http|https)://(localhost|127\.0\.0\.1|0\.0\.0\.0)" --glob "!*.env*"

# Search for typical dummy/mock names and IDs:
rg "(user-001|default-user|test@example\.com|John Doe|dummy|placeholder)"

# Search for inline credentials or API tokens:
rg "(api[_-]?key|secret|token|password)\s*[:=]\s*['\"][a-zA-Z0-9_\-]{8,}['\"]"
```

### Step 2: Extract to Central Configuration
- **Environment Settings**: Add new external variables to `.env.example` and validate them on startup using schemas (e.g. `z.object({...})` or `pydantic_settings.BaseSettings`).
- **Domain Constants**: Group domain-specific literals in a dedicated `constants/` or `config/` file with descriptive names (`MAX_RETRY_COUNT`, `DEFAULT_PAGE_SIZE`).
- **Data Models**: Ensure frontend interfaces strictly mirror backend DTOs/schemas.

### Step 3: Replace Call Sites with Typed Bindings
- Replace literal values with imported constants or config properties.
- Ensure all query parameters (e.g., active user ID, pagination offset, filter tags) are derived from the active session or URL state, never hardcoded.

### Step 4: Validate Data Invalidation & Dynamic Flows
When users perform any mutation or write operation:
```typescript
// TanStack Query / React Query example:
onSuccess: () => {
  queryClient.invalidateQueries({ queryKey: ["dashboard-overview"] });
  queryClient.invalidateQueries({ queryKey: ["transactions"] });
  queryClient.invalidateQueries({ queryKey: ["resource-list"] });
}
```
*Never rely on page reload (`window.location.reload()`) to refresh stale data.*

---

## 3. Chrome DevTools & E2E Verification Protocol

After eliminating hardcoded values, verify end-to-end dynamic behavior:

1. **Console Check**:
   - Inspect console output on affected pages using DevTools.
   - Confirm **0 unhandled errors** and **0 hydration mismatches** (common when dates are rendered dynamically).
2. **DOM Snapshot & Data Inspection**:
   - Inspect the DOM hierarchy to confirm elements display real dynamic data, not fallback mock strings.
3. **Visual & Layout Check**:
   - Confirm layouts handle dynamic length strings gracefully (e.g. ellipsis, line wrapping, responsiveness) rather than assuming fixed mock lengths.
4. **Automated Test Gate**:
   - Run the unit/integration test suite to verify no mocks were broken unintentionally:
     ```bash
     npm test -- --run   # or pytest / cargo test
     ```

---

## 4. De-Hardcoding Checklist Before Submitting Code

- [ ] **No Localhost/IPs**: Zero occurrences of `localhost`, `127.0.0.1`, or explicit ports in application code.
- [ ] **No Dummy Credentials**: No plain-text tokens, API keys, or database credentials committed.
- [ ] **No Mock Data Leakage**: Dummy user IDs, placeholder usernames, or hardcoded transaction records removed.
- [ ] **No Magic Numbers**: All business thresholds, timeouts, and limits extracted to named constants.
- [ ] **Environment Schema Validated**: Any new environment variable is added to `.env.example` and validated.
- [ ] **Tests Pass**: All unit, integration, and E2E tests pass cleanly.
