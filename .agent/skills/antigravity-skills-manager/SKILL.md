---
name: antigravity-skills-manager
description: >-
  Global skills manager & workflow orchestrator for Google Antigravity. Explore,
  search, install, and govern 300+ agent skills from the catalog, with automated
  phase discovery, lifecycle sequences, and core operating behaviors.
metadata:
  model: inherit
---

# 📦 Antigravity Skills Manager & Workflow Orchestrator

The `antigravity-skills-manager` is the central skill management CLI and meta-skill governance hub for Google Antigravity. It empowers agents and users to discover, search, install, and govern skills from the curated [`rmyndharis/antigravity-skills`](https://github.com/rmyndharis/antigravity-skills) catalog and orchestrates engineering lifecycle workflows.

---

## When to Use This Skill

- Starting a new session or deciding which skill applies to a task
- Searching, exploring, or installing agent skills via `skills-cli.js`
- Enforcing non-negotiable engineering behaviors and governance across tasks
- Auditing local workspace (`.agent/skills/`) or global (`~/.gemini/antigravity/skills/`) capabilities

---

## Part 1: Skill Discovery & Phase Mapping

When a task arrives, identify the development phase and apply the matching skill:

```
Task arrives
    │
    ├── Underspecified requirements? ────────→ interview-me
    ├── Raw concept, need variations? ───────→ brainstorming-ideas
    ├── Formalizing requirements & specs? ───→ spec-driven-development
    ├── Establishing quality bar contracts? ─→ constraint-driven-development
    ├── Have a spec, need bite-sized tasks? ──→ writing-plans
    ├── Implementing code in thin slices? ───→ incremental-implementation
    │   ├── UI components & styling? ────────→ frontend-ui-engineering / frontend-design
    │   ├── API contracts & endpoints? ──────→ api-engineering
    │   ├── Database schema & pooling? ──────→ database-engineering
    │   ├── Context window optimization? ────→ context-engineering
    │   ├── Doc-verified code? ──────────────→ source-driven-development
    │   └── High-stakes adversarial check? ──→ doubt-driven-development
    ├── Writing & executing tests? ──────────→ test-driven-development
    │   └── Real browser validation? ────────→ webapp-testing
    ├── Something broke or failed? ──────────→ troubleshooting-applications
    ├── Reviewing pull requests / diffs? ────→ code-review-excellence
    │   ├── Unnecessary complexity? ─────────→ code-simplification
    │   ├── Security vulnerabilities? ───────→ security-and-hardening
    │   └── Profiling & bottlenecks? ────────→ performance-optimization
    ├── Committing, semver & changelogs? ────→ git-pr-workflows-git-workflow
    ├── CI/CD pipeline automation? ──────────→ ci-cd-and-automation
    ├── Deprecating or migrating? ───────────→ deprecation-and-migration
    ├── Architecture decisions (ADRs)? ──────→ documentation-engineering
    ├── Logging, metrics & tracing? ─────────→ observability-and-instrumentation
    └── Production launch & rollouts? ───────→ shipping-and-launch
```

---

## Part 2: Non-Negotiable Core Operating Behaviors

These behaviors apply at all times across all skills:

1. **Surface Assumptions Early**:
   State assumptions explicitly before writing non-trivial code:
   ```
   ASSUMPTIONS I'M MAKING:
   1. [Assumption about requirements]
   2. [Assumption about existing architecture]
   → Correct me now or I will proceed with these.
   ```
2. **Manage Confusion Actively**:
   When specs or code conflict, **STOP**. Do not silently pick an arbitrary path. Name the inconsistency and ask for clarification.
3. **Push Back When Warranted**:
   You are an engineering partner, not a yes-machine. When an approach introduces security, scalability, or maintenance problems, quantify the impact and propose a simpler alternative.
4. **Enforce Simplicity (Anti-Overengineering)**:
   If 100 lines suffice, writing 1,000 lines is a failure. Prefer standard libraries and boring, obvious patterns.
5. **Maintain Scope Discipline**:
   Touch only what you are asked to touch. Never perform unsolicited refactoring of adjacent modules or delete unfamiliar comments.
6. **Verify Before Completion**:
   Never claim a task is complete without fresh terminal or test execution evidence. "Should work" is unacceptable.

---

## Part 3: Complete Feature Lifecycle Sequence

For an end-to-end feature delivery:
```
1. interview-me               → Clarify underlying user intent
2. brainstorming-ideas        → Explore approaches & trade-offs
3. spec-driven-development    → Author PRD and acceptance criteria
4. writing-plans              → Create dependency graph & vertical slices
5. test-driven-development    → Write failing tests before code
6. incremental-implementation → Implement thin slices to turn tests green
7. code-review-excellence     → Perform multi-axis pre-merge review
8. git-pr-workflows-git-workflow → Atomic commits, semver bump & PR description
9. shipping-and-launch        → Staged rollout and verification
```

---

## Part 4: Skills CLI Tool Usage

The repository includes a zero-dependency CLI (`skills-cli.js`) supporting project and global scopes:

```bash
# List catalog skills (filtered by keyword or category)
node skills-cli.js list [filter]

# Search catalog skills
node skills-cli.js search <keyword>

# List installed skills in current workspace
node skills-cli.js installed

# Install a skill from the catalog into workspace
node skills-cli.js install <skill-id>

# Install globally to ~/.gemini/antigravity/skills/
node skills-cli.js install <skill-id> --global

# Install a pre-configured bundle (e.g., core-dev, security-core)
node skills-cli.js bundle install <bundle-name>
```

---

## 10 Critical Failure Modes to Avoid

1. Making unverified assumptions without stating them
2. Plowing ahead blindly when confused or encountering contradictory code
3. Rubber-stamping bad ideas to be agreeable
4. Writing complex abstractions before the 3rd use case
5. Editing files orthogonal to the task
6. Removing code or comments you don't understand
7. Skipping written specs on architectural changes
8. Skipping failing tests in TDD
9. Declaring victory without fresh test execution output
10. Committing monolithic "everything" diffs
