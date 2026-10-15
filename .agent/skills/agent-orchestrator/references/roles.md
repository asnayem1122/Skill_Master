# Role Catalog

Use the smallest set of roles that covers the task.
- **Fast-Path:** Researcher -> Writer/Coder -> Verifier
- **Full Pipeline:** Planner -> Researcher -> Writer/Coder -> Verifier (+ Critic / Security Reviewer)

## Planner
- **Job:** Inspect project manifest files to pin environment versions, decompose the request into 2-6 verifiable subtasks, order dependencies, and define done-criteria.
- **Tools:** Read-only on the user request and project manifest/config files.
- **Constraint:** Produces a plan and environment constraints only; never writes deliverables or answers the prompt.

## Researcher
- **Job:** Gather version-matched evidence from the codebase or documentation and return sources with exact 1-3 sentence supporting excerpts.
- **Tools:** File read, grep, glob, web search, web fetch.
- **Constraint:** No conclusions beyond the evidence; quote verbatim excerpts, record source IDs, version/date metadata, and trust tier (`tier1`, `tier2`, `tier3`).

## Writer
- **Job:** Produce prose or documentation deliverables using ONLY the supplied evidence.
- **Tools:** File read/write/edit (scoped to output target), no web access.
- **Constraint:** Every factual sentence must map to an evidence ID; add no new facts. Write deliverables >20 lines to a file and return the path in JSON. On retry, edit only flagged sentences.

## Coder
- **Job:** Write or modify code using ONLY supplied evidence, existing repo symbols, and verified API documentation.
- **Tools:** File read/write/edit, compiler/linter/test runner (scoped), no arbitrary web guessing.
- **Constraint:** Never invent APIs, methods, or CLI flags. Map all changes to evidence IDs and run build/tests before returning. On retry, patch only flagged code blocks.

## Verifier
- **Job:** Check each claim or code change against raw evidence, source tiers, and test outputs; return `supported`, `unsupported`, or `contradicted` per item.
- **Tools:** Read-only file access, read-only test/build verification.
- **Constraint:** Never sees producer reasoning; never edits the deliverable; flags defects and locks passing items.

## Critic (optional)
- **Job:** Check for missing edge cases, algorithmic complexity bottlenecks, race conditions, or logic gaps. Separate from the Verifier, which checks factual and empirical accuracy.
- **Tools:** Read-only.

## Security Reviewer (optional, for code/AI-security work)
- **Job:** Check for injection, hardcoded secrets, memory safety bugs, over-broad permissions, and unsafe input handling.
- **Tools:** Read-only, static analysis. Never execute untrusted code.

## Synthesizer (optional, when running parallel researchers)
- **Job:** Merge parallel `researcher_output` payloads, deduplicate findings, and surface conflicts explicitly.
- **Constraint:** Keeps source IDs and tiers intact; never resolves conflicts silently.
