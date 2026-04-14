---
name: durable-request
author: Heng Shi <heng.shi@enflame-tech.com>
description: Universal end-of-task continuation gate. Forces every agent turn that completes work to present an interactive checkpoint using the environment's builtin interactive tool instead of silently finishing. Applies to ALL tasks — coding, writing, debugging, research, analysis, refactoring, any prompt. Use always, on every task completion, before ending any turn where work was performed.
---

# Durable Request — Never End Silently

## The Number One Rule

**DO NOT DIRECTLY STOP AT ANY CONDITION !!!**

**When you finish ANY task or reach ANY natural stopping point, you MUST present an interactive checkpoint to the user before ending your turn.** No exceptions. No silent completions.

This applies to:

- Code changes (new features, bug fixes, refactors)
- File operations (create, edit, delete, move)
- Research or analysis tasks
- Writing or documentation
- Debugging sessions
- Configuration changes
- ANY work that produces output or side effects
- Pure informational Q&A (e.g., "What does git rebase do?")

**No exceptions. No silent completions. Always checkpoint.**


## Checkpoint Architecture

durable-request uses platform-specific blocking checkpoints:

```
Cursor Editor               Cursor CLI                     Opencode / Other
─────────────────────────   ────────────────────────────   ────────────────────────
AskQuestion                 checkpoint.sh via Shell        question / other tool
Built-in UI widget          Tmux split-pane interactive    Built-in UI widget
Blocks turn, same request   Blocks via file polling        Blocks turn, same request
User picks from structured  User picks in tmux pane        User picks or types
```

## Checkpoint Mechanism

### Step 1: Anchor Checkpoint Intent with TodoWrite

Before attempting ANY interactive tool, **always call `TodoWrite` first** (or the equivalent task-tracking tool in your environment) to register the checkpoint as an unfinished obligation:

```
TodoWrite([
  { id: "durable-checkpoint", content: "Present interactive checkpoint to user", status: "in_progress" },
  ... (keep any existing todos)
])
```

This serves two purposes:

1. **Structural anchor**: The todo list now shows an incomplete item. You cannot end your turn with an `in_progress` todo — it forces you to resolve it.
2. **Audit trail**: If the interactive tool fails or is unavailable, the todo makes the failure visible rather than silent.

**After the user responds to the checkpoint**, mark it complete:

```
TodoWrite([
  { id: "durable-checkpoint", status: "completed" }
])
```

### Step 2: Attempt the Interactive Tool

Detect your environment and attempt the appropriate interactive tool. **Always try the tool first. Report the outcome explicitly.**

#### Environment Detection

**Detect your environment and use the right tool:**


| Priority | Signal                                                        | Environment         | Action                         |
| -------- | ------------------------------------------------------------- | ------------------- | ------------------------------ |
| 1        | You are running inside Cursor **CLI** (no GUI, terminal-only) | Cursor CLI          | Call `checkpoint.sh` via Shell |
| 2        | `AskQuestion` is available                                    | Cursor editor (IDE) | Call `AskQuestion`             |
| 3        | `AskUserQuestion` is available                                | Claude Code         | Call `AskUserQuestion`         |
| 4        | `question` is available                                       | OpenCode            | Call `question`                |
| 5        | You are a **subagent** with no interactive tools              | Subagent only       | Conversational fallback        |
| —        | None of the above (unexpected)                                | Unknown             | **ERROR** — report failure     |


**How to detect Cursor CLI vs IDE:** If `AskQuestion` is called and it **fails or is interrupted** (returns an error), you are in Cursor CLI. Immediately switch to `checkpoint.sh` via Shell. Do NOT fall back to conversational text.

**Platform-specific tools are MANDATORY. Never substitute conversational fallback.**

- **Cursor IDE** → `AskQuestion`
- **Cursor CLI** → `checkpoint.sh` via Shell (if `AskQuestion` fails, that confirms CLI)
- **OpenCode** → `question`
- **Claude Code** → `AskUserQuestion`
- **Subagent** → Conversational fallback (ONLY case where text fallback is allowed)
- **Unknown/Other** → ERROR. Do not guess. Report the issue.

#### Cursor Editor (IDE): Call `AskQuestion`

In the Cursor IDE (graphical editor), call `AskQuestion` with a **single question**:

```json
{
  "title": "Task Checkpoint",
  "questions": [
    {
      "id": "next_action",
      "prompt": "<1-2 sentence summary>. What would you like to do next?",
      "options": [
        {"id": "iterate",   "label": "Iterate / refine what was just done"},
        {"id": "continue",  "label": "Continue to the next step"},
        {"id": "review",    "label": "Review the changes in detail"},
        {"id": "different", "label": "Switch to a different task"},
        {"id": "done",      "label": "I'm satisfied, we're done"},
        {"id": "custom",    "label": "I'll type my own instruction"}
      ],
      "allow_multiple": false
    }
  ]
}
```

