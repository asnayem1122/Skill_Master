---
name: security-and-hardening
description: >-
  Hardens code and reviews systems against modern security vulnerabilities using OWASP Top 10:2025, ASVS 5.0 (May 2025), OWASP Top 10 for LLM Applications (2026), and OWASP Top 10 for Agentic Applications (2026, ASI01-ASI10). Covers authentication, authorization, injection, software supply chain security, cryptography, error handling, rate limiting, and 4-step false-positive triage.
---

# Security and Hardening

Security-first engineering for web applications, APIs, and AI agent architectures. Treat every external input as hostile, every secret as sacred, and every authorization check as mandatory. Security is an architectural constraint across every line of code touching user data, authentication, external integrations, or autonomous agent actions.

---

## 1. When to Use This Skill

- Building or reviewing authentication, session management, or authorization (RBAC/ABAC)
- Handling external untrusted input (routes, forms, uploads, webhooks, third-party APIs, or LLM outputs)
- Auditing dependencies, package-manager lockfiles, or supply-chain integrity
- Designing or implementing LLM integrations, RAG pipelines, or autonomous tool-calling agents
- Performing pre-merge security code reviews or preparing for production compliance audits

---

## 2. The 4-Step False-Positive Triage Rubric

A pattern match is not a vulnerability. Before reporting or patching a security issue, confirm all 4 criteria:

1. **Attacker-Controlled Input**: Trace input back to a true external entry point (query param, header, body, webhook, upload, LLM response). Constants and internal configs are not injection sources.
2. **Sink Reachability**: Verify whether validation, allowlists, ORMs, or centralized middleware (`middleware.ts`, gateway proxies) already mitigate the path.
3. **Blast Radius**: Identify who can trigger it, what data or privilege they obtain, and whether it crosses tenant or system boundaries.
4. **Attacker Capability**: Confirm the attacker can perform every step from their position. If preconditions cannot be confirmed from available code, label as *"Needs verification"*, not High/Critical.

---

## 3. Modern Security Standards Matrix

### A. OWASP Top 10:2025
*(See [references/owasp-standards-2025-2026.md](references/owasp-standards-2025-2026.md) for full details)*
- **A01: Broken Access Control (includes SSRF)**: Deny by default; enforce object-level ownership (IDOR/BOLA); validate resolved IPs against private ranges (RFC 1918/4193).
- **A02: Security Misconfiguration**: Harden configs; disable default credentials and debug flags; disable XML external entities (XXE).
- **A03: Software Supply Chain Failures (NEW)**: Commit immutable lockfiles; pin manager versions; inspect install scripts before execution; audit registry provenance.
- **A04: Cryptographic Failures**: Enforce TLS 1.2+; use AES-256-GCM; hash passwords with Argon2id or bcrypt (≥12 rounds); ban ECB mode.
- **A05: Injection**: Parameterize all SQL/NoSQL queries; pass process arguments as arrays; never concatenate shell strings.
- **A06: Insecure Design**: Threat model before code; implement rate limiting; eliminate check-then-write race conditions.
- **A07: Authentication Failures**: NIST 800-63b compliance; block top 3,000 common passwords; check breached sets; no forced periodic rotation.
- **A08: Software or Data Integrity Failures**: Ban insecure deserialization (`pickle`, `ObjectInputStream`); enforce Subresource Integrity (SRI) on CDNs.
- **A09: Security Logging and Alerting Failures**: Structured logging for auth failures; sanitize against log injection; ship off-box with real-time alerting.
- **A10: Mishandling of Exceptional Conditions (NEW)**: Fail-closed; never expose stack traces or internal paths to clients; ensure atomicity on partial failures.

