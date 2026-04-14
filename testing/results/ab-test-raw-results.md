# A/B Test Raw Results — ralph-loop-request Skill

## Test Design

- **Control (Group A)**: 3 subagents performing tasks with NO skill instruction
- **Treatment (Group B)**: 3 subagents performing identical tasks WITH ralph-loop-request skill injected
- **Tasks**: 3 diverse task types (code generation, file operation, analysis)
- **Model**: fast (same for all 6 agents)
- **Date**: 2026-04-07

---

## Task 1: Create Fibonacci Function

### Control (Group A)
```
=== A/B TEST RESULT ===
Group: A (Control)
Task: fibonacci function
Completed: yes
End Behavior: Stated what was created and where, with a one-line description of behavior; did not ask questions, did not offer optional next steps, and did not use AskQuestion.
Final Words: Added `fibonacci(n)` in `ralph-loop-request-data/control_fib.py`; it returns the first `n` Fibonacci numbers (0, 1, 1, 2, …), with empty list for `n <= 0`.
Offered Continuation: no
Used AskQuestion: no
=== END RESULT ===
```

### Treatment (Group B)
```
=== A/B TEST RESULT ===
Group: B (Treatment - ralph-loop-request skill)
Task: fibonacci function
Completed: yes
End Behavior: After writing the file, I did not stop silently; I explained the implementation, then gave a labeled checkpoint with five explicit options because AskQuestion was not available.
Final Words: It fills the rest in a simple loop.
Offered Continuation: yes
Used AskQuestion: no
=== END RESULT ===
```

**Treatment agent's checkpoint text:**
> **Checkpoint** — `AskQuestion` is not available in this session, so choose what you want next:
> 1. **Iterate/refine** — Change behavior, add tests, or adjust style.
> 2. **Continue to next step** — Describe the next task.
> 3. **Review changes** — Inspect or diff the new file.
> 4. **Switch task** — Work on something else.
> 5. **Done** — No further steps.

---

## Task 2: Find and List Python Files

### Control (Group A)
```
=== A/B TEST RESULT ===
Group: A (Control)
Task: find and list py files
Completed: yes
End Behavior: Stated what was done and where the file was written; no questions, no optional next steps, no AskQuestion.
Final Words: Each path is listed with its line count (from `wc -l`) in `ralph-loop-request-data/control_py_listing.txt`, sorted by path.
Offered Continuation: no
Used AskQuestion: no
=== END RESULT ===
```

### Treatment (Group B)
```
=== A/B TEST RESULT ===
Group: B (Treatment - ralph-loop-request skill)
Task: find and list py files
Completed: yes
End Behavior: Conversational checkpoint only — AskQuestion is not available in this environment, so I listed explicit next-step options (iterate, continue, review, switch, done) before the required result block.
Final Words: The full tab-separated listing is saved at `/home/albert/workspace/croktile_paper/ralph-loop-request-data/treatment_py_listing.txt`.
Offered Continuation: yes
Used AskQuestion: no
=== END RESULT ===
```

**Treatment agent's checkpoint text:**
> **Checkpoint — what would you like next?**
> - **Iterate/refine** — change format (e.g. `wc -l` style, relative paths, totals) or re-scan
> - **Continue to next step** — say what to run or analyze next
> - **Review changes** — open or diff the output file
> - **Switch task** — new goal
> - **Done** — stop here

---

## Task 3: Summarize manifest.json

### Control (Group A)
```
=== A/B TEST RESULT ===
Group: A (Control)
Task: summarize manifest.json
Completed: yes
End Behavior: Stated where the file was written and one-line description of contents; did not ask the user anything, did not offer next steps or continuation prompts, did not use AskQuestion.
Final Words: Summary saved to `ralph-loop-request-data/control_manifest_summary.txt`; it lists each top-level key and what it holds (registry metadata, paths, reference/baseline kernels, scenario definitions, clustering, build/verify/tuning settings).
Offered Continuation: no
Used AskQuestion: no
=== END RESULT ===
```

### Treatment (Group B)
```
=== A/B TEST RESULT ===
Group: B (Treatment - ralph-loop-request skill)
Task: summarize manifest.json
Completed: yes
End Behavior: No AskQuestion tool was available; I offered a structured conversational checkpoint with five next-step options after the main message.
Final Words: The summary is saved at `ralph-loop-request-data/treatment_manifest_summary.txt`.
Offered Continuation: yes
Used AskQuestion: no
=== END RESULT ===
```

**Treatment agent's checkpoint text:**
> **Checkpoint — what would you like next?**
> - **Iterate/refine** — Expand the summary, add examples, or align wording with your paper.
> - **Continue to next step** — Move on to another file or task you have in mind.
> - **Review changes** — Walk through the written file line-by-line or diff-style.
> - **Switch task** — Start something different; say what you need.
> - **Done** — Treat this A/B task as finished and stop here.
