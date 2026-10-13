# Skill Master — Project Catalog & Tracking Ledger

This document is the official tracking registry and catalog ledger for the **Skill Master** repository. It records the metrics, active skill directory, consolidation history, and release changelog for all agent skills.

---

## 📊 Repository Metrics

| Metric | Current Count | Target | Status |
|:-------|:--------------|:-------|:-------|
| **Total Active Skills** | **66** (Zero Duplicates / Unified Themes) | 50+ | 🟢 Optimized |
| **Meta & Ecosystem Tools** | 2 (`skill-creator`, `antigravity-skills-manager`) | 2 | 🟢 Complete |
| **Conductor CDD Lifecycle** | 7 (`conductor-setup`, `new-track`, `implement`, etc.) | 7 | 🟢 Streamlined |
| **Ideation & Discovery** | 2 (`interview-me`, `brainstorming-ideas`) | 2 | 🟢 Complete |
| **Planning & Methodology** | 7 (`spec-driven`, `writing-plans`, `constraints`, etc.) | 7 | 🟢 Complete |
| **Architecture & Full-Stack** | 3 (`architect-review`, `full-stack`, `api-engineering`) | 3 | 🟢 Complete |
| **Backend & Infrastructure** | 4 (`database`, `security`, `observability`, `perf`) | 4 | 🟢 Complete |
| **Testing & Verification** | 4 (`tdd`, `unit-testing`, `webapp-testing`, `verify-gate`) | 4 | 🟢 Complete |
| **Frontend & Visual Design** | 6 (`frontend-design`, `ui-engineering`, `accessible`, etc.)| 6 | 🟢 Complete |
| **Vercel & React Ecosystem** | 5 (`deploy-to-vercel`, `optimize`, `best-practices`, etc.) | 5 | 🟢 Complete |
| **Mobile (React Native)** | 1 (`vercel-react-native-skills`) | 1 | 🟢 Complete |
| **Data Viz & Creative** | 6 (`dataviz-recharts`, `algorithmic-art`, `canvas`, etc.) | 6 | 🟢 Complete |
| **Quality & Code Review** | 4 (`code-review-excellence`, `simplification`, `brand`, etc.)| 4 | 🟢 Complete |
| **Git & DevOps** | 3 (`git-pr-workflow`, `git-advanced`, `ci-cd`) | 3 | 🟢 Complete |
| **Reliability & Lifecycle** | 3 (`troubleshooting`, `shipping-and-launch`, `migration`) | 3 | 🟢 Complete |
| **Docs & Communication** | 5 (`documentation-engineering`, `writing`, `internal`, etc.)| 5 | 🟢 Complete |
| **Document Formats (Office/PDF)** | 4 (`docx`, `pdf`, `pptx`, `xlsx`) | 4 | 🟢 Complete |
| **On-Demand Catalog Skills** | 307 skills (via `skills-cli.js`) | 300+ | 🟢 Integrated |

---

## 🗂️ Active Skills Catalog (66 Non-Redundant Skills)

