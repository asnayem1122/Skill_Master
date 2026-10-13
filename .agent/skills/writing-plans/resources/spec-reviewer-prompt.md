# Spec Document Reviewer Prompt

Use this template when reviewing a spec document before planning.

**Purpose:** Verify the spec is complete, consistent, and ready for
implementation planning.

## What to Check

| Category | What to Look For |
|:---------|:-----------------|
| Completeness | TODOs, placeholders, "TBD", incomplete sections |
| Consistency | Internal contradictions, conflicting requirements |
| Clarity | Requirements ambiguous enough to cause building the wrong thing |
| Scope | Focused enough for a single plan — not covering multiple independent subsystems |
| YAGNI | Unrequested features, over-engineering |

## Calibration

**Only flag issues that would cause real problems during implementation
planning.** A missing section, a contradiction, or a requirement so ambiguous
it could be interpreted two different ways — those are issues. Minor wording
improvements and stylistic preferences are not.

Approve unless there are serious gaps that would lead to a flawed plan.

## Output Format

```markdown
## Spec Review

**Status:** Approved | Issues Found

**Issues (if any):**
- [Section X]: [specific issue] - [why it matters for planning]

**Recommendations (advisory, do not block approval):**
- [suggestions for improvement]
```
