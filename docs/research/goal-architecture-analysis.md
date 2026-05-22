# /goal Architecture Analysis: Claude Code → Cursor Implementation

> **Purpose:** Rigorous analysis of Claude Code's `/goal` internals and the final
> design for an equivalent standalone skill in Cursor IDE.
>
> **Date:** 2026-05-22  
> **Status:** Design finalized after user review

---

## 1. Claude Code `/goal` — Complete Architecture

### 1.1 What `/goal` IS

`/goal` is a **session-scoped prompt-based Stop hook** — syntactic sugar over the
Stop hook system, not a built-in command.

```
/goal "all tests in test/auth pass"
  ↓
Installs a session-scoped Stop hook:
  type: "prompt"
  condition: "all tests in test/auth pass"
  evaluator: configured small fast model (default: Haiku)
  ↓
After each agent turn:
  1. (condition + conversation transcript) → evaluator model
  2. Evaluator returns: { yes/no, short reason }
  3. NO  → agent auto-continues, reason injected as guidance
  4. YES → goal clears, agent stops, control returns to user
```

### 1.2 The Evaluator Model

| Property | Detail |
|----------|--------|
| Model | Small fast model, defaults to Haiku |
| Input | Goal condition + conversation transcript |
| Output | yes/no boolean + short reason string |
| Capabilities | **Text-only.** Cannot run commands, read files, or call tools |
| Max condition | ~4000 characters |
| Cost | Negligible vs main-turn spend |

**Critical constraint:** The evaluator only judges transcript text. If Claude
never runs the tests, the evaluator never sees test output to confirm success.

### 1.3 Stop Hook I/O

**Input (stdin):**
```json
{
  "hook_event_name": "Stop",
  "stop_hook_active": false,
  "session_id": "..."
}
```

**Output to block (continue working):**
```json
{ "decision": "block", "reason": "Tests still failing. Continue fixing." }
```

**Output to allow (goal met):**
```json
{}
```

**`stop_hook_active`:** `true` when the current stop was triggered by a previous
hook block. Must check and exit 0 immediately when true to prevent infinite loops.

### 1.4 Lifecycle

| Command | Action |
|---------|--------|
| `/goal <condition>` | Install session-scoped Stop hook, start working |
| `/goal` | Show status: turns, tokens, elapsed time |
| `/goal clear` | Remove Stop hook, allow normal stop |

### 1.5 Key Architecture Properties

1. **Separation of concerns:** The working model does NOT evaluate its own
   completion. A separate, cheaper model evaluates from outside.
2. **Cross-turn persistence:** The goal survives across turns via the Stop hook.
3. **Reason as guidance:** The evaluator's "NO" reason becomes steering for the
   next turn — the agent knows WHY it hasn't finished yet.

---

## 2. Cursor Stop Hook — Specification

### 2.1 Input

```typescript
type StopHookInput = {
  conversation_id: string;
  generation_id: string;
  model: string;
  status: 'completed' | 'aborted' | 'error';
  loop_count: number;
  transcript_path?: string;
  workspace_roots?: string[];
  input_tokens?: number;
  output_tokens?: number;
};
```

**`followup_message` only consumed when `status === "completed"`.**

### 2.2 Output

```typescript
type StopHookOutput = {
  followup_message?: string;
};
```

### 2.3 Compatibility

Cursor accepts Claude Code formats:
```json
{ "hookSpecificOutput": { "decision": "block", "reason": "..." } }  // nested
{ "decision": "block", "reason": "..." }                             // flat
{ "followup_message": "..." }                                        // native
```

### 2.4 Loop Control

| | Claude Code | Cursor |
|-|-------------|--------|
| Guard | `stop_hook_active` boolean | `loop_count` integer |
| Cap | None built-in | `loop_limit` (default 5, `null` = unlimited) |

---

## 3. Core Difference and Solution

### 3.1 The Gap

Claude Code has **prompt-based hooks** (`type: "prompt"`) — one-line LLM
evaluator calls built into the hook system. Cursor does NOT have this.

