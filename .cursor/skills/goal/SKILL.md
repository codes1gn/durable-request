# /goal — Autonomous Goal Loop

Set a persistent objective. Work toward it across turns until it's met.

## How It Works

You set a completion condition. After each work phase, a subagent evaluates
whether the condition holds. If not, you continue working. A stop hook provides
a safety net between turns — if you end a turn with the goal still active,
the hook auto-continues you with a `followup_message`.

```
/goal "all tests pass" --test "npm test" --budget 20
  ↓
goal-manage.sh create → goal.json written
  ↓
Agent works → runs tests → spawns evaluator subagent
  ↓
Subagent says NO → agent continues (same turn)
Subagent says YES → goal-manage.sh done → goal achieved
  ↓
Turn ends → stop hook checks goal.json
  ↓
Still active → followup_message (auto-continue)
Achieved → {} (allow stop)
```

## Command Reference

| Command | Action |
|---------|--------|
| `/goal "<condition>"` | Set goal and start working |
| `/goal "<condition>" --test "<cmd>"` | Set goal with validation command |
| `/goal "<condition>" --budget <N>` | Set goal with custom turn budget (default: 20) |
| `/goal status` | Show current goal state |
| `/goal pause` | Pause auto-continuation |
| `/goal resume` | Resume a paused goal |
| `/goal clear` | Remove goal entirely |

## Setting a Goal

When the user says `/goal`, parse the command and manage state:

```bash
# Create a goal
bash ~/.cursor/skills/goal/goal-manage.sh create "<condition>" --test "<cmd>" --budget <N>

# Other lifecycle commands
bash ~/.cursor/skills/goal/goal-manage.sh status
bash ~/.cursor/skills/goal/goal-manage.sh pause
bash ~/.cursor/skills/goal/goal-manage.sh resume
bash ~/.cursor/skills/goal/goal-manage.sh done
bash ~/.cursor/skills/goal/goal-manage.sh clear
```

After creating the goal, **immediately start working toward the condition**.
Do not checkpoint. Do not ask what to do. Begin.

## Working Toward the Goal

### Work Phase Protocol

While the goal is active (`status: "pursuing"`), repeat this cycle:

1. **Do focused work** — make code changes, run commands, fix issues
2. **Run validation** (if `--test` provided) — execute the test command via Shell
3. **Evaluate** — spawn a readonly subagent to judge completion
4. **Act on result** — YES → mark done. NO → incorporate reason, continue.

### Evaluation via Subagent

After each significant work phase (not every micro-action), evaluate:

```
Task(
  subagent_type: "generalPurpose",
  readonly: true,
  description: "Evaluate goal completion",
  prompt: "You are a goal completion evaluator. Determine whether this goal
           condition has been achieved based on the evidence provided.

           Goal condition: <condition from goal.json>

           Validation command output (if available):
           <last validation output, or 'no validation command configured'>

           Recent work summary:
           <brief description of what was just done>

           Rules:
           1. Answer ONLY with 'YES: <reason>' or 'NO: <reason>'
           2. Be conservative — only YES when there is clear evidence
           3. If validation command passed (exit 0), that is strong evidence
           4. Keep reason to 1-2 sentences
           5. For NO, explain what specific work remains"
)
```

### Acting on Evaluation Result

**Subagent returns "YES: ..."**
1. Run `goal-manage.sh done` via Shell
2. Report the achievement to the user
3. If durable-request is active → invoke `/deep-sleep` to keep session alive
4. If standalone → end turn normally

**Subagent returns "NO: ..."**
1. Parse the reason — it tells you what remains
2. Continue working toward the goal in the same turn
3. After more work, evaluate again
4. Do NOT end the turn while the goal is still pursuing

### When to Evaluate

Evaluate after:
- Running the validation command and seeing a new result
- Completing a logical unit of work (e.g., fixing a failing test)
- Making changes that could plausibly satisfy the condition

Do NOT evaluate after:
- Every single file edit
- Reading files or gathering context
- Planning or thinking (no observable change)

## Stop Hook Safety Net

The stop hook (`goal-stop.sh`) fires when your turn ends. If the goal is
still active, it returns a `followup_message` that auto-continues you.

**You should NOT rely on the stop hook as the primary evaluator.** It is
a safety net for cases where you forget to evaluate or end the turn
prematurely. The subagent evaluation within your turn is the primary
mechanism.

The stop hook also:
- Increments the turn counter
- Checks the turn budget
- Runs the validation command (if configured) for quick feedback
- Forces a budget-limit wrap-up when turns are exhausted

## Turn Budget

Default budget is 20 turns. When the budget is hit:
1. The stop hook sets `status: "budget-limited"` and `active: false`
2. You receive a final `followup_message` asking you to wrap up
3. Summarize progress, list what remains, and stop

Users can customize: `/goal "condition" --budget 50`

## Writing Good Conditions

Good conditions are specific and verifiable:

```
✓ "all tests in test/auth/ pass"                    → run tests, check exit code
✓ "npm run build exits with code 0"                 → run build, check exit code
✓ "no ESLint errors in src/"                        → run eslint, check output
✓ "the login page renders without console errors"   → observable in test output
```

Bad conditions are vague or subjective:

```
✗ "the code is clean"                → no objective measure
✗ "implement the feature"            → too vague, when is it "done"?
✗ "fix the bug"                      → which bug? what proves it's fixed?
```

When the condition has a natural test command, always use `--test`:
```
/goal "all tests pass" --test "npm test"
/goal "build succeeds" --test "npm run build"
/goal "no lint errors" --test "eslint src/ --quiet"
```

## Integration with durable-request

When both /goal and durable-request are installed:

- **Goal active:** auto-continuation via stop hook + subagent evaluation.
  durable-request checkpoints are **suppressed** — do not call AskQuestion
  or checkpoint.sh while pursuing a goal.

- **Goal achieved:** invoke `/deep-sleep` to keep the session alive.
  The user is likely away (that's why they set a goal). When they return
  and wake the session, they'll see the completion report.

- **Goal budget-limited:** same as achieved — `/deep-sleep` after
  the wrap-up summary.

- **Goal cleared by user:** return to normal durable-request behavior
  (checkpoint at next stopping point).

## State File

Located at `~/.durable-request/data/goal.json`:

```json
{
  "active": true,
  "condition": "all tests pass",
  "validation_command": "npm test",
  "created_at": "2026-05-22T19:00:00Z",
  "turn_budget": 20,
  "turns_used": 3,
  "status": "pursuing",
  "last_reason": "2 tests still failing in auth module",
  "last_validation_output": "Tests: 2 failed, 48 passed, 50 total"
}
```

Status values: `pursuing`, `paused`, `achieved`, `budget-limited`

## Followup Message Format

When the stop hook auto-continues you, you'll receive a user message like:

```
[GOAL] Turn 3/20 (17 remaining). Continue working toward: all tests pass
```

or with validation results:

```
[GOAL] Turn 5/20. Validation FAILED (exit 1): Tests: 2 failed. Continue working toward: all tests pass
```

or on budget limit:

```
[GOAL BUDGET] Turn limit (20) reached. Wrap up current work and summarize progress toward: all tests pass
```

When you see `[GOAL]` prefix in a user message, you know you're in an
auto-continued turn. Resume working toward the condition immediately.
Do not re-introduce yourself or ask what to do.
