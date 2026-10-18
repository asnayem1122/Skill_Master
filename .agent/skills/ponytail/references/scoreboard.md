# Ponytail Benchmark & Impact Scoreboard

These figures represent the published agentic benchmark results from Ponytail 5: headless Claude Code (Opus 5.5, default effort) evaluated across 39 real-world tasks (feature tickets in a FastAPI + React repository, bug fixes, security and privacy scenarios, and micro-applications), 5 runs each, measured against the same agent operating without the skill.

---

## 📊 Benchmark Scoreboard

```text
  Ponytail Gain Benchmark · 39 tasks × 5 runs · Opus 5.5

  Baseline (No Skill)      ████████████████████  100%
  Lines of Code            █████████···········   47%   ▼ 53%
  Output Tokens            ███████████·········   55%   ▼ 45%
  Total Cost               ███████████████·····   74%   ▼ 26%
  Task Completion Time     ████████████········   59%   ▼ 41%
  Hidden Checks Passed     97%  (Baseline: 96%)
  Tests on Risky Logic     98%  (Baseline: 68%)
  Bugs Caught by Self-Test 66%  (Baseline: 46%)
```

---

## 🛡️ The Honesty Boundary

1. **Benchmark Averages vs. Live Codebase:**
   These metrics represent measured geometric means across controlled test suites, not real-time calculations from your current workspace.
2. **No Fictional Savings:**
   Never invent or fabricate per-repository savings numbers (*"You saved 140 lines here"*), because the unbuilt, bloated alternative was never written.
3. **Real Metrics via Debt Ledger:**
   The only verified per-repository numbers come from the **Shortcut Debt Ledger** (`git grep -nE '(shortcut|ponytail):'`), which provides a factual, countable record of deferred technical decisions.