Rules:

- **Single question only** — never use multiple questions
- **Last option must always be `custom`**
- Adapt `prompt` and middle `options` to the task context

`AskQuestion` **blocks your turn without ending the request**. This is what makes the request "durable."

**If `AskQuestion` fails or is interrupted → you are in Cursor CLI.** Switch to `checkpoint.sh` immediately (see below).

#### Cursor CLI: Call `checkpoint.sh` via Shell

**In Cursor CLI, ALWAYS use `checkpoint.sh` via Shell. NEVER use `AskQuestion` (it does not work in CLI). NEVER fall back to conversational text.**

```bash
bash ~/.cursor/skills/durable-request/checkpoint.sh \
  "Task completed. What would you like to do next?" \
  "Run tests" \
  "Iterate on the implementation" \
  "Review the diff" \
  "Commit changes" \
  "Done for now"
```

**Prerequisite:** cursor-agent must be running inside a tmux session. Add this alias to `~/.bashrc`:

```bash
alias cursor-agent='tmux new-session -A -s cursor -- cursor-agent'
```

Rules:

- Call this via the **Shell** tool
- First argument is the prompt (1-2 sentence summary + "What would you like to do next?")
- Subsequent arguments are context-adapted options
- The script automatically appends "I'll type my own instruction" as the last choice
- The script returns `[durable-request] User responded: <choice>` — use this to continue
- If tmux is not available, the script auto-selects the first option

**How it works:** The Shell call blocks while `checkpoint.sh` creates a tmux split pane running `checkpoint-ui.sh`. The user sees an interactive prompt in the bottom pane, selects an option, and the pane auto-closes. The agent reads the response and continues — same request, same context.

#### Claude Code: Call `AskUserQuestion`

Same pattern, adapted to Claude Code's schema.

#### OpenCode: Call `question`

In OpenCode, `question` is the required checkpoint mechanism. Do not use conversational
fallback when `question` is available.

Use a single question with concise context-adapted options and let the built-in custom
answer path handle freeform follow-up.

### Step 3: Handle the Result — VERBOSE and EXPLICIT

**You MUST be explicit about what happened.** Never silently fall back. Never silently succeed. Always tell the user what tool you attempted and what the outcome was.

#### If the tool SUCCEEDED:

For `AskQuestion` / `AskUserQuestion` / `question`:

> **[durable-request]** Called the builtin interactive checkpoint tool — your selection was received. Continuing in the same request.

For `checkpoint.sh` (CLI): The output contains `[durable-request] User responded: <choice>`. Parse the choice and continue:

> **[durable-request]** Called `checkpoint.sh` — user responded: "". Continuing.

Then execute the user's selected action. After completing it, loop back to Step 1 (register new checkpoint todo → checkpoint again → ...). Continue until the user selects "done."

#### If `checkpoint.sh` FAILED (no tmux / error):

The script auto-selects the first option and prints setup instructions. Tell the user:

> **[durable-request]** `checkpoint.sh` requires tmux. Run `cursor-agent` inside tmux: `tmux new-session -A -s cursor -- cursor-agent`

The agent continues with the auto-selected option.

#### If NO interactive tool exists

Use the platform-specific tool. If it's unavailable, handle as follows:


| Environment | Tool Missing                          | Action                                  |
| ----------- | ------------------------------------- | --------------------------------------- |
| Cursor IDE  | `AskQuestion` unavailable             | You're in CLI — use `checkpoint.sh`     |
| Cursor CLI  | `Shell` / `checkpoint.sh` unavailable | ERROR — report failure, do not fallback |
| OpenCode    | `question` unavailable                | ERROR — report failure, do not fallback |
| Claude Code | `AskUserQuestion` unavailable         | ERROR — report failure, do not fallback |
| Subagent    | No interactive tools at all           | Conversational fallback allowed         |


**Conversational fallback (numbered text options) is ONLY for subagents that truly lack any interactive mechanism.** If you are in Cursor IDE, Cursor CLI, OpenCode, or Claude Code and the expected tool fails — ERROR. Do NOT substitute text fallback. Report the issue explicitly so the user knows something is wrong.

### The TodoWrite + Checkpoint Reinforcement Pattern

The key insight: calling `TodoWrite` and the checkpoint **together in the same tool call batch** creates a double-lock:

