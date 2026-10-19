# Andrej Karpathy's 4 Laws of LLM Coding

Derived from [Andrej Karpathy's observations](https://x.com/karpathy/status/2015883857489522876) on common LLM coding pitfalls. These four behavioral principles combat overcomplication, silent assumptions, drive-by refactoring, and unverified assumptions.

---

## 1. Think Before Coding
> *"The models make wrong assumptions on your behalf and just run along with them without checking. They don't manage their confusion, don't seek clarifications, don't surface inconsistencies, don't present tradeoffs, don't push back when they should."*

- **State assumptions explicitly**: If uncertain about user intent, ask rather than guess.
- **Present multiple interpretations**: Don't pick one silently when ambiguity exists. Show Option A vs Option B with tradeoffs.
- **Push back when warranted**: If a simpler approach exists, say so. Reject speculative over-engineering.
- **Stop when confused**: Name what's unclear and ask for clarification before editing code.

---

## 2. Simplicity First
> *"They really like to overcomplicate code and APIs, bloat abstractions... implement a bloated construction over 1000 lines when 100 would do."*

- **Minimum code that solves the problem**: Nothing speculative.
- **No single-use abstractions**: Never create interfaces, factory classes, or utility wrappers for code only used in one place.
- **No speculative flexibility**: Never add configuration flags, hooks, or plugin architectures that weren't requested.
- **No error handling for impossible scenarios**: Handle realistic failure modes, not absurd hypotheticals.
- **The Rewrite Test**: If you wrote 200 lines and it could be 50, rewrite it. Would a senior engineer say this is overcomplicated? If yes, simplify.

---

## 3. Surgical Changes
> *"They still sometimes change/remove comments and code they don't sufficiently understand as side effects, even if orthogonal to the task."*

- **Touch only what you must**: Clean up only your own mess.
- **No drive-by refactoring**: Don't "improve" adjacent code, comments, or formatting. Don't reformat files you didn't need to change.
- **Match existing codebase conventions**: Match the surrounding style, even if you would personally format it differently.
- **Orphan clean-up**: Remove imports, variables, and functions that YOUR changes made unused. Do not touch pre-existing dead code unless explicitly asked.
- **The Traceability Test**: Every changed line in the git diff must trace directly to the user's request.

---

## 4. Goal-Driven Execution
> *"LLMs are exceptionally good at looping until they meet specific goals... Don't tell it what to do, give it success criteria and watch it go."*

- **Transform imperative tasks into declarative goals**:
  - Instead of *"Add validation"*, define: *"Write tests for invalid inputs, then make them pass."*
  - Instead of *"Fix the bug"*, define: *"Write a test reproducing the bug, then make it pass."*
  - Instead of *"Refactor X"*, define: *"Ensure test suite passes before and after."*
- **State verifiable multi-step plans**:
  ```text
  1. [Step] → verify: [check command]
  2. [Step] → verify: [check command]
  3. [Step] → verify: [check command]
  ```
- **Loop until verified**: Strong success criteria enable independent validation. Weak criteria require endless back-and-forth.
