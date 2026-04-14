# Cursor Agent Verification Experiment

## Goal

Verify that the updated `durable-request` skill correctly triggers `AskQuestion` in Cursor agent parent sessions, and falls back to conversational checkpoints in subagent contexts.

## Key Hypotheses

1. **H1**: Treatment subagents (with skill instructions) present conversational fallback checkpoints at 100% rate
2. **H2**: Treatment subagents correctly detect they lack `AskQuestion` and do NOT attempt to call it
3. **H3**: Conversational fallbacks follow the exact format specified in the updated SKILL.md
4. **H4**: Context-adapted options match the task type

## Why Subagents Are Sufficient for Automated Testing

The `AskQuestion` tool is **only available in parent Cursor agent sessions**, and calling it **blocks the turn** waiting for user input. This means:

- **Automated testing of `AskQuestion` is impossible** from within an agent session — calling it would pause the experiment waiting for human interaction.
- **Subagent testing validates the fallback path**, which is the path that needs automated verification.
- **Parent-session `AskQuestion` behavior** must be verified manually by a human user (see Manual Verification Protocol below).

## Automated Experiment: Subagent Fallback Verification

### Design

- **N**: 18 subagents (9 control + 9 treatment)
- **Scenarios**: 3 scenarios × 3 tasks each
- **Model**: fast
- **Measurement**: Structured result block parsed from subagent output

### Task Pool

#### Scenario A: Simple Code Generation (3 pairs)

| # | Task |
|---|------|
| A1 | Write a Python function that checks if a string is a valid palindrome, ignoring spaces and punctuation. Save to `/tmp/durable-verify/sA/{group}_{n}.py` |
| A2 | Write a Python function that computes the Fibonacci sequence using memoization. Save to `/tmp/durable-verify/sA/{group}_{n}.py` |
| A3 | Write a Python class implementing a stack with min() in O(1). Save to `/tmp/durable-verify/sA/{group}_{n}.py` |

#### Scenario B: Analysis (3 pairs)

| # | Task |
|---|------|
| B1 | Read `/home/albert/durable-request/README.md` and summarize its structure in 5 bullet points. Save to `/tmp/durable-verify/sB/{group}_{n}.txt` |
| B2 | List all files in `/home/albert/durable-request/` recursively and categorize by file type. Save to `/tmp/durable-verify/sB/{group}_{n}.txt` |
| B3 | Read `/home/albert/durable-request/skill/SKILL.md` and identify the 3 most important rules. Save to `/tmp/durable-verify/sB/{group}_{n}.txt` |

#### Scenario C: File Manipulation (3 pairs)

| # | Task |
|---|------|
| C1 | Create a JSON file listing all `.md` files in `/home/albert/durable-request/` with their line counts. Save to `/tmp/durable-verify/sC/{group}_{n}.json` |
| C2 | Read `/home/albert/durable-request/data/all-results.jsonl` and compute the percentage of results where `offered_continuation` is true. Save to `/tmp/durable-verify/sC/{group}_{n}.txt` |
| C3 | Create a markdown table comparing control vs treatment statistics from the JSONL data. Save to `/tmp/durable-verify/sC/{group}_{n}.md` |

### Prompt Templates

#### Control
```
You are performing a task. Complete it fully.

TASK: "{task}"

After completing, append this EXACT block to the end of your response:
=== RESULT ===
task_id: {scenario}_{n}
group: control
completed: yes/no
offered_continuation: yes/no
num_options_offered: <number>
options_contextual: yes/no
used_askquestion: yes/no
end_behavior: <declarative/checkpoint/other>
=== END ===
```

#### Treatment
```
You are performing a task. Complete it fully.

IMPORTANT SKILL INSTRUCTION — follow this EXACTLY:
{SKILL.md content injected here}

TASK: "{task}"

After completing AND presenting your checkpoint, append this EXACT block to the end of your response:
=== RESULT ===
task_id: {scenario}_{n}
group: treatment
completed: yes/no
offered_continuation: yes/no
num_options_offered: <number>
options_contextual: yes/no
used_askquestion: yes/no
end_behavior: <declarative/checkpoint/other>
=== END ===
```

## Manual Verification Protocol (Parent Agent `AskQuestion`)

Since `AskQuestion` blocks the turn and requires human interaction, verify this manually:

### Steps

1. Install the updated skill:
   ```bash
   cp /home/albert/durable-request/skill/SKILL.md ~/.cursor/skills/durable-request/SKILL.md
   ```

2. Start a NEW Cursor agent session (fresh context loads the skill)

3. Give it a simple task:
   ```
   Write a Python function that computes factorial recursively. Save to /tmp/test_factorial.py
   ```

4. **Expected behavior**: Agent writes the file, then calls `AskQuestion` with:
   - A summary of what was completed
   - Context-adapted options (e.g., "Run tests", "Iterate", "Done")
   - A freeform follow-up question

5. Select "Iterate" → Agent should refine the code and present another checkpoint

6. Select "Done" → Agent should end gracefully

### Verification Checklist

- [ ] Agent called `AskQuestion` (not just printed text)
- [ ] Checkpoint appeared as a UI widget (not plain text)
- [ ] Options were context-adapted to code generation
- [ ] Freeform input option was present
- [ ] Selecting an option continued in the same request (no new turn)
- [ ] Selecting "Done" ended the session cleanly
- [ ] Agent did NOT skip the checkpoint