### 3.2 The Solution: Cursor Subagent as Evaluator

**Key insight from user:** Cursor's `Task` tool (subagent) provides the same
capability as Haiku evaluation. A readonly subagent can read the transcript,
evaluate the goal condition, and return yes/no + reason.

```
Claude Code:                          Cursor equivalent:
─────────────────────                 ─────────────────────
condition + transcript                condition + transcript context
      ↓                                    ↓
Haiku (prompt-based hook)             Task subagent (readonly=true)
      ↓                                    ↓
{ ok: true/false, reason }            "YES: <reason>" or "NO: <reason>"
```

**Execution location differs:**
- Claude Code: evaluator runs in the stop hook (between turns)
- Cursor: subagent runs within the agent's turn (before turn ends)

### 3.3 Two-Layer Architecture

```
Layer 1 — In-Turn Evaluation (subagent):
  Agent works → thinks it might be done → spawns readonly subagent
  → subagent evaluates goal → YES: mark achieved, turn ends
                             → NO + reason: agent continues (same turn)

Layer 2 — Between-Turn Safety Net (stop hook):
  Turn ends → stop hook checks goal.json
  → goal still active → followup_message: "Continue toward goal"
  → goal achieved/paused → {} (allow stop)
```

This is **stronger than Claude Code** — evaluation can happen mid-turn, not
just at turn boundaries. The stop hook is a safety net, not the primary mechanism.

---

## 4. Standalone Skill Design

### 4.1 Design Decision: Independent Skill

`/goal` is a **standalone skill**, NOT integrated into durable-request. Reasons:

1. **Separation of concerns:** durable-request = "never end silently" (checkpoint).
   /goal = "auto-continue until done." Complementary but independent.
2. **Composability:** Users can use /goal alone, or combine with durable-request.
3. **Installation flexibility:** Optional addon, not forced dependency.

### 4.2 Integration with durable-request

When both skills are installed:

```
/durable-request /goal "all tests pass" --test "npm test"

  Phase 1: /goal behavior
  ─────────────────────
  Agent works autonomously
  Subagent evaluates after each work phase
  Stop hook provides safety net between turns
  (durable-request checkpoint does NOT fire during this phase)

  Phase 2: Goal completes → durable-request behavior
  ──────────────────────────────────────────────────
  Goal achieved → agent calls /deep-sleep
  → Session stays alive until user returns
  → User wakes agent, sees goal completion report
```

**Key:** Goal completion triggers `/deep-sleep`, not a checkpoint. This is correct
because goal tasks are inherently unattended — the user is likely away.

### 4.3 File Layout

```
~/.cursor/skills/goal/
├── SKILL.md              # Skill definition: /goal parsing + agent behavior
├── goal-stop.sh          # Stop hook: safety net for between-turn continuation
├── goal-manage.sh        # State management: create/status/pause/resume/clear
└── goal-evaluate.sh      # Optional: deterministic validation command runner

~/.durable-request/data/
└── goal.json             # Runtime state (reuses durable-request data dir)
```

### 4.4 goal.json State

```json
{
  "active": true,
  "condition": "all tests pass",
  "validation_command": "npm test",
  "created_at": "2026-05-22T19:00:00Z",
  "turn_budget": 20,
  "turns_used": 0,
  "status": "pursuing",
  "last_reason": "",
  "last_validation_output": ""
}
```

### 4.5 Evaluation Flow (Detailed)

```
Agent receives /goal or followup_message with goal context
       │
       ▼
Agent works toward goal (code changes, test runs, etc.)
       │
       ▼
Agent thinks work phase may be complete
       │
       ▼
Agent spawns readonly subagent (Task tool):
  Prompt: "Evaluate whether this goal is achieved:
           Condition: <condition>
           If --test command exists, check the last validation output.
           Based on conversation context, answer:
           YES: <reason> — if condition is met
           NO: <reason> — if condition is not met, explain what remains"
       │
       ├── Subagent returns "YES: all tests passing"
       │   └── Agent marks goal achieved in goal.json
       │       └── If durable-request active → call /deep-sleep
       │       └── If standalone → agent stops normally
       │
       └── Subagent returns "NO: 3 test failures remain in auth module"
           └── Agent incorporates reason, continues working (same turn)
           └── After more work → spawns subagent again
           └── (repeat until YES or turn ends naturally)
                    │
                    └── Turn ends with goal still active
                        └── stop hook fires → reads goal.json
                            └── goal active → followup_message:
                                "[GOAL] Continue toward: <condition>"
                            └── Agent starts new turn automatically
```

