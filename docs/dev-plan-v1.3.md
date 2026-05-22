# durable-request v1.3 Development Plan

> **Version:** 1.3.0  
> **Codename:** "Remember & Persist"  
> **Features:** `/goal` (autonomous loop) + L1 Memory (project state) + L2 Memory (user preferences)  
> **Estimated effort:** 3-4 weeks total  
> **Prerequisite:** durable-request v1.2.0 installed

---

## Feature 1: `/goal` — Autonomous Goal Loop

### Overview

The agent works toward a verifiable objective across multiple turns without
user interaction. A fast evaluator checks after each turn if the goal is met.
If not, the agent auto-continues. When met, the goal clears and a normal
durable-request checkpoint fires.

### Architecture

```
User: /goal "all tests pass in src/auth/"
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  SKILL.md parses /goal → writes goal.json → starts work    │
│                                                             │
│  Agent does work (turn 1)                                   │
│         │                                                   │
│         ▼                                                   │
│  Agent turn ends → stop hook fires                          │
│         │                                                   │
│         ▼                                                   │
│  goal-stop.sh reads goal.json                               │
│  ├── No active goal? → exit (normal durable checkpoint)     │
│  ├── Run validation: npm test -- --testPathPattern=auth     │
│  │   ├── Exit 0 (pass) → goal achieved → clear goal.json   │
│  │   │   → return {} → durable checkpoint fires             │
│  │   └── Exit 1 (fail) → return followup_message:           │
│  │       "Tests still failing. Continue working: <goal>"    │
│  │       → agent starts new turn automatically              │
│  └── Turn budget exceeded? → pause goal, checkpoint         │
│                                                             │
│  Repeat until goal met, budget hit, or user /goal clear     │
└─────────────────────────────────────────────────────────────┘
```

### Deliverables

#### 1.1 `goal.json` schema

```json
{
  "active": true,
  "condition": "all tests pass in src/auth/",
  "validation_command": "npm test -- --testPathPattern=auth",
  "created_at": "2026-05-22T19:00:00Z",
  "turn_count": 0,
  "turn_budget": 20,
  "status": "pursuing"
}
```

Location: `~/.durable-request/data/goal.json`

Status values: `pursuing | paused | achieved | budget-limited`

#### 1.2 `goal-stop.sh` — stop hook script

**Input** (from Cursor, via stdin):
```json
{
  "loop_count": 3
}
```

**Logic:**
1. Read `~/.durable-request/data/goal.json`
2. If no active goal or status != "pursuing" → exit 0 (no output)
3. Increment turn_count in goal.json
4. If turn_count >= turn_budget → set status="budget-limited", output:
   ```json
   {
     "followup_message": "[GOAL BUDGET] Turn limit reached (20/20). Goal paused. Run /goal resume to continue or /goal clear to stop. Summary: <condition>"
   }
   ```
5. If validation_command exists → run it:
   - Exit 0 → set status="achieved", output `{}`
   - Exit non-0 → output:
     ```json
     {
       "followup_message": "[GOAL] Turn 4/20. Tests still failing (3 failures). Continue working toward: all tests pass in src/auth/"
     }
     ```
6. If no validation_command → use prompt-based evaluation:
   - Read recent agent output
   - Simple heuristic: does the output contain "Done" or success indicators?
   - If unclear → continue (err on side of continuation)

**File:** `.cursor/skills/durable-request/goal-stop.sh`

#### 1.3 hooks.json update

Add to `~/.cursor/hooks.json`:
```json
{
  "stop": [
    {
      "command": "~/.cursor/skills/durable-request/goal-stop.sh",
      "loop_limit": null
    }
  ]
}
```

`loop_limit: null` removes the default cap of 5 auto-continuations.

Update `install-steering.sh` to install this hook alongside the existing
preToolUse steering hook.

#### 1.4 SKILL.md update

Add `/goal` section:

```markdown
## /goal — Autonomous Goal Loop

When the user invokes /goal:
1. Parse the goal condition and optional validation command
2. Write goal.json to ~/.durable-request/data/goal.json
3. Start working toward the goal immediately
4. The stop hook handles auto-continuation — you don't need to manage it
5. When the goal is achieved, present a normal durable-request checkpoint

Commands:
- /goal <condition>              — Set a new goal
- /goal <condition> --test "cmd" — Set goal with validation command
- /goal                          — Show current goal status
- /goal pause                    — Pause the goal
- /goal resume                   — Resume a paused goal
- /goal clear                    — Clear the goal
- /goal budget <N>               — Set turn budget (default: 20)
```

#### 1.5 Testing

New workload: `testing/workloads/12-goal.md`
- Task: "Set goal to make all tests pass, intentionally break 2 tests"
- Expected: Agent fixes tests autonomously, goal clears, checkpoint fires
- Features to verify: F11 (goal set), F12 (auto-continue), F13 (goal achieved)

New patterns in `testing/scripts/patterns.py`:
- F11: Goal activation (`goal.json.*pursuing`)
- F12: Auto-continuation (`followup_message.*GOAL`)
- F13: Goal achievement (`goal.*achieved`)