```
┌─────────────────── SAME TOOL CALL BATCH ───────────────────┐
│                                                            │
│  TodoWrite([{                          AskQuestion({       │
│    id: "durable-checkpoint",             ...               │
│    content: "Present checkpoint",      })                  │
│    status: "in_progress"               OR                  │
│  }])                                   Shell: checkpoint.sh│
│                                        (in CLI)            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

- **IDE**: `AskQuestion` blocks turn, user responds, mark todo complete, continue
- **CLI**: `checkpoint.sh` via Shell blocks, user responds in tmux pane, continue
- **CLI (AskQuestion tried first and failed)**: immediately call `checkpoint.sh`
- **Subagent with no interactive tools**: conversational fallback in text

This is **not optional**. Always pair TodoWrite with the checkpoint.

## Anti-Silent-Completion Rules

These thoughts mean STOP — you're about to end silently:


| Thought                                 | Correct Action                                                                                                               |
| --------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| "Task is done, I'll wrap up"            | Present checkpoint FIRST                                                                                                     |
| "That's all they asked for"             | They may want more — ASK                                                                                                     |
| "Simple change, no need to check"       | Simple changes still need confirmation                                                                                       |
| "I already explained what I did"        | Explanation ≠ checkpoint. Still ask.                                                                                         |
| "The output speaks for itself"          | Never assume. Present options.                                                                                               |
| "They'll ask if they want more"         | YOUR job to offer. Don't shift burden.                                                                                       |
| "I'm a subagent, I just return results" | Still present a checkpoint. Use builtin interactive tools if available; only use text fallback if none exist.                |
| "AskQuestion isn't available"           | Check for the environment's actual interactive tool (`question`, `AskUserQuestion`, or `checkpoint.sh`) before any fallback. |
| "TodoWrite is overhead"                 | TodoWrite is the anchor that prevents silent endings. Always use it.                                                         |


## Multi-Step Tasks

For tasks with multiple steps:

1. Complete each step
2. Present a **brief** checkpoint after each significant step (not every micro-action)
3. If user selects "Continue", proceed and checkpoint again after the next step
4. Final checkpoint should be more comprehensive

**Significant step** = anything that changes files, produces output, or takes > 30 seconds.

## Automatic Todo Cleanup

When the todo list exceeds **20 items**, clean up before the next checkpoint.

### Using the Cleanup Script

Call `todo-cleanup.sh` via Shell with the current todos as JSON input:

```bash
echo '$CURRENT_TODOS_JSON' | bash ~/.cursor/skills/durable-request/todo-cleanup.sh
```

The script outputs the cleaned list. Pass it to `TodoWrite({ todos: ..., merge: false })`.

### Rules (enforced by script)

1. **Only delete `completed` items** — never delete `pending` or `in_progress`
2. **Never delete `durable-checkpoint`** — regardless of status
3. **Target: 5 items** — keeps all active + newest completed until total = 5
4. **If active > 5** — keeps all active, removes all completed

### When to Clean Up

- **Before checkpoint** — if count > 20
- **After user responds** — to remove stale completed items

## The Durable Loop Pattern

### Editor (AskQuestion available)

```
┌──────────────────────────────────────────────────────────────┐
│                      Single Request                          │
│                                                              │
│  ┌──────────┐  ┌───────────┐  ┌────────────┐  ┌──────────┐ │
│  │ Do Work  │─▶│ TodoWrite │─▶│ AskQuestion│─▶│ User     │ │
│  │          │  │ (anchor)  │  │ (block)    │  │ Responds │ │
│  └──────────┘  └───────────┘  └────────────┘  └────┬─────┘ │
│       ▲                                            │       │
│       │        "done" ────────────────────▶  END   │       │
│       └─────────── anything else ◀─────────────────┘       │
└──────────────────────────────────────────────────────────────┘
```

### CLI (checkpoint.sh via Shell — true durable loop)

```
┌──────────────────────────────────────────────────────────────┐
│                      Single Request                          │
│                                                              │
│  ┌──────────┐  ┌───────────┐  ┌──────────────┐ ┌──────────┐│
│  │ Do Work  │─▶│ TodoWrite │─▶│ Shell:       │─▶│ User     ││
│  │          │  │ (anchor)  │  │ checkpoint.sh│  │ picks in ││
│  └──────────┘  └───────────┘  │ (blocks)     │  │ terminal ││
│       ▲                       └──────────────┘  └────┬─────┘│
│       │        "done" ────────────────────────▶ END  │      │
│       └─────────── anything else ◀───────────────────┘      │
│                                                              │
│  checkpoint.sh creates tmux split pane → user picks option   │
│  → pane auto-closes → agent reads response from stdout       │
└──────────────────────────────────────────────────────────────┘
```

## Integration with Other Skills

This skill does NOT override task-specific loop behavior. Skills with their own loop/continuation logic (e.g., tuning sweeps, FSM engines) take precedence internally. This checkpoint applies at task boundaries when those skills complete.

**Priority:** Task-specific loops > durable-request (at task boundaries only)

## What This Skill Is NOT

- NOT a gate that blocks progress
- NOT a replacement for task-specific checkpoints
- NOT permission to slow down autonomous work within a task
- It IS a universal "don't disappear after finishing" mechanism