### 4.6 Stop Hook (goal-stop.sh)

The stop hook is a **safety net**, not the primary evaluator:

```bash
#!/usr/bin/env bash
# Read input from Cursor
read -r INPUT
STATUS=$(echo "$INPUT" | jq -r '.status')
LOOP_COUNT=$(echo "$INPUT" | jq -r '.loop_count // 0')

# Only process completed turns
[ "$STATUS" != "completed" ] && exit 0

# Read goal state
GOAL_FILE="$HOME/.durable-request/data/goal.json"
[ ! -f "$GOAL_FILE" ] && exit 0

ACTIVE=$(jq -r '.active' "$GOAL_FILE")
GOAL_STATUS=$(jq -r '.status' "$GOAL_FILE")

# If goal not active or not pursuing, allow normal stop
[ "$ACTIVE" != "true" ] || [ "$GOAL_STATUS" != "pursuing" ] && exit 0

# Check turn budget
TURN_BUDGET=$(jq -r '.turn_budget' "$GOAL_FILE")
TURNS_USED=$(jq '.turns_used + 1' "$GOAL_FILE")
jq ".turns_used = $TURNS_USED" "$GOAL_FILE" > "${GOAL_FILE}.tmp" \
  && mv "${GOAL_FILE}.tmp" "$GOAL_FILE"

CONDITION=$(jq -r '.condition' "$GOAL_FILE")

if [ "$TURNS_USED" -ge "$TURN_BUDGET" ] 2>/dev/null; then
  jq '.status = "budget-limited" | .active = false' "$GOAL_FILE" \
    > "${GOAL_FILE}.tmp" && mv "${GOAL_FILE}.tmp" "$GOAL_FILE"
  echo "{\"followup_message\": \"[GOAL BUDGET] Turn limit ($TURN_BUDGET) reached. Wrap up and summarize progress toward: $CONDITION\"}"
  exit 0
fi

# Safety net: goal still active, agent didn't evaluate → auto-continue
REMAINING=$((TURN_BUDGET - TURNS_USED))
echo "{\"followup_message\": \"[GOAL] Turn $TURNS_USED/$TURN_BUDGET ($REMAINING remaining). Continue working toward: $CONDITION\"}"
```

### 4.7 hooks.json

```json
{
  "version": 1,
  "hooks": {
    "stop": [
      {
        "command": "~/.cursor/skills/goal/goal-stop.sh",
        "loop_limit": null,
        "timeout": 10
      }
    ]
  }
}
```

- `loop_limit: null` — no cap (turn_budget in script manages this)
- `timeout: 10` — stop hook is lightweight (no validation cmd here)

### 4.8 SKILL.md Core Directives

```markdown
## /goal Command

When user says /goal:
1. Parse: /goal "<condition>" [--test "<command>"] [--budget <N>]
2. Write goal.json via Shell: goal-manage.sh create "<condition>" [--test "cmd"] [--budget N]
3. Begin autonomous work toward the condition

### During Active Goal

While goal.json shows status: "pursuing":
- Work toward the condition in focused phases
- After each significant work phase, evaluate using a subagent:
  Launch Task(readonly=true, subagent_type="generalPurpose"):
    "Evaluate whether goal is achieved. Condition: <X>.
     Last validation output: <Y>. Answer YES/NO with reason."
- If subagent says NO: incorporate the reason, continue working
- If subagent says YES: mark goal achieved via goal-manage.sh done
- Do NOT present durable-request checkpoints during active goal
- If --test command exists, run it before subagent evaluation

### Goal Lifecycle

/goal status  → Shell: goal-manage.sh status
/goal pause   → Shell: goal-manage.sh pause
/goal resume  → Shell: goal-manage.sh resume
/goal clear   → Shell: goal-manage.sh clear

### When Goal Completes

If durable-request is active → call /deep-sleep (user likely away)
If standalone → present completion summary and stop
```