### B. OWASP Top 10 for LLM Applications (2026 Edition)
- **LLM01 Prompt Injection**: Treat user text and tool output as untrusted data; enforce boundaries in server code, not prompt wording.
- **LLM02 Sensitive Information Disclosure**: Filter PII at RAG retrieval time before reaching context.
- **LLM03 Excessive Agency**: Least-privilege tool scoping; require human confirmation for destructive actions.
- **LLM04 Supply Chain**: Verify model weights, signatures, and LoRA adapters.
- **LLM05 Data Poisoning**: Validate ingestion pipelines and fine-tuning datasets.
- **LLM06 Unbounded Consumption**: Hard ceilings on tokens, requests, and spend.
- **LLM07 Misinformation & Slopsquatting**: Ground answers with citations; guard against hallucinated dependencies.
- **LLM08 Hidden Context Exposure**: Assume system prompts and tool schemas are extractable; store zero secrets in prompt context.
- **LLM09 Vector & Embedding Weaknesses**: Tenant-isolate vector databases; enforce auth on similarity search.
- **LLM10 Improper Output Handling**: Treat LLM output as untrusted input; validate schemas before passing to SQL, DOM, or shell.

### C. OWASP Top 10 for Agentic Applications (2026 Edition - ASI01 to ASI10)
- **ASI01 Goal Hijack**: Prevent malicious content from steering agent objectives via rigid code guardrails.
- **ASI02 Tool Misuse**: Enforce strict schema validation on tool arguments and outputs.
- **ASI03 Identity Abuse**: Issue short-lived, task-scoped tokens instead of long-lived ambient credentials.
- **ASI04 Agentic Supply Chain**: Sandbox and containerize MCP servers and plugins; verify signatures.
- **ASI05 Unexpected Code Execution**: Sandbox autonomous code execution; mandate human approval for host changes.
- **ASI06 Memory Poisoning**: Segment agent memory by trust boundary; enforce memory decay.
- **ASI07 Insecure Inter-Agent Comm**: Cryptographically authenticate and sign messages between cooperating agents.
- **ASI08 Cascading Failures**: Circuit breakers, recursion limits, and exponential backoff across agent handoffs.
- **ASI09 Human-Agent Trust Exploitation**: Surface explicit diffs and blast-radius summaries in approval dialogs.
- **ASI10 Rogue Agents**: Implement hard kill switches, centralized telemetry, and tool-call anomaly detection.

### D. ASVS 5.0 Key Requirements (May 2025)
- **Levels**: Level 1 (Minimum Bar, ~20%), Level 2 (Standard Commercial, ~70% cumulative), Level 3 (High Assurance).
- **V6 Authentication**: Min 8 chars (6.2.1); allow all characters and paste (6.2.5); block top 3,000 common passwords (6.2.4); MFA required for L2 (6.3.3).
- **V7 Sessions**: CSPRNG tokens with 128+ bit entropy (7.2.3); new token on auth/re-auth (7.2.4); invalidate on logout (7.4.1).
- **V16 Logging**: **All security logging starts at Level 2**. ASVS 5.0 contains zero L1 logging requirements.

---

## 4. Hardening Controls & Implementation Rules

### 1. Input Validation & Parameterization
- Validate at the boundary with typed schemas (Zod, Pydantic). Reject malformed payloads with 422 and structured errors.
- Always use parameterized queries or trusted ORMs.

### 2. Authentication & Sessions
- Passwords hashed with Argon2id or bcrypt (≥12 rounds). Secrets loaded exclusively from environment variables.
- Session cookies must be `httpOnly`, `secure`, and `sameSite: 'lax'` or `'strict'`.

### 3. Response Security & Headers
- Enforce strict response headers: CSP (`default-src 'self'`), HSTS, `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`.
- Strip sensitive fields (`passwordHash`, reset tokens) before returning JSON.

### 4. Supply Chain & Dependency Hygiene
- Commit immutable lockfiles (`package-lock.json`, `pnpm-lock.yaml`, `uv.lock`).
- Block untrusted dependency install scripts before execution.
- Run native package manager audits (`npm audit`, `cargo audit`) and triage by reachable impact.

---

## 5. Security Finding Report Format

Report findings ordered by severity (Critical $\rightarrow$ High $\rightarrow$ Medium $\rightarrow$ Low $\rightarrow$ Info):

```text
[SEVERITY] Title (CWE-###, OWASP A##:2025, LLM## Risk Name, ASI## Risk Name)
Location:   path/to/file.ext:LINE
Path:       <entry point> -> <intermediate hops> -> <sink>
Impact:     who can trigger it, what they get, which trust boundary it crosses
Fix:        the concrete change with code snippet
Confidence: Confirmed | Likely | Needs verification
```
