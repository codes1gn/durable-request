# /goal — Autonomous Goal Loop

Set a persistent objective. Work toward it across turns until it's met.

## How It Works

You set a completion condition. After each work phase, a subagent evaluates
whether the condition holds. If not, you continue working. A stop hook provides
a safety net between turns — if you end a turn with the goal still active,
the hook auto-continues you.

## Platform Behavior

- **Cursor IDE / CLI:** Stop hook uses `followup_message` for auto-continuation.
  Subagent evaluation within turns via Task tool.
- **Claude Code:** Native `/goal` command is preferred (built-in prompt-based
  Stop hook with Haiku evaluator). This skill adds state management and
  the `/goal` command interface if the native command is unavailable.

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

Parse the command and manage state via Shell:

```bash
bash ~/.cursor/skills/goal/goal-manage.sh create "<condition>" --test "<cmd>" --budget <N>
bash ~/.cursor/skills/goal/goal-manage.sh status
bash ~/.cursor/skills/goal/goal-manage.sh pause
bash ~/.cursor/skills/goal/goal-manage.sh resume
bash ~/.cursor/skills/goal/goal-manage.sh done
bash ~/.cursor/skills/goal/goal-manage.sh clear
```

After creating the goal, **immediately start working toward the condition**.

## Working Toward the Goal

### Work Phase Protocol

While the goal is active (`status: "pursuing"`):

1. **Do focused work** — make code changes, run commands, fix issues
2. **Run validation** (if `--test` provided) — execute the test command
3. **Evaluate** — spawn a readonly subagent to judge completion
4. **Act on result** — YES → mark done. NO → incorporate reason, continue.

### Evaluation via Subagent

After each significant work phase, spawn a readonly subagent:

```
Task(
  subagent_type: "generalPurpose",
  readonly: true,
  description: "Evaluate goal completion",
  prompt: "You are a goal completion evaluator. Determine whether this goal
           condition has been achieved based on the evidence provided.

           Goal condition: <condition>
           Validation command output (if available): <output>
           Recent work summary: <what was done>

           Rules:
           1. Answer ONLY 'YES: <reason>' or 'NO: <reason>'
           2. Be conservative — only YES with clear evidence
           3. If validation command passed (exit 0), that is strong evidence
           4. Keep reason to 1-2 sentences"
)
```

**YES** → `goal-manage.sh done` → report achievement, end turn
**NO** → continue working, incorporate the reason

### When to Evaluate

Evaluate after completing a logical unit of work or seeing new validation
results. Do NOT evaluate after every micro-action.

## Writing Good Conditions

```
Good:  "all tests in test/auth/ pass"       → verifiable
Good:  "npm run build exits with code 0"    → deterministic
Bad:   "the code is clean"                  → subjective
Bad:   "implement the feature"              → vague
```

Always use `--test` when a validation command exists.