### Effort: ~2 weeks

| Task | Days |
|------|------|
| goal-stop.sh implementation | 3 |
| SKILL.md /goal section | 1 |
| hooks.json installer update | 1 |
| Testing workload + patterns | 2 |
| Integration testing (manual) | 3 |

---

## Feature 2: L1 Memory — Project State Persistence

### Overview

Automatically save project state at session end; restore it at session start.
The agent knows "where we left off" without the user re-explaining.

### Architecture

```
Session N ends (stop/sessionEnd hook):
         │
         ▼
┌────────────────────────────────────────────────────┐
│  state-save.sh                                     │
│  1. Read current TodoWrite state (from agent's     │
│     last checkpoint — state file written by agent)  │
│  2. Read git status (branch, recent commits, diff) │
│  3. Read goal.json (if active)                     │
│  4. Write to:                                      │
│     ~/.durable-request/memory/<project>/state.md   │
└────────────────────────────────────────────────────┘

Session N+1 starts (sessionStart hook):
         │
         ▼
┌────────────────────────────────────────────────────┐
│  state-restore.sh                                  │
│  1. Read ~/.durable-request/memory/<project>/      │
│     state.md                                       │
│  2. Return as additional context for the agent:    │
│     "[SESSION RESUME] Previous session state:      │
│      Branch: feature/auth                          │
│      Completed: login, JWT setup                   │
│      Pending: password reset, tests                │
│      Last decision: using bcrypt over argon2"      │
└────────────────────────────────────────────────────┘
```

### Deliverables

#### 2.1 Agent-written state file

SKILL.md instructs the agent to maintain a state file:

```markdown
## Project State Persistence

After each checkpoint, update the project state file:
  ~/.durable-request/memory/<project-slug>/state.md

Format:
  # Project State: <project-name>
  Updated: <timestamp>

  ## Completed This Session
  - <task 1>
  - <task 2>

  ## Pending
  - <task 1>
  - <task 2>

  ## Key Decisions
  - <decision>: <reasoning>

  ## Current Branch
  <branch name>

  ## Notes
  <anything the next session should know>

The <project-slug> is derived from the workspace path (e.g., home-albert-my-project).
```

#### 2.2 `state-save.sh` — sessionEnd / stop hook enhancement

Runs at session end. Appends git context to the agent-written state file:
- Current branch and recent commits (last 5)
- Modified files count
- Whether there are uncommitted changes

**File:** `.cursor/skills/durable-request/state-save.sh`

#### 2.3 `state-restore.sh` — sessionStart hook

Runs at session start. If a state file exists for the current project:
- Read the state file
- Output as `additionalContext` or inject into the conversation

**Note:** `sessionStart` hook is fire-and-forget in Cursor. The mechanism
for injecting context is:
- Option A: Write context to a temp file, have a preToolUse hook inject it
  on the first tool call (similar to steering injection)
- Option B: Write context to a `.cursor/rules/session-resume.mdc` temp rule
  file that auto-loads (delete after first use)

Option B is cleaner — use a temp rule file.

**File:** `.cursor/skills/durable-request/state-restore.sh`

#### 2.4 hooks.json additions

```json
{
  "sessionStart": [
    {
      "command": "~/.cursor/skills/durable-request/state-restore.sh"
    }
  ],
  "stop": [
    {
      "command": "~/.cursor/skills/durable-request/state-save.sh"
    }
  ]
}
```

#### 2.5 Directory structure

```
~/.durable-request/
├── data/
│   ├── goal.json
│   ├── steering-message
│   └── ...
└── memory/
    ├── home-albert-workspace-my-project/
    │   └── state.md
    ├── home-albert-workspace-other-project/
    │   └── state.md
    └── ...
```

### Effort: ~1 week

| Task | Days |
|------|------|
| state-save.sh | 1 |
| state-restore.sh + temp rule injection | 2 |
| SKILL.md instructions for state writing | 1 |
| hooks.json installer update | 0.5 |
| Testing | 1.5 |

---

## Feature 3: L2 Memory — User Preference Learning

### Overview

The agent detects when the user corrects its behavior, extracts the preference,
confirms with the user, and persists it as a Cursor User Rule that auto-applies
to all future sessions.

### Architecture

```
During a durable session:
         │
  User: "不要用 npm，用 pnpm"
         │
         ▼
┌────────────────────────────────────────────────────┐
│  Agent detects correction/preference               │
│  At next checkpoint, adds option:                  │
│  "我注意到你偏好 pnpm。要我记住这个偏好吗？"         │
│         │                                          │
│         ▼                                          │
│  User confirms → Agent calls cursor_dialog MCP:    │
│  {                                                 │
│    item: "rule",                                   │
│    scope: "user",                                  │
│    action: "add",                                  │
│    content: "Always use pnpm, never npm or yarn"   │
│  }                                                 │
│         │                                          │
│         ▼                                          │
│  Cursor adds User Rule → auto-applied forever      │
└────────────────────────────────────────────────────┘
```

### Deliverables

#### 3.1 SKILL.md preference detection instructions

Add to SKILL.md:

