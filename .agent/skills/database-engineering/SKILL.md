---
name: database-engineering
description: Best practices, schema migrations, async connection pooling, and Row-Level Security (RLS) management for PostgreSQL (pgvector) and SQLite with SQLAlchemy 2.0. Trigger when configuring, auditing, migrating, normalizing, or optimizing database connections and queries.
---

# Database Engineering & Resilience Skill

This skill defines standards and procedures for high-performance, security-hardened database operations across PostgreSQL (pgvector) and SQLite within asynchronous Python architectures.

## Core Directives

### 1. Connection Normalization & Zero Hardcoding
- Never hardcode hostnames (`localhost`, `127.0.0.1`), ports, passwords, or database paths directly in code.
- Always load database configuration via centralized, validated Pydantic settings (`app.core.config.Settings`).
- Provide robust environment variable fallbacks:
  - If `DATABASE_URL` is set, prefer it.
  - Automatically normalize driver prefixes (`postgres://` or `postgresql://` $\rightarrow$ `postgresql+asyncpg://`, `sqlite://` $\rightarrow$ `sqlite+aiosqlite://`).
  - Support fallback SQLite demo database when PostgreSQL is unavailable or in offline environments.

### 2. Async Connection Pooling (SQLAlchemy 2.0 + asyncpg)
- Use singleton engine and sessionmaker factories (`AsyncEngine`, `async_sessionmaker[AsyncSession]`).
- Enable `pool_pre_ping=True` to prune stale/dropped sockets.
- Set appropriate pool boundaries for production: `pool_size=10-20`, `max_overflow=10`, `pool_timeout=30.0`, `pool_recycle=1800`.
- In SQLite mode, use `NullPool` or `StaticPool` with appropriate thread isolation.

### 3. PostgreSQL Row-Level Security (RLS) Enforceability
- Tenant isolation must be strictly enforced at the SQL kernel level using PostgreSQL RLS policies (`SET LOCAL app.user_id = :user_id`).
- When operating in SQLite fallback mode, detect dialect (`if "sqlite" in bind.dialect.name: return`) and enforce user scoping at the ORM query level.

### 4. Health Probes & Connection Verifications
- Implement non-blocking database readiness checks (`SELECT 1`).
- Gracefully handle database transient disconnects with exponential backoff and structured error logs.
- Never leak database credentials in error messages, exception traces, or HTTP responses.
