# Detailed Error Handling & Resilience Patterns

This reference provides production-ready error handling, retry, circuit breaker,
and async resilience patterns across languages.

---

## 1. Custom Error Hierarchies Across Languages

### Python: Structured Application Exceptions

```python
from typing import Any, Optional

class ApplicationError(Exception):
    """Base error for all predictable domain/application errors."""
    def __init__(
        self,
        message: str,
        code: str = "APP_ERROR",
        status_code: int = 500,
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}

class ValidationError(ApplicationError):
    def __init__(self, message: str, field: Optional[str] = None) -> None:
        super().__init__(
            message,
            code="VALIDATION_ERROR",
            status_code=400,
            details={"field": field} if field else {},
        )

class NotFoundError(ApplicationError):
    def __init__(self, resource: str, identifier: Any) -> None:
        super().__init__(
            f"{resource} '{identifier}' not found",
            code="NOT_FOUND",
            status_code=404,
            details={"resource": resource, "id": str(identifier)},
        )

class ExternalServiceError(ApplicationError):
    def __init__(self, message: str, service: str, details: Optional[dict[str, Any]] = None) -> None:
        merged = {"service": service, **(details or {})}
        super().__init__(message, code="EXTERNAL_SERVICE_ERROR", status_code=502, details=merged)
```

### TypeScript: Result Type & Cause-Preserving Errors

```typescript
// Explicit Result type for expected failures (validation, parsing, domain rules)
export type Result<T, E = AppError> =
  | { ok: true; value: T }
  | { ok: false; error: E };

export const Ok = <T>(value: T): Result<T, never> => ({ ok: true, value });
export const Err = <E>(error: E): Result<never, E> => ({ ok: false, error });

// Structured Error class preserving ES2022 `cause`
export class AppError extends Error {
  constructor(
    message: string,
    public readonly code: string,
    public readonly statusCode: number = 500,
    public readonly context?: Record<string, unknown>,
    options?: ErrorOptions
  ) {
    super(message, options);
    this.name = this.constructor.name;
  }
}
```

### Rust & Go: Idiomatic Error Propagation

- **Rust:** Use `thiserror` for library/domain error enums and `anyhow` (with `.context("...")`) at application boundaries. Never `.unwrap()` in production paths unless the invariant is statically proven.
- **Go:** Wrap errors with context using `fmt.Errorf("fetching user %s: %w", id, err)` and inspect with `errors.Is(err, ErrNotFound)` or `errors.As(err, &targetErr)`.

---

## 2. Resilience Patterns

### Retry with Exponential Backoff & Jitter

Only retry **transient, idempotent** failures (network timeouts, `429`, `502`, `503`, `504`). Never retry `400`, `401`, `403`, or `422`.

```typescript
export async function retryWithBackoff<T>(
  operation: () => Promise<T>,
  options: {
    maxAttempts?: number;
    baseDelayMs?: number;
    shouldRetry?: (err: unknown) => boolean;
  } = {}
): Promise<T> {
  const {
    maxAttempts = 3,
    baseDelayMs = 200,
    shouldRetry = () => true,
  } = options;

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await operation();
    } catch (error) {
      if (attempt === maxAttempts || !shouldRetry(error)) {
        throw error;
      }
      // Full jitter: random between 0 and baseDelay * 2^(attempt-1)
      const cap = baseDelayMs * Math.pow(2, attempt - 1);
      const sleepMs = Math.random() * cap;
      await new Promise((resolve) => setTimeout(resolve, sleepMs));
    }
  }
  throw new Error("Unreachable");
}
```

### Circuit Breaker Pattern

Prevents cascading failures when a downstream service is degraded:
- **Closed:** Requests flow normally; failures increment a counter.
- **Open:** After reaching `failureThreshold`, fail fast immediately without calling the downstream service until `resetTimeoutMs` elapses.
- **Half-Open:** Allow a single probe request through; if it succeeds, close the circuit; if it fails, re-open immediately.

### Graceful Degradation & Fallbacks

When non-critical dependencies fail (e.g., recommendations service, analytics, avatar lookup):
1. Catch the specific `ExternalServiceError`.
2. Record a degraded metric/warning log.
3. Return cached data or a safe default value so the primary user flow succeeds.

---

## 3. Diagnostic Checklist by Symptom Type

| Symptom | First Diagnostic Command / Action | Typical Root Cause |
|:--------|:----------------------------------|:-------------------|
| `ECONNREFUSED` / `ETIMEDOUT` | Check target service port, env vars, DNS, and firewall | Service not running, wrong port/host in `.env`, Docker network mismatch |
| `401` / `403` in API | Inspect auth header format, token expiry, CORS preflight | Expired JWT, missing `Bearer ` prefix, wrong environment secret |
| `500 Internal Server Error` | Read server stderr / exception log for exact line | Unhandled null/undefined property, DB constraint error, missing migration |
| Flaky test passes locally, fails in CI | Search test for `sleep`/`setTimeout`, shared DB state, timezone | Race condition, test order pollution, hardcoded UTC vs local time |
| High memory / crash under load | Check unbounded arrays/maps, unclosed streams, N+1 queries | Event listener leak, missing pagination, connection pool exhaustion |
| Build works locally, fails in CI | Compare lockfiles, OS case sensitivity (`Foo.ts` vs `foo.ts`), Node/Python version | Untracked local file, case-insensitive macOS/Windows FS vs Linux CI |