```markdown
## User Preference Learning

During a durable session, watch for user corrections — any time the user
tells you to change your approach, tool choice, style, or behavior.

Examples of corrections:
- "用 pnpm 不要 npm"
- "变量名用驼峰"
- "不要加那么多注释"
- "commit message 用英文"
- "先写测试"

When you detect a correction:
1. Note it internally
2. At the NEXT checkpoint, add a preference confirmation option:
   Option B or C: "Remember preference: <description>? (writes User Rule)"
3. If the user selects it:
   a. First, call cursor_dialog to list existing user rules to avoid duplicates
   b. Then call cursor_dialog to add the new rule
   c. Confirm: "Preference saved. It will apply to all future sessions."

DO NOT auto-save preferences without user confirmation.
DO NOT save project-specific preferences as user rules (those belong in
project rules).

cursor_dialog usage:
  - List: { item: "rule", scope: "user", action: "list" }
  - Add:  { item: "rule", scope: "user", action: "add",
            content: "<preference description>" }
```

#### 3.2 cursor_dialog MCP integration

The `cursor-app-control` MCP already provides `cursor_dialog` with rule
management. No new MCP code needed — just SKILL.md instructions to use it.

Verify the MCP tool descriptor for correct parameter format.

#### 3.3 Preference deduplication

Before adding a new preference, list existing rules and check for duplicates.
The SKILL.md instructs the agent to do this check.

#### 3.4 Testing

New workload: `testing/workloads/13-preference-learning.md`
- Task: "Write a function" → user corrects "use TypeScript not JavaScript"
- Expected: At checkpoint, agent offers to save preference
- Features: F14 (preference detected), F15 (preference saved)

### Effort: ~1 week

| Task | Days |
|------|------|
| SKILL.md preference detection instructions | 2 |
| cursor_dialog MCP descriptor verification | 0.5 |
| Testing workload + patterns | 1.5 |
| Manual testing with real corrections | 1 |

---

## Implementation Order

```
Week 1-2: /goal
  ├── goal-stop.sh
  ├── SKILL.md /goal section
  ├── hooks.json update
  └── Testing

Week 3: L1 Memory (Project State)
  ├── state-save.sh
  ├── state-restore.sh
  ├── SKILL.md state instructions
  └── Testing

Week 4: L2 Memory (User Preferences)
  ├── SKILL.md preference learning
  ├── cursor_dialog integration
  └── Testing
```

### Dependencies

```
/goal ──────────────► independent (can ship alone)
L1 Memory ──────────► independent (can ship alone)
L2 Memory ──────────► depends on cursor_dialog MCP (already available)
                      independent of /goal and L1

All three ──────────► require install-steering.sh update for hooks.json
```

### Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|-----------|
| `stop` hook `followup_message` doesn't work as documented | /goal blocked | Test immediately on day 1. If broken, fall back to Shell-blocking loop. |
| `sessionStart` hook can't inject context effectively | L1 partially blocked | Fall back to temp rule file injection via `.cursor/rules/` |
| `cursor_dialog` MCP API changes | L2 blocked | Pin to current API. Fall back to SKILL.md instruction "write a .cursor/rules/ file manually" |
| `loop_limit: null` not respected | /goal capped at 5 turns | Verify on day 1. If broken, use multiple stop hook entries or workaround. |
| Long /goal runs consume excessive tokens | Cost overrun | Enforce turn budget (default 20). Add token estimation warning. |

---

## CHANGELOG entry (draft)

```
## [1.3.0] - 2026-06-XX

### Added
- **/goal — Autonomous Goal Loop**: Set a verifiable objective and the agent
  works toward it across multiple turns without user interaction. Uses Cursor's
  `stop` hook with `followup_message` for auto-continuation. Supports
  validation commands, turn budgets, pause/resume/clear lifecycle.
- **L1 Memory — Project State Persistence**: Automatically saves project
  state (completed work, pending tasks, decisions, git context) at session end.
  Restores state at session start so the agent knows where you left off.
- **L2 Memory — User Preference Learning**: Detects user corrections during
  durable sessions. Offers to save preferences as Cursor User Rules via
  `cursor_dialog` MCP. Preferences auto-apply to all future sessions.
- New test workloads: 12-goal.md, 13-preference-learning.md
- New feature patterns: F11-F15

### Changed
- install-steering.sh now installs `stop` and `sessionStart/End` hooks
  in addition to the existing `preToolUse` steering hook
- hooks.json schema updated to support multiple hook types
```

---

## Success Criteria

| Feature | Metric | Target |
|---------|--------|--------|
| /goal | Agent auto-continues without user input | 100% of /goal invocations |
| /goal | Goal achieves when validation passes | 100% of test cases |
| /goal | Budget limit stops runaway | 100% of budget-limited cases |
| L1 Memory | State saved at session end | 100% of sessions |
| L1 Memory | State restored at session start | 100% when state file exists |
| L2 Memory | Preference detected from correction | >80% of corrections |
| L2 Memory | Preference saved after confirmation | 100% of confirmed preferences |
| Overall | No regression in F1-F10 features | 100% pass rate |
