# Security Controls and Asset Categories

Use this checklist to maintain consistency across threat modeling sessions. Prefer concrete, system-specific items over generic text.

## Asset Categories (select applicable items)
- **User Data**: PII, user-generated content, document uploads, financial records.
- **Authentication Artifacts**: Passwords, session cookies, JWTs, OAuth refresh tokens.
- **Authorization State**: RBAC roles, tenant memberships, ACL policies.
- **Secrets and Keys**: API keys, HMAC signing secrets, TLS private keys, DB credentials.
- **Configuration & Feature Flags**: Runtime flags, tenant toggles, environment variables.
- **Models & Weights**: ML weights, embedding indexes, prompt templates, vector stores.
- **Source Code & Build Artifacts**: CI secrets, build pipelines, docker registries.
- **Audit Logs & Telemetry**: Security event logs, access trails, transaction telemetry.
- **Availability-Critical Resources**: Message queues, Redis caches, rate limit buckets, compute budgets.
- **Tenant Isolation Boundaries**: Row-level policies, tenant identifiers, schema partitions.

## Security Control Categories
- **Identity & Access**: AuthN, AuthZ, session revocation, mTLS, asymmetric key rotation.
- **Input Protection**: Schema validation (Zod, Pydantic), parser hardening, upload sanitization, sandbox isolation.
- **Network Safeguards**: TLS 1.3, internal network policies, reverse proxy WAF, IP allowlists, DoS burst controls.
- **Data Protection**: AES-256-GCM encryption at rest, envelope encryption, automated redaction of sensitive logs.
- **Isolation Boundaries**: Process sandboxing, microVMs, Docker seccomp profiles, multi-tenant RLS.
- **Observability**: Tamper-resistant audit trails, alert thresholds, anomaly detection, off-box log shipping.
- **Supply Chain**: Dependency lockfiles, SBOM generation, checksum pinning, minimal runtime images.

## Grounded Mitigation Phrasing Patterns
- *"Enforce strict Zod/Pydantic schema at `<boundary>` for `<payload>` before parsing in `<service>`."*
- *"Require tenant-scoped ownership verification in DB query for `<resource>` in `<handler>` to eliminate IDOR."*
- *"Pin DNS resolution and drop private IP addresses (RFC 1918) in `<webhook-service>` to prevent SSRF."*
- *"Run untrusted document parser `<component>` in an unprivileged, isolated sandbox with strict cgroup memory caps."*
- *"Rate-limit `<endpoint>` by authenticated tenant ID and client IP with sliding window token buckets."*
