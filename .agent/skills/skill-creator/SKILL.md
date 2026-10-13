---
name: creating-skills
description: >-
  Generates new Antigravity skills from user requirements. Activate when the
  user asks to "create a skill", "build a skill", "make a new agent skill",
  or mentions "skill creator". Produces a complete .agent/skills/ directory
  with SKILL.md, optional scripts, examples, and resources.
---

# Antigravity Skill Creator

## When to use this skill

- User asks to **create**, **build**, or **scaffold** a new skill
- User says "skill creator" or "generate a skill for …"
- User wants to automate a repeatable agent workflow

## Core Structural Requirements

Every generated skill **must** follow this folder hierarchy:

```
<skill-name>/
├── SKILL.md          # Required – main logic and instructions
├── scripts/          # Optional – helper scripts
├── examples/         # Optional – reference implementations
└── resources/        # Optional – templates or assets
```

## YAML Frontmatter Standards

The `SKILL.md` must begin with YAML frontmatter:

| Field         | Rules                                                                                      |
| :------------ | :----------------------------------------------------------------------------------------- |
| `name`        | Gerund form (e.g., `testing-code`). Max 64 chars. Lowercase, digits, hyphens only.         |
| `description` | Third-person voice. Include trigger keywords. Max 1024 chars.                               |

> [!IMPORTANT]
> Never include brand names like "claude" or "anthropic" in the skill name.

## Writing Principles

- **Conciseness** – Assume the agent is expert-level. Don't explain common concepts.
- **Progressive Disclosure** – Keep `SKILL.md` under 500 lines. Link to secondary
  files (one level deep) for extended detail: `[See ADVANCED.md](ADVANCED.md)`.
- **Forward Slashes** – Always use `/` for paths, never `\`.
- **Degrees of Freedom**:
  - **Bullet points** → high-freedom tasks (heuristics, guidelines)
  - **Code blocks** → medium-freedom (templates, patterns)
  - **Exact commands** → low-freedom (fragile operations that must be precise)

## Workflow

Use this checklist when generating a new skill:

- [ ] **Clarify** – Confirm the skill's purpose, triggers, and scope with the user
- [ ] **Name** – Choose a gerund-form name (`verbing-noun`)
- [ ] **Structure** – Decide which optional folders (`scripts/`, `examples/`, `resources/`) are needed
- [ ] **Draft SKILL.md** – Write frontmatter + body following the template below
- [ ] **Draft supporting files** – Scripts, examples, resources as needed
- [ ] **Validate** – Confirm frontmatter is valid YAML, paths use `/`, line count < 500
- [ ] **Deliver** – Write all files to `.agent/skills/<skill-name>/`

## SKILL.md Template

```markdown
---
name: <gerund-name>
description: <Third-person description with trigger keywords>
---

# <Skill Title>

## When to use this skill
- <Trigger 1>
- <Trigger 2>

## Workflow
<Checklist or step-by-step guide>

## Instructions
<Specific logic, code snippets, rules, or decision trees>

## Resources
- <Links to scripts/ or resources/ if applicable>
```

## Validation & Error Handling

- Run `--help` on any script before executing it if behavior is unclear
- For complex skills, include a **Plan → Validate → Execute** pattern:
  1. Generate a plan and show it to the user
  2. Run a validation check (e.g., lint, dry-run)
  3. Execute only after validation passes
- Include checklists the agent can copy and update to track state across turns

## Anti-patterns to Avoid

- Don't create monolithic `SKILL.md` files over 500 lines
- Don't hardcode absolute paths – use relative paths from the skill root
- Don't duplicate logic that belongs in a script – put it in `scripts/` instead
- Don't write instructions that assume a specific OS unless required
