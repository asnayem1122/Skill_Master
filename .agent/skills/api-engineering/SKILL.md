---
name: api-engineering
description: >-
  Comprehensive API design, contract enforcement, client normalization, and
  interface architecture. Use when designing REST/GraphQL endpoints, establishing
  type contracts between frontend and backend, configuring dynamic base URLs, or
  handling RFC 7807 error semantics.
---

# API Engineering & Interface Design

Design stable, well-documented, resilient interfaces that are hard to misuse. Good interfaces make the right thing easy and the wrong thing hard. Enforces contract-first design, zero-hardcoding environment configuration, RFC 7807 Problem Details, and robust frontend-backend client communication.

---

## When to Use This Skill

- Designing new REST endpoints, GraphQL schemas, or service APIs
- Defining inter-module boundaries, type contracts, and data transfer objects (DTOs)
- Auditing or refactoring API clients, base URL resolution, and CORS middleware
- Implementing authentication token lifecycle, retries, and error handling
- Evolving public interfaces while preventing breaking changes (Hyrum's Law)

---

## Core Design Principles

### 1. Hyrum's Law Awareness
> *With a sufficient number of users of an API, all observable behaviors of your system will be depended on by somebody, regardless of what you promise in the contract.*

- **Be intentional**: Every observable property, header, error message, and response order is a commitment.
- **Don't leak internals**: Never leak database column names, internal IDs, stack traces, or ORM quirks into public responses.
- **Extend, don't break**: Add optional fields; never rename or remove required fields without a deprecation window.

### 2. Contract-First Architecture
Define the schema and interface before writing implementation:
```typescript
interface TaskAPI {
  createTask(input: CreateTaskInput): Promise<Task>;
  listTasks(params: ListTasksParams): Promise<PaginatedResult<Task>>;
  getTask(id: string): Promise<Task>;
  updateTask(id: string, input: UpdateTaskInput): Promise<Task>;
  deleteTask(id: string): Promise<void>; // Idempotent
}
```

### 3. Dynamic API Base URL Resolution (Zero Hardcoded Hosts)
Never hardcode `http://localhost:8000` or IP addresses in application code.

- **Frontend Client (`api-client.ts`)**:
  1. Read `process.env.NEXT_PUBLIC_API_BASE_URL` (e.g., `/api/v1` for proxy/rewrite setups).
  2. Fall back to relative `/api/v1` in browser contexts.
  3. Use server-side runtime `BACKEND_URL` or `INTERNAL_API_URL` during SSR.
- **Next.js Rewrites (`next.config.mjs`)**:
  - Configure upstream destination via `process.env.BACKEND_URL || "http://127.0.0.1:8000"`.
- **Edge Middleware (`middleware.ts`)**:
  - Dynamically inject CSP `connect-src` based on environment and backend URLs.

---

## Error Handling & RFC 7807 Standard

Enforce RFC 7807 Problem Details uniformly across all endpoints:

```json
{
  "type": "https://api.example.com/errors/validation-failed",
  "title": "Validation Failed",
  "status": 422,
  "detail": "Field 'email' is required and must be a valid email format.",
  "instance": "/api/v1/users/123",
  "invalid_params": [
    { "name": "email", "reason": "Invalid format" }
  ]
}
```

### HTTP Status Code Semantics
| Code | Meaning | When to Use |
|:-----|:--------|:------------|
| **200 OK** | Success | Standard GET, PUT, PATCH responses |
| **201 Created** | Resource Created | Successful POST creation (include `Location` header) |
| **204 No Content**| Success, No Body | Successful DELETE or empty action |
| **400 Bad Request**| Malformed Syntax | JSON parse errors or malformed payloads |
| **401 Unauthorized**| Missing / Invalid Auth | Missing or expired token (triggers refresh flow) |
| **403 Forbidden** | Authenticated, Not Allowed | Missing required role or permissions |
| **404 Not Found** | Missing Resource | URL or resource ID does not exist |
| **409 Conflict** | State Conflict | Duplicate unique key or optimistic concurrency mismatch |
| **422 Unprocessable**| Semantic Validation Error | Schema parsed but business validation failed |
| **429 Rate Limited**| Too Many Requests | Rate limit exceeded (include `Retry-After`) |
| **500 Server Error**| Internal Failure | Unhandled exceptions (never leak trace to client) |

---

## Client Normalization & Auth Lifecycle

### 1. Token Refresh & Retries
- Store short-lived access tokens in memory; keep refresh tokens in `HttpOnly, Secure, SameSite=Strict` cookies.
- On receiving a `401 Unauthorized`, intercept the response, attempt a single token refresh, and replay the original request.
- If refresh fails, clear auth state and redirect cleanly to login.

### 2. Request & Response Normalization
- Enforce strict schemas via Zod / Pydantic / TypeScript types.
- Provide bidirectional normalization for enum variants (e.g. `expense` $\leftrightarrow$ `payment`).
- Strip undefined / null values where appropriate and sanitize input query parameters.

---

## Pagination & List Design

Always paginate unbounded collections. Avoid unbounded queries:
```typescript
interface PaginatedResult<T> {
  items: T[];
  pagination: {
    cursor?: string;       // Cursor-based for high-scale or streaming feeds
    page: number;          // Page-based for administrative UI tables
    pageSize: number;
    totalItems: number;
    hasNextPage: boolean;
  };
}
```

---

## Pre-Merge API Checklist

- [ ] Base URLs are dynamically resolved from environment variables
- [ ] Inputs are validated at the edge using schemas (Zod/Pydantic)
- [ ] Errors return standardized RFC 7807 Problem Details
- [ ] Responses are paginated; no unbounded queries
- [ ] No internal implementation details or secrets leaked
- [ ] Idempotency supported for state-modifying actions (PUT/DELETE/Idempotency-Key)
