# OWASP Standards: 2025–2026 Reference Guide

Official reference mappings for **OWASP Top 10:2025**, **ASVS 5.0** (May 2025), **OWASP Top 10 for LLM Applications (2026)**, and **OWASP Top 10 for Agentic Applications (2026)**.

---

## 1. OWASP Top 10:2025

| Category | Title | Focus & Key Prevention |
|---|---|---|
| **A01** | **Broken Access Control** | Deny by default. Enforce object-level ownership (IDOR/BOLA). Server-side authorization checks on every endpoint. Explicitly covers Server-Side Request Forgery (SSRF). |
| **A02** | **Security Misconfiguration** | Harden server/framework configs; disable default accounts/debug flags; disable XML external entities (XXE); minimize unnecessary features and open ports. |
| **A03** | **Software Supply Chain Failures (NEW)** | Lock dependency versions (`package-lock.json`, `uv.lock`); verify package signatures; block unreviewed install scripts; prevent typosquatting and dependency confusion. |
| **A04** | **Cryptographic Failures** | Mandate TLS 1.2+ for all traffic. Use AES-256-GCM / ChaCha20-Poly1305. Hash passwords with Argon2id or bcrypt (≥12 rounds). Ban ECB mode and unauthenticated CBC. |
| **A05** | **Injection** | Parameterize all SQL/NoSQL queries. Pass arguments as arrays to OS processes (avoid shell concatenation). Allowlist-based schema validation. |
| **A06** | **Insecure Design** | Threat model before building. Implement rate limiting and replay prevention. Prevent check-then-write race conditions. Maintain strict tenant isolation. |
| **A07** | **Authentication Failures** | NIST 800-63b alignment. Block top 3,000 common passwords. Check breached password sets. Disallow forced periodic password expiration. Multi-factor authentication (MFA). |
| **A08** | **Software or Data Integrity Failures** | Ban insecure deserialization (Python `pickle`, Java `ObjectInputStream`). Verify code signatures and plugin checksums. Enforce Subresource Integrity (SRI) for CDN scripts. |
| **A09** | **Security Logging and Alerting Failures** | Structured audit logging for security events (auth failures, access denial). Prevent log injection (sanitize CR/LF). Ship logs off-box to tamper-resistant stores with real-time alerts. |
| **A10** | **Mishandling of Exceptional Conditions (NEW)** | Fail-closed security architecture. Never leak stack traces, SQL errors, or internal paths to clients. Ensure atomicity and rollbacks on partial transaction failures. |

---

## 2. OWASP Top 10 for LLM Applications (2026 Edition)

| 2026 ID | Risk Name | Core Mitigation |
|---|---|---|
| **LLM01** | **Prompt Injection** | Treat all external content (user input, RAG chunks, tool outputs) as untrusted data. Enforce permissions in server-side code, not prompt wording. |
| **LLM02** | **Sensitive Information Disclosure** | Restrict retrieval at the database/RAG level before passing to model context. Sanitize PII from embeddings. |
| **LLM03** | **Excessive Agency** | Principle of least privilege on tool access. Require explicit human confirmation for destructive actions. Scope API keys per task. |
| **LLM04** | **Supply Chain** | Verify model weights, provenance, and hashes. Vet third-party hubs. Lock model versions and LoRA adapters. |
| **LLM05** | **Data and Model Poisoning** | Validate fine-tuning and pre-training datasets. Anomaly detection on data ingestion pipelines. |
| **LLM06** | **Unbounded Consumption** | Hard token caps, spend ceilings, rate limits, and recursion depth limits to prevent wallet exhaustion and DoS. |
| **LLM07** | **Misinformation (Slopsquatting)** | Ground high-stakes answers with citations. Guard against hallucinated package names registered by adversaries (*slopsquatting*). |
| **LLM08** | **Hidden Context Exposure** | Assume system prompts, tool schemas, and developer instructions can be extracted. Never hide secrets or authorization logic in prompt text. |
| **LLM09** | **Vector and Embedding Weaknesses** | Tenant-partition vector databases. Access-control on semantic retrieval. Guard against embedding inversion attacks. |
| **LLM10** | **Improper Output Handling** | Treat all LLM outputs (code, SQL, JSON) as untrusted input. Validate against strict schemas before passing to execution sinks. |

