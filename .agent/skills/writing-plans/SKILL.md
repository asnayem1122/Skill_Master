---
name: writing-plans
description: >-
  Creates structured, bite-sized implementation plans with vertical slicing,
  dependency graphs, task right-sizing, and TDD steps before touching code. Use
  when the user says "write a plan", "create an implementation plan", "plan this
  feature", or when breaking specs into verifiable tasks.
---

# Writing Implementation Plans

Write plans for an engineer or agent who has never seen this codebase or spec. Assume they write idiomatic code once they know the exact interface and exact test. What they cannot know is what you decided: which files, which names and signatures, which values from the spec, and which tests prove each task.

Decompose work into small, vertically sliced, verifiable tasks with explicit acceptance criteria. Good task breakdown is the difference between an agent that completes work reliably and one that produces a tangled mess.

**Announce at start:** *"I'm using the writing-plans skill to create the implementation plan."*

**Save plans to:** `docs/plans/YYYY-MM-DD-<feature-name>.md` (or `tasks/plan.md` if existing project convention).

---

## When to Use This Skill

- A spec, PRD, or design doc exists and needs to become actionable tasks
- User says "plan this", "write a plan", "implementation plan", "break this down"
- After a brainstorming or design phase produces an approved architecture
- A task feels too large or vague to start safely

## When NOT to Use

- Single-file changes with obvious scope
- Trivial bug fixes where the root cause is already isolated and regression test known

---

## Core Planning Principles

### 1. Vertical Slicing (Not Horizontal)
Instead of building all database tables, then all APIs, then all UI screens — build complete, working feature paths end-to-end:

```
❌ Bad (Horizontal Slicing):
Task 1: Build entire database schema
Task 2: Build all API endpoints
Task 3: Build all UI components
Task 4: Wire everything together (High risk integration collision)

✅ Good (Vertical Slicing):
Task 1: User Registration (Schema + API + UI form + tests)
Task 2: User Login & Session (Auth schema + token API + login UI + tests)
Task 3: Task Creation (Task schema + POST API + modal UI + tests)
```

### 2. Dependency Graph Mapping
Map foundations bottom-up so each task builds on completed, verified components:
```
Database migrations & domain models
    │
    ├── Domain validation & business logic
    │       │
    │       ├── API route handlers & middleware
    │       │       │
    │       │       └── Frontend API clients
    │       │               │
    │       │               └── UI components & page views
```

### 3. Task Sizing Guidelines

| Size | Files Changed | Scope | Action |
|:-----|:--------------|:------|:-------|
| **XS** | 1 | Single utility or config change | Combine into parent task |
| **S** | 1-2 | One component or endpoint + test | Ideal task size |
| **M** | 3-5 | One vertical feature slice + tests | Standard task size |
| **L** | 5-8 | Multi-component workflow | Split into S/M slices |
| **XL** | 8+ files | Too large — high failure rate | **Forbidden: Must decompose further** |

*Decompose further if:*
- It touches two independent subsystems
- Acceptance criteria exceed 3 bullet points
- You find yourself writing "and" in the task title

### 4. Verification Checkpoints
Insert explicit checkpoints after every 2-3 tasks:
```markdown
### 🛑 Checkpoint: After Tasks 1-3
- [ ] All unit and integration tests pass
- [ ] Application builds without warnings
- [ ] Core end-to-end flow verified manually or via browser test
- [ ] Review progress with user before proceeding
```

---

## Plan Document Template

```markdown
# [Feature Name] Implementation Plan

**Goal:** [One sentence describing what this builds]
**Architecture:** [2-3 sentences about approach and module boundaries]
**Tech Stack:** [Key technologies, libraries, and test runners]
**Spec:** [Path to the spec/design doc this plan implements]

## Global Constraints & Invariants
- [Version floors, dependency limits, zero-any policy, naming conventions]

## Dependency Graph & Ordering
1. Foundation & Domain Models
2. API Routes & Contracts
3. Frontend State & UI Components

---

### Task 1: [Slice Name]
**Files:**
- Create: `src/domain/user.ts`
- Modify: `src/db/schema.ts`
- Test: `tests/domain/user.test.ts`

**Interfaces:**
- Consumes: `DatabaseConnection` from `src/db/connection.ts`
- Produces: `createUser(data: UserInput): Promise<User>`

- [ ] **Step 1: Write failing test**
```typescript
test('creates active user with validated email', async () => { ... });
```
- [ ] **Step 2: Run test to verify failure**
Run: `npm test tests/domain/user.test.ts` → Expected: FAIL (createUser not defined)
- [ ] **Step 3: Implement minimal code to pass**
- [ ] **Step 4: Run test to verify pass**
- [ ] **Step 5: Commit**
`git commit -m "feat(user): add validated user domain model"`

---

## Plan Self-Review Checklist
- [ ] **Spec coverage**: Every requirement maps to an explicit task
- [ ] **Step scan**: Each step does exactly one action with a checkable result
- [ ] **Type consistency**: Method signatures and types match across tasks
- [ ] **Proportion**: Plan contains signatures and tests, not full copy-pasted implementations
- [ ] **Preservation**: Never overwrite an existing incomplete plan without asking
```
