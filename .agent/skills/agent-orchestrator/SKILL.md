---
name: agent-orchestrator
description: Act as an orchestrator that splits a complex task into narrow sub-agent roles (researcher, writer, coder, verifier, etc.), defines each role's tools, constraints and output schema, and checks every handoff so errors and hallucinations don't compound. Use this whenever the user mentions multi-agent systems, sub-agents, orchestration, agent roles, delegating work to agents, planner/worker/verifier patterns, or wants research, coding, writing or analysis done "without hallucinations" by several cooperating agents, even if they don't say "orchestrator".
---

# Agent Orchestrator

Split work across narrow sub-agents and verify every handoff. Splitting alone does not stop hallucination: it only shrinks each agent's context so mistakes are easier to spot. The real protection is version-pinned evidence, source authority tiers, empirical test gates, and an independent verifier.

## 1. Environment & Triage Check (do this first)

### Runtime Mode
- **Sub-agent runtime (Agentic IDE / SDK):** Define and dispatch isolated sub-agents using the templates in `assets/agents/`. For payloads >40 lines, write JSON outputs to `.orchestrator/runs/<task_id>/` and pass file paths via `input_ref` and `output_ref` to prevent context bloat and JSON escaping errors.
- **Single-agent / Plain chat (no sub-agent tool):** Run each role yourself as a separate, strictly labeled pass (`[PASS: PLANNER]`, `[PASS: RESEARCHER]`, `[PASS: CODER/WRITER]`, `[PASS: VERIFIER]`). The Verifier pass must evaluate ONLY the raw evidence and quote the exact matching substring side-by-side with each claim, ignoring your earlier reasoning. Tell the user this is simulated.

### Complexity Triage
- **Fast-Path (1-2 files or single-question verification):** Skip Planner. Run `Researcher -> Writer/Coder -> Verifier`.
- **Full Pipeline (multi-module code, deep research, or high ambiguity):** Run `Planner -> Researcher(s) -> Writer/Coder -> Verifier (+ Critic/Security if high-stakes)`.

## 2. Workflow

1. **Pin Environment.** Before researching external docs, inspect local manifests (`package.json`, `Cargo.toml`, `CMakeLists.txt`, `pyproject.toml`, compiler/OS version) so agents never pull evidence for the wrong version.
2. **Decompose.** Write 2-6 subtasks. Each needs: goal, input, output, done-criteria. Merge subtasks that cannot be verified on their own.
3. **Assign Roles.** Pick from `references/roles.md`. One role, one job. Fewer agents is better; add one only if it removes a real failure mode.
4. **Write Each Brief** using the Agent Brief Template below.
5. **Dispatch Safely.** Run independent subtasks in parallel, dependent ones in sequence. **Disjoint Write-Set Rule:** Never run two parallel `Coder` or `Writer` agents that modify the same file. Before a `Coder` edits tracked files, ensure a clean rollback path exists (`git diff` / backup).
6. **Gate & Short-Circuit Every Handoff.** Check every output against its schema in `references/schemas.md` and its evidence (see Gates). **Short-Circuit Rule:** If a `Researcher` returns `status: "insufficient_evidence"`, reformulate the search/inspection query at most ONCE; if still insufficient, halt downstream `Writer`/`Coder` passes for that branch and report the gap to the user.
7. **Verify Independently.** A Verifier that never saw the producer's reasoning checks each claim or code change against raw evidence and empirical test results.
8. **Surgical Decide.** Accept, send back ONLY the specific failed claims/blocks for patching (max 2 retries; lock all already-verified items), or roll back and escalate to the user.
9. **Report & Clean Up.** Give the user the final result plus what was verified, what was not, and any open uncertainty. Remove temporary `.orchestrator/` scratch files unless debugging was requested.

## 3. Agent Brief Template

Every sub-agent gets exactly this, nothing more (extra context invites drift):

~~~text
ROLE: <one sentence>
TASK: <the single subtask>
ENVIRONMENT CONSTRAINTS: <pinned language/library versions, OS, build system>
INPUT: <raw evidence/files/paths, not summaries>
TOOLS ALLOWED: <minimal list>
RULES:
- Every claim or API usage must cite a source id from INPUT or a tool result.
- Pull a 1-3 sentence verbatim excerpt window around key facts so context and negations are preserved.
- Tag every finding with its trust tier (tier1, tier2, tier3) and verify version compatibility.
- Write long deliverables (>20 lines) to a file and reference the path in JSON to avoid escaping errors.
- If evidence is missing, return status "insufficient_evidence". Do not guess.
- Stay inside TASK. Do not do other roles' work.
OUTPUT: JSON matching the schema for this role in `references/schemas.md`
~~~

## 4. Gates (the anti-hallucination part)

- **Schema Gate:** Reject output that does not match its JSON schema or contains uncited claims.
- **Evidence & Version Gate:** Spot-check that cited sources actually contain the claim AND match `ENVIRONMENT CONSTRAINTS`.
- **Evidence Trust Hierarchy:**
  - `tier1` (Ground Truth): Local repository code, compiler/test execution output, official language/library specifications.
  - `tier2` (Secondary): Official maintainer GitHub issues, release notes, changelogs.
  - `tier3` (Untrusted Alone): Third-party blogs, forums, Q&A posts. `tier3` can never override `tier1`, and any code relying on `tier3` must pass an empirical test run.
- **Empirical Code Gate:** For `Coder` tasks, build/syntax/test execution (`verification_run.passed == true`) is mandatory. Text citations alone do not pass broken code.
- **Raw-Evidence Rule:** Pass originals downstream. Summaries lose detail, and that is where hallucinations start.
- **Independence Rule:** The Verifier receives only the deliverable, `claim_map`/`implementation_map`, and raw evidence. Never pass the producer's chain-of-thought.
- **Unknown Is Valid:** `"insufficient_evidence"` counts as a successful agent execution. Penalizing it forces agents to invent facts.
- **High-Stakes Gate** (security, destructive file ops, production configs): Run two independent verification passes or require explicit user approval.

## 5. Failure Handling

- **Surgical Retry:** When the Verifier rejects specific items, lock all `"supported"` items in `locked_items` and instruct the producer to patch or drop ONLY the `"unsupported"` or `"contradicted"` items.
- **Second Failure & Rollback:** After 2 failed retries, revert any unverified file edits on that branch and escalate to the user with the exact blocker.
- **Agent Disagreement:** Show the user both versions alongside the raw evidence and source tiers; never silently pick one.
- **Audit Trail:** Log every handoff using `handoff_log` so any error can be traced to the exact step that introduced it.

## 6. Final Report Format

~~~text
Result: <final answer or paths to modified files>
Verified: <claims/changes verified against tier1/tier2 evidence + build/test results>
Unverified / assumptions: <anything not checked or relying on tier3>
Disagreements or open questions: <if any>
~~~