---

## 3. OWASP Top 10 for Agentic Applications (2026 Edition - ASI01 to ASI10)

| Risk ID | Title | Description & Prevention |
|---|---|---|
| **ASI01** | **Agent Goal Hijack** | Malicious content steers agent objectives. Enforce boundary guardrails in code; monitor goal drift. |
| **ASI02** | **Tool Misuse & Exploitation** | Tools executed in unintended ways. Enforce fine-grained schema validation on tool inputs and outputs. |
| **ASI03** | **Identity & Privilege Abuse** | Inherited ambient credentials across tool calls. Issue short-lived, scoped tokens per task step. |
| **ASI04** | **Agentic Supply Chain** | Compromised MCP servers or tools. Containerize/sandbox MCP runtimes; verify signatures. |
| **ASI05** | **Unexpected Code Execution** | Autonomous code generation executed in host environment. Require isolated sandbox containers and human approval. |
| **ASI06** | **Memory & Context Poisoning** | Malicious instructions stored in long-term memory or RAG. Segment memory by trust tier; enforce memory decay. |
| **ASI07** | **Insecure Inter-Agent Comm** | Spoofed or intercepted messages between subagents. Mutual TLS, cryptographic signing, and zero-trust validation. |
| **ASI08** | **Cascading Failures** | Infinite retry loops or errors propagating across agents. Circuit breakers, max step limits, exponential backoff. |
| **ASI09** | **Human-Agent Trust Exploitation**| Deceptive multi-turn interactions persuading humans to approve risky actions. Display clear diffs and impact summaries. |
| **ASI10** | **Rogue Agents** | Compromised agents behaving maliciously. Implement hard kill switches and centralized telemetry monitoring. |

---

## 4. OWASP ASVS 5.0 (May 2025 Overhaul)

ASVS 5.0 completely reorganized requirements into 17 chapters:
- **V1**: Encoding and Sanitization
- **V2**: Validation and Business Logic
- **V3**: Web Frontend Security
- **V4**: API and Web Service
- **V5**: File Handling
- **V6**: Authentication (6.2.1: min 8 chars; 6.2.4: block top 3000 common passwords; 6.2.5: permit all characters & paste; 6.2.10: no forced periodic rotation; 6.2.12: breached-password checks [L2]; 6.3.3: MFA [L2, L3 FIDO hardware key])
- **V7**: Session Management (7.2.3: CSPRNG 128+ bit tokens; 7.2.4: new token on auth/re-auth; 7.4.1: session invalidation on logout)
- **V8**: Authorization (8.2.1: function-level; 8.2.2: data-level IDOR mitigation; 8.3.1: server-side enforcement)
- **V9**: Self-contained Tokens
- **V10**: OAuth and OIDC
- **V11**: Cryptography (11.3.1: no ECB; 11.3.2: approved ciphers)
- **V12**: Secure Communication (12.1.1: TLS 1.2+)
- **V13**: Configuration
- **V14**: Data Protection (14.2.1: no sensitive data in URLs)
- **V15**: Secure Coding and Architecture
- **V16**: Security Logging and Error Handling (**Note**: ASVS 5.0 has **zero L1 logging requirements**; all logging starts at L2)
- **V17**: WebRTC

---

## 5. False-Positive Triage Rubric (Rule of 4)

Confirm all 4 criteria before reporting any finding:
1. **Attacker Control**: Trace input back to a true external entry point (request param, header, upload, webhook, LLM output). Constants and internal configs are not injection sources.
2. **Sink Reachability**: Verify no middleware, ORM, or sanitizer sits between input and sink. Check centralized auth middleware before flagging routes.
3. **Blast Radius**: Determine what tenant, data, or system boundary is crossed.
4. **Attacker Capabilities**: Confirm the attacker can perform every step from their position. If preconditions cannot be confirmed, rate as "Needs verification".

---

## 6. Standard Security Finding Block

```text
[SEVERITY] Title (CWE-###, OWASP A##:2025, LLM## Risk Name, ASI## Risk Name)
Location:   path/to/file.ext:LINE
Path:       <entry point> -> <intermediate hops> -> <sink>
Impact:     who can trigger it, what they get, which trust boundary it crosses
Fix:        the concrete change with code snippet
Confidence: Confirmed | Likely | Needs verification
```