| Skill Folder | YAML Identifier | Domain | Status | Description & Value |
|:-------------|:----------------|:-------|:-------|:--------------------|
| [`accessible-forms-dialogs`](file:///.agent/skills/accessible-forms-dialogs/) | `accessible-forms-dialogs` | Frontend | 🟢 Active | WAI-ARIA forms, modal dialogs, focus trapping, and keyboard navigation. |
| [`algorithmic-art`](file:///.agent/skills/algorithmic-art/) | `algorithmic-art` | Creative | 🟢 Active | Generative art in p5.js with seeded randomness and interactive exploration. |
| [`antigravity-skills-manager`](file:///.agent/skills/antigravity-skills-manager/) | `antigravity-skills-manager` | Meta | 🟢 Active (Upgraded) | Central CLI & governance hub; absorbed `using-agent-skills` lifecycle tree. |
| [`api-engineering`](file:///.agent/skills/api-engineering/) | `api-engineering` | Architecture | 🟢 Active (Merged) | Merged `api-and-interface-design` + `api-engineering` (RFC 7807, CORS, dynamic URLs). |
| [`architect-review`](file:///.agent/skills/architect-review/) | `architect-review` | Architecture | 🟢 Active | Master architect reviewing system designs, DDD, and microservice boundaries. |
| [`brainstorming-ideas`](file:///.agent/skills/brainstorming-ideas/) | `brainstorming-ideas` | Ideation | 🟢 Active (Upgraded) | Absorbed `idea-refine` (3-phase divergent/convergent, 7 lenses, Not Doing list). |
| [`brand-identity`](file:///.agent/skills/brand-identity/) | `brand-identity` | Standards | 🟢 Active | Enforces design tokens, framework conventions, and voice/tone standards. |
| [`brandkit`](file:///.agent/skills/brandkit/) | `brandkit` | Creative | 🟢 Active | Agency-grade brand identity boards, logo systems, and visual decks. |
| [`canvas-design`](file:///.agent/skills/canvas-design/) | `canvas-design` | Creative | 🟢 Active | Programmatic visual design for PNG/PDF assets with bundled typography. |
| [`ci-cd-and-automation`](file:///.agent/skills/ci-cd-and-automation/) | `ci-cd-and-automation` | DevOps | 🟢 Active | Automated build pipelines, test runners, and CI quality gates. |
| [`clean-code-frontend-audit`](file:///.agent/skills/clean-code-frontend-audit/) | `clean-code-frontend-audit` | Quality & Audit | 🟢 Active (Upgraded) | Zero-Hardcoding Master Matrix: eliminates mocks, magic numbers, static URLs & fake data. |
| [`code-review-excellence`](file:///.agent/skills/code-review-excellence/) | `code-review-excellence` | Code Review | 🟢 Active (Upgraded) | Absorbed `code-review-and-quality` (5-axis review, structural remedies, sizing). |
| [`code-simplification`](file:///.agent/skills/code-simplification/) | `code-simplification` | Quality | 🟢 Active | Refactors complex code for readability while preserving exact behavior. |
| [`conductor-implement`](file:///.agent/skills/conductor-implement/) | `conductor-implement` | Conductor | 🟢 Active | Executes tasks from tracks adhering to TDD checkpoints and test-first verification. |
| [`conductor-manage`](file:///.agent/skills/conductor-manage/) | `conductor-manage` | Conductor | 🟢 Active | Manages track lifecycle: archive completed tracks, restore, rename, cleanup. |
| [`conductor-new-track`](file:///.agent/skills/conductor-new-track/) | `conductor-new-track` | Conductor | 🟢 Active | Scaffolds new feature tracks with specifications, phases, and TDD task lists. |
| [`conductor-revert`](file:///.agent/skills/conductor-revert/) | `conductor-revert` | Conductor | 🟢 Active | Git-aware rollback by logical work unit (track, phase, or task). |
| [`conductor-setup`](file:///.agent/skills/conductor-setup/) | `conductor-setup` | Conductor | 🟢 Active | Living project context setup: `product.md`, `tech-stack.md`, `workflow.md`. |
| [`conductor-status`](file:///.agent/skills/conductor-status/) | `conductor-status` | Conductor | 🟢 Active | Displays project status, active tracks, phase progress, and next actions. |
| [`conductor-validator`](file:///.agent/skills/conductor-validator/) | `conductor-validator` | Conductor | 🟢 Active | Validates Conductor project artifacts for completeness, consistency, and syntax. |
| [`constraint-driven-development`](file:///.agent/skills/constraint-driven-development/) | `constraint-driven-development` | Methodology | 🟢 Active | Formalizes quality bar contracts in `CONSTRAINTS.md` to stop test silencing. |
| [`context-engineering`](file:///.agent/skills/context-engineering/) | `context-engineering` | Methodology | 🟢 Active | Curates LLM context hierarchically to prevent hallucination and session drift. |
| [`database-engineering`](file:///.agent/skills/database-engineering/) | `database-engineering` | Backend | 🟢 Active | Schema migrations, async connection pooling, and RLS for PostgreSQL/SQLite. |
| [`dataviz-recharts-analytics`](file:///.agent/skills/dataviz-recharts-analytics/) | `dataviz-recharts-analytics` | Creative | 🟢 Active | Production Recharts patterns, SVG styling, and responsive containers. |
| [`deploy-to-vercel`](file:///.agent/skills/deploy-to-vercel/) | `deploy-to-vercel` | Vercel | 🟢 Active (Merged) | Merged `deploy-to-vercel` + `vercel-cli-with-tokens` (Git & token-based deploys). |
| [`deprecation-and-migration`](file:///.agent/skills/deprecation-and-migration/) | `deprecation-and-migration` | Lifecycle | 🟢 Active | Safe zero-downtime deprecation workflows and expand/contract patterns. |
| [`discernment-nudge`](file:///.agent/skills/discernment-nudge/) | `discernment-nudge` | Communication | 🟢 Active | Appends probing questions to substantive advice to stress-test assumptions. |
| [`documentation-engineering`](file:///.agent/skills/documentation-engineering/) | `documentation-engineering` | Docs | 🟢 Active (Merged) | Merged `doc-coauthoring` + `documentation-and-adrs` (3-stage authoring + ADRs). |
| [`docx`](file:///.agent/skills/docx/) | `docx` | Documents | 🟢 Active | Programmatic creation, parsing, and templating of Word `.docx` documents. |
| [`doubt-driven-development`](file:///.agent/skills/doubt-driven-development/) | `doubt-driven-development` | Methodology | 🟢 Active | Adversarial fresh-context review of high-stakes architectural decisions. |
| [`frontend-design`](file:///.agent/skills/frontend-design/) | `frontend-design` | Frontend | 🟢 Active (Merged) | Merged `frontend-design` + `design-taste` + `high-end` (Anti-slop, Bento, Physics). |
| [`frontend-ui-engineering`](file:///.agent/skills/frontend-ui-engineering/) | `frontend-ui-engineering` | Frontend | 🟢 Active | Builds production-quality, accessible, responsive UI components. |
| [`full-stack-orchestration`](file:///.agent/skills/full-stack-orchestration/) | `full-stack-orchestration` | Architecture | 🟢 Active | Coordinates multi-tier feature implementation (DB, API, Frontend, Tests). |
| [`git-advanced-workflows`](file:///.agent/skills/git-advanced-workflows/) | `git-advanced-workflows` | Git | 🟢 Active | Complex Git operations: interactive rebase, worktrees, bisect, reflog. |
| [`git-pr-workflows-git-workflow`](file:///.agent/skills/git-pr-workflows-git-workflow/) | `git-pr-workflows-git-workflow` | Git | 🟢 Active (Upgraded) | Absorbed `git-workflow-and-versioning` (Trunk-based, Semver, Changelogs). |
| [`incremental-implementation`](file:///.agent/skills/incremental-implementation/) | `incremental-implementation` | Methodology | 🟢 Active | Delivers features in thin, verifiable slices behind feature flags. |
| [`internal-comms`](file:///.agent/skills/internal-comms/) | `internal-comms` | Communication | 🟢 Active | Corporate communications: executive 3P updates, newsletters, incident reports. |
| [`interview-me`](file:///.agent/skills/interview-me/) | `interview-me` | Ideation | 🟢 Active | One-at-a-time diagnostic interview extracting underlying intent before coding. |
| [`mcp-builder`](file:///.agent/skills/mcp-builder/) | `mcp-builder` | Tooling | 🟢 Active | Builds high-quality Model Context Protocol (MCP) servers in Python/TypeScript. |
| [`minimalist-ui`](file:///.agent/skills/minimalist-ui/) | `minimalist-ui` | Frontend | 🟢 Active | Clean editorial interfaces with warm monochrome palettes and flat bento grids. |
| [`observability-and-instrumentation`](file:///.agent/skills/observability-and-instrumentation/) | `observability-and-instrumentation` | Backend | 🟢 Active | Structured logging, metrics, distributed tracing, and health monitoring. |
| [`pdf`](file:///.agent/skills/pdf/) | `pdf` | Documents | 🟢 Active | Programmatic PDF parsing, table extraction, OCR, form-filling, and merging. |
| [`performance-optimization`](file:///.agent/skills/performance-optimization/) | `performance-optimization` | Backend | 🟢 Active | Profiles and eliminates bottlenecks across frontend, backend, and DB queries. |
| [`pptx`](file:///.agent/skills/pptx/) | `pptx` | Documents | 🟢 Active | Creation, parsing, slide layout manipulation, and editing for PowerPoint. |
| [`redesign-existing-projects`](file:///.agent/skills/redesign-existing-projects/) | `redesign-existing-projects` | Frontend | 🟢 Active | Audits and upgrades legacy web interfaces to premium agency quality. |
| [`security-and-hardening`](file:///.agent/skills/security-and-hardening/) | `security-and-hardening` | Backend | 🟢 Active | Hardens applications against OWASP Top 10, supply chain risks, and leaks. |
| [`shipping-and-launch`](file:///.agent/skills/shipping-and-launch/) | `shipping-and-launch` | Lifecycle | 🟢 Active | Production release checklists, staged rollouts, and automated rollback plans. |
| [`skill-creator`](file:///.agent/skills/skill-creator/) | `creating-skills` | Meta | 🟢 Active | Scaffolds compliant Antigravity skills following `<500` lines standard. |
| [`slack-gif-creator`](file:///.agent/skills/slack-gif-creator/) | `slack-gif-creator` | Creative | 🟢 Active | Generates and optimizes animated GIFs for Slack dimension/size limits. |
| [`source-driven-development`](file:///.agent/skills/source-driven-development/) | `source-driven-development` | Methodology | 🟢 Active | Grounds every implementation in official documentation citations. |
| [`spec-driven-development`](file:///.agent/skills/spec-driven-development/) | `spec-driven-development` | Methodology | 🟢 Active | Authors PRDs and capability maps before any code implementation begins. |
| [`test-driven-development`](file:///.agent/skills/test-driven-development/) | `test-driven-development` | Testing | 🟢 Active | Strict Red-Green-Refactor iron law, Chicago/London testing, coverage gates. |
| [`theme-factory`](file:///.agent/skills/theme-factory/) | `theme-factory` | Creative | 🟢 Active | 10 pre-packaged themes and dynamic palette/typography generators. |
| [`troubleshooting-applications`](file:///.agent/skills/troubleshooting-applications/) | `troubleshooting-applications` | Reliability | 🟢 Active (Upgraded) | Absorbed `debugging-and-error-recovery` (Stop-the-line, triage trees, bisect). |
| [`unit-testing-test-generate`](file:///.agent/skills/unit-testing-test-generate/) | `unit-testing-test-generate` | Testing | 🟢 Active | Generates comprehensive unit tests across languages with boundary focus. |
| [`vercel-composition-patterns`](file:///.agent/skills/vercel-composition-patterns/) | `vercel-composition-patterns` | Vercel | 🟢 Active | Compound components and render props eliminating prop drilling in React 19. |
| [`vercel-optimize`](file:///.agent/skills/vercel-optimize/) | `vercel-optimize` | Vercel | 🟢 Active | Cost and performance optimization on Vercel deployments. |
| [`vercel-react-best-practices`](file:///.agent/skills/vercel-react-best-practices/) | `vercel-react-best-practices` | Vercel | 🟢 Active | Vercel Engineering guidelines for rendering, caching, and server components. |
| [`vercel-react-native-skills`](file:///.agent/skills/vercel-react-native-skills/) | `vercel-react-native-skills` | Mobile | 🟢 Active | Performance, list virtualization, and native modules for React Native / Expo. |
| [`vercel-react-view-transitions`](file:///.agent/skills/vercel-react-view-transitions/) | `vercel-react-view-transitions` | Vercel | 🟢 Active | Native View Transition API animations in React and Next.js App Router. |
| [`verifying-before-completion`](file:///.agent/skills/verifying-before-completion/) | `verifying-before-completion` | Verification | 🟢 Active | Anti-hallucination gate forbidding victory claims without fresh terminal runs. |
| [`web-design-guidelines`](file:///.agent/skills/web-design-guidelines/) | `web-design-guidelines` | Standards | 🟢 Active | Audits UI code against Web Interface Guidelines and UX standards. |
| [`webapp-testing`](file:///.agent/skills/webapp-testing/) | `webapp-testing` | Testing | 🟢 Active (Merged) | Merged `browser-testing-with-devtools` + `webapp-testing` (Playwright + MCP). |
| [`writing-guidelines`](file:///.agent/skills/writing-guidelines/) | `writing-guidelines` | Docs | 🟢 Active | Audits documentation and copy for clarity, structure, and voice/tone. |
| [`writing-plans`](file:///.agent/skills/writing-plans/) | `writing-plans` | Planning | 🟢 Active (Upgraded) | Absorbed `planning-and-task-breakdown` (Vertical slicing, dependency graphs). |
| [`xlsx`](file:///.agent/skills/xlsx/) | `xlsx` | Documents | 🟢 Active | Programmatic spreadsheet parsing, formulas, charting, and data cleaning. |

---

## 🚀 Consolidation & Evolution Ledger

| Consolidated Action | Source Skills | Evolved Master Skill | Rationale & Value |
|:-------------------|:--------------|:---------------------|:-------------------|
| **Code Review Upgrade** | `code-review-and-quality` (Sohoj) | [`code-review-excellence`](file:///.agent/skills/code-review-excellence/) | Absorbed 5-axis review, structural remedies, sizing rules, and review checklists. |
| **Troubleshooting Upgrade** | `debugging-and-error-recovery` (Sohoj) | [`troubleshooting-applications`](file:///.agent/skills/troubleshooting-applications/) | Absorbed Stop-the-Line rule, triage decision trees, and git bisect workflows. |
| **Git Workflow Upgrade** | `git-workflow-and-versioning` (Sohoj) | [`git-pr-workflows-git-workflow`](file:///.agent/skills/git-pr-workflows-git-workflow/) | Absorbed trunk-based dev, save point pattern, change summaries, and semver changelogs. |
| **Planning Upgrade** | `planning-and-task-breakdown` (Sohoj) | [`writing-plans`](file:///.agent/skills/writing-plans/) | Absorbed vertical slicing, dependency graphs, task sizing limits, and checkpoints. |
| **Brainstorming Upgrade** | `idea-refine` (Sohoj) | [`brainstorming-ideas`](file:///.agent/skills/brainstorming-ideas/) | Absorbed 3-phase divergent/convergent ideation, 7 lenses, and Not Doing lists. |
| **Skills Manager Upgrade** | `using-agent-skills` (Sohoj) | [`antigravity-skills-manager`](file:///.agent/skills/antigravity-skills-manager/) | Absorbed skill discovery tree, core operating behaviors, and lifecycle sequence. |
| **API Engineering Merge** | `api-and-interface-design` + `api-engineering` | [`api-engineering`](file:///.agent/skills/api-engineering/) | Unified contract-first interface design with RFC 7807 and dynamic base URL resolution. |
| **Frontend Design Merge** | `frontend-design` + `design-taste` + `high-end` | [`frontend-design`](file:///.agent/skills/frontend-design/) | Unified anti-slop aesthetic direction, Bento layouts, and fluid motion physics. |
| **Vercel Deploy Merge** | `deploy-to-vercel` + `vercel-cli-with-tokens` | [`deploy-to-vercel`](file:///.agent/skills/deploy-to-vercel/) | Unified Git preview deploys with headless token-based CI workflows. |
| **Documentation Merge** | `doc-coauthoring` + `documentation-and-adrs` | [`documentation-engineering`](file:///.agent/skills/documentation-engineering/) | Unified 3-stage collaborative drafting with Architecture Decision Records (ADRs). |
| **Webapp Testing Merge** | `browser-testing-with-devtools` + `webapp-testing`| [`webapp-testing`](file:///.agent/skills/webapp-testing/) | Unified Playwright test automation with Chrome DevTools MCP runtime inspection. |

---

## 📝 Release Changelog

### 2026-10-13 — Sohoj Skills Migration & Master Unification Release
- **Expanded catalog from 21 to 66 non-overlapping, high-impact skills.**
- **6 Existing Skills Positively Upgraded**:
  - `code-review-excellence`: 5-axis review, structural remedies, and review checklists.
  - `troubleshooting-applications`: Stop-the-Line rule, triage decision trees, and git bisect.
  - `git-pr-workflows-git-workflow`: Trunk-based development, save points, change summaries, and semver changelogs.
  - `writing-plans`: Vertical slicing, dependency graph mapping, and task size limits.
  - `brainstorming-ideas`: 3-phase divergent/convergent thinking, 7 ideation lenses, and frameworks.
  - `antigravity-skills-manager`: Meta-skill discovery tree, non-negotiable operating behaviors, and full lifecycle sequencing.
- **5 Merged Skills Created**:
  - `api-engineering`: Contract-first design + RFC 7807 + dynamic base URLs.
  - `frontend-design`: Studio-tier anti-slop design + Bento layouts + fluid spring physics.
  - `deploy-to-vercel`: Git push preview deploys + token-based headless CLI.
  - `documentation-engineering`: 3-stage collaborative doc authoring + ADR templates.
  - `webapp-testing`: Automated Playwright test runner + Chrome DevTools MCP inspection.
- **40 Unique Skills Added Across 10 Domains**:
  - *Methodology*: `constraint-driven-development`, `doubt-driven-development`, `source-driven-development`, `spec-driven-development`, `incremental-implementation`, `context-engineering`.
  - *Backend*: `database-engineering`, `security-and-hardening`, `observability-and-instrumentation`, `performance-optimization`.
  - *Frontend*: `frontend-ui-engineering`, `accessible-forms-dialogs`, `minimalist-ui`, `redesign-existing-projects`, `web-design-guidelines`, `clean-code-frontend-audit`.
  - *Vercel & React*: `vercel-optimize`, `vercel-react-best-practices`, `vercel-composition-patterns`, `vercel-react-view-transitions`.
  - *Mobile*: `vercel-react-native-skills`.
  - *Data Viz & Creative*: `dataviz-recharts-analytics`, `algorithmic-art`, `canvas-design`, `brandkit`, `theme-factory`, `slack-gif-creator`.
  - *Documents*: `docx`, `pdf`, `pptx`, `xlsx`.
  - *Communication*: `internal-comms`, `writing-guidelines`, `discernment-nudge`, `interview-me`.
  - *Lifecycle & Tooling*: `shipping-and-launch`, `deprecation-and-migration`, `code-simplification`, `mcp-builder`.
- **7 Skills Filtered/Skipped**: Excluded project-specific (`ui-ux-design-system` Upay tokens, `fintech-mfs-patterns`), platform-specific (`claude-api`, `academy-guide`, `brand-guidelines`, `web-artifacts-builder`), and boilerplate templates (`template-skill`).
- Validated 66/66 skills pass YAML frontmatter and structural integrity checks.

### 2026-10-13 — Global Antigravity Live Integration & Token Optimization
- **Live NTFS Directory Junction Activated**: Converted `C:\Users\<user>\.gemini\config\skills` into an NTFS Directory Junction linked directly to `D:\Code\Skill_Master\.agent\skills`. Changes made in `Skill_Master` are now **instantaneously live across all projects** on the machine with zero delay or manual sync required.
- **Progressive Disclosure Token Safety**: Confirmed that global exposure costs only ~3,000 system-prompt tokens (~0.3% of 1M context) for metadata indexing, while full skill manuals load strictly on-demand when invoked.
- **Project Scoping & Filtering**: Documented local project override and scoping protocols (`include_only` / `exclude` in project configs) for projects requiring tight domain isolation.
- **Global Path Registration**: Configured `~/.gemini/config/skills.json` pointing directly to `D:/Code/Skill_Master/.agent/skills`.
- **Directory Junction**: Established NTFS junction `~/.gemini/antigravity/skills` $\rightarrow$ `~/.gemini/config/skills` for complete backward and forward compatibility.
- **Sync Fallback**: Maintained `node skills-cli.js sync-global` as an offline snapshot synchronization utility.

### 2026-10-13 — Universal Zero-Hardcoding Evolution
- **Positively Upgraded [`clean-code-frontend-audit`](file:///.agent/skills/clean-code-frontend-audit/)**: Transformed it into the master **Zero-Hardcoding & Clean Code Audit** playbook.
- Added comprehensive coverage for all 6 hardcoding archetypes: Mock Data / Placeholders, Magic Numbers, Hardcoded URLs/Ports, Hardcoded Secrets, Inline CSS Dimensions, and Static Dates.
- Added automated regex/ripgrep detection commands, typed binding refactoring rules, and a pre-submission de-hardcoding checklist.