---

## 5. Harness Engineering Considerations

### 5.1 Subagent Evaluator Prompt Engineering

The evaluator subagent prompt must be carefully crafted:

```
You are a goal completion evaluator. Your ONLY job is to determine whether
a goal condition has been met based on the evidence in the conversation.

Goal condition: "<condition>"

Validation command output (if available): "<output>"

Rules:
1. Answer ONLY "YES: <reason>" or "NO: <reason>"
2. Be conservative — only say YES when there is clear evidence
3. If no validation command output exists, evaluate based on
   the agent's work described in the conversation
4. Keep your reason to 1-2 sentences

Evidence to evaluate:
<recent conversation context or validation output>
```

### 5.2 Deterministic vs Model-Based Evaluation

When `--test` is provided, the agent should run the test command FIRST,
then pass its output to the subagent. This gives the subagent deterministic
evidence rather than relying on conversation heuristics.

```
Priority:
1. --test command exists → run it → pass exit code + output to subagent
2. No --test → subagent evaluates from conversation context alone
```

### 5.3 Turn Budget vs loop_limit

Two independent mechanisms:
- `loop_limit: null` in hooks.json — Cursor won't cap the stop hook
- `turn_budget` in goal.json — script-managed, logged, predictable

The script's turn_budget is the user-facing control. Cursor's loop_limit
is set to null so it doesn't interfere.

### 5.4 Edge Cases

| Edge Case | Handling |
|-----------|---------|
| Agent forgets to evaluate | Stop hook fires, sends followup_message |
| Subagent says YES prematurely | --test command provides ground truth |
| Goal condition too vague | SKILL.md warns: use specific, verifiable conditions |
| Runaway cost (no budget) | Default turn_budget = 20. SKILL.md reminds agent. |
| goal.json corrupted | goal-stop.sh exits 0 on parse error (fail-open) |
| User interrupts | status = "aborted" → script exits 0, no followup |
| Multiple /goal calls | New goal replaces old (goal-manage.sh create overwrites) |
| Network failure during subagent | Agent retries or defers to stop hook safety net |

---

## 6. Comparison with Claude Code

| Aspect | Claude Code | Our Cursor Design |
|--------|-------------|-------------------|
| Evaluator | Haiku (prompt-based hook) | Subagent (Task, readonly) |
| Evaluation timing | Between turns (stop hook) | **Within turn** (subagent) + between turns (safety net) |
| Evaluation scope | Transcript text only | Transcript + validation command output |
| Loop guard | stop_hook_active flag | loop_count + turn_budget in script |
| Cost model | Haiku tokens per evaluation | Subagent call (same model pool) |
| Status display | Built-in ◎ indicator | Agent text output |
| Post-goal behavior | Returns to user prompt | /deep-sleep (if durable-request) |

**Advantages of our design:**
1. Within-turn evaluation allows faster iteration (no turn boundary overhead)
2. Validation command output gives deterministic evidence to evaluator
3. Two-layer architecture (subagent + stop hook) is more robust
4. Tight integration with durable-request's /deep-sleep for unattended use

---

## 7. Implementation Checklist

| # | Deliverable | Est. |
|---|-------------|------|
| 1 | `goal-manage.sh` — state management script | 1d |
| 2 | `goal-stop.sh` — stop hook safety net | 1d |
| 3 | `SKILL.md` — /goal command + evaluation protocol | 2d |
| 4 | hooks.json integration/installer | 0.5d |
| 5 | Testing: manual integration test | 2d |
| 6 | Testing: edge cases (budget, abort, corrupt) | 1d |
| **Total** | | **~7.5d** |
