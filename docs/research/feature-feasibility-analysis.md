# Feature Feasibility Analysis

> **Purpose:** Technical feasibility assessment for each feature identified in
> `industry-feature-landscape-2026.md`. Each feature is evaluated on implementation
> difficulty, platform constraints, and integration path with the current durable-request
> infrastructure.
>
> **Date:** 2026-05-22  
> **Baseline:** durable-request v1.2.0 on Cursor IDE + CLI

---

## Feasibility Rating Scale

| Rating | Meaning |
|--------|---------|
| **F1 — Trivial** | Can implement with current infrastructure (skills + scripts). Days. |
| **F2 — Straightforward** | Needs new scripts/skills but no new platform features. 1-2 weeks. |
| **F3 — Moderate** | Needs hooks, MCP, or significant new code. 2-4 weeks. |
| **F4 — Hard** | Needs platform features that may not exist yet, or major architecture. 1-2 months. |
| **F5 — Blocked** | Requires platform changes outside our control, or fundamentally incompatible. |

---

## Tier 1 Features (Transformative)

### 1. `/goal` — Autonomous Goal Loop

**Value:** Very High  
**Feasibility:** F2-F3

**How it works in Claude Code / Codex:**
A fast evaluator model checks after every turn whether a goal condition is met.
If not met, the agent auto-continues with a new turn.

**Implementation path for durable-request:**

Cursor's `stop` hook is the key enabler. From the hooks documentation:

> The optional `followup_message` is a string. When provided and non-empty,
> Cursor will automatically submit it as the next user message. This enables
> loop-style flows (e.g., iterate until a goal is met).

This is literally designed for `/goal`. The implementation would be:

```
1. User invokes /goal "all tests pass"
2. Skill writes goal condition to ~/.durable-request/data/goal.json
3. stop hook (goal-stop.sh) fires after each agent turn:
   a. Reads goal.json
   b. If no active goal → exit (no followup)
   c. If active goal → evaluate condition:
      - Run validation command if specified (e.g., npm test)
      - Or use prompt-based hook with fast model to evaluate
   d. If NOT met → return { followup_message: "Continue working toward: <goal>" }
   e. If met → clear goal, return {} (agent stops, durable-request checkpoint fires)
4. loop_limit (default 5) needs to be set to null or a high number
```

**Constraints:**
- `loop_limit` defaults to 5 per script. Must set to `null` for long-running goals.
  This is configurable per-hook in `hooks.json`.
- `followup_message` only consumed when `status` is `"completed"` — need to verify
  the stop hook receives the right status when the agent naturally finishes.
- For CLI (no stop hook): can implement via `checkpoint.sh` variant that auto-selects
  "continue" if goal is not met, but this is clunkier.
- Cost control: need a turn counter and/or token budget to prevent runaway.

**Platform support:**

| Platform | Mechanism | Works? |
|----------|-----------|--------|
| Cursor IDE | `stop` hook + `followup_message` | Yes — native support |
| Cursor CLI | `stop` hook (same hooks.json) | Yes — same mechanism |
| Claude Code | Native `/goal` command | Already exists, no need to build |
| Codex CLI | Native `/goal` command | Already exists, no need to build |
| Others | Skill-level loop via checkpoint auto-select | Degraded but functional |

**Files to create:**
- `goal-stop.sh` — stop hook script
- `/goal` section in SKILL.md
- Update `hooks.json` installation in `install-steering.sh`

**Verdict: GO.** The `stop` hook + `followup_message` makes this straightforward
for Cursor. The hardest part is the evaluator logic, which can start simple
(run a shell command, check exit code) and evolve to prompt-based evaluation later.

---

### 2. Channels — Event-Driven Reactions

**Value:** Very High  
**Feasibility:** F4-F5

**How it works in Claude Code:**
MCP servers push events (CI failures, chat messages, webhooks) into the running
session. The agent reacts without polling.

**Implementation path for durable-request:**

This requires an always-running process that:
1. Listens for incoming events (HTTP webhooks, WebSocket, etc.)
2. Translates events into agent-visible signals
3. Delivers signals to the agent mid-session

**Challenge 1: How to deliver events to the agent**

In Cursor, the only way to inject information into the agent is:
- `preToolUse` hook: modify Shell commands (current steering approach)
- `beforeSubmitPrompt` hook: inject into prompts
- `stop` hook: send followup_message
- MCP tools: agent must actively call them

None of these are "push" — they all require the agent to be doing something
(calling a tool, finishing a turn) to trigger. True push requires the `stop` hook
to fire a `followup_message` when an event arrives, but the `stop` hook only
fires after a turn completes, not mid-turn.

**Challenge 2: MCP server lifecycle**

Cursor can load MCP servers, but they're configured per-project or globally.
A "channels" MCP server would need to:
- Run as a background process
- Listen on a port for incoming webhooks
- Expose a `get_pending_events` tool the agent can call
- Or use the `stop` hook to inject events as followup_messages

**Challenge 3: The agent isn't always "listening"**

In durable-request, the agent is either:
- Working on a task (not polling for events)
- Blocked on `AskQuestion` or `checkpoint.sh` (can't receive events)
- In `deep-sleep` (can receive events via file-based wake mechanism)

The only realistic delivery path is:
1. Event arrives → write to file (like steering)
2. On next `preToolUse` (Shell), inject the event into output
3. Agent sees it and reacts

This is essentially "steering but for external events" — feasible but not
real-time push. It's polling at the speed of tool calls.

**Simplified viable path:**
- Build a `event-listener.sh` that runs in the background (tmux pane or daemon)
- Listens for CI webhook (simple HTTP server via `nc` or `socat`)
- Writes event to `~/.durable-request/data/pending-event`
- `preToolUse` hook picks it up on next Shell call (same as steering)
- Agent acknowledges and reacts

**Platform support:**

| Platform | Mechanism | Quality |
|----------|-----------|---------|
| Cursor IDE | preToolUse injection (polling, not push) | Degraded — not real-time |
| Cursor CLI | Same as above | Degraded |
| Claude Code | Native Channels | Already exists, superior |

**Verdict: DEFER.** The value is very high but the implementation is a poor
approximation of what Claude Code does natively. The file-based polling approach
(steering-style) is feasible but doesn't deliver the "reactive hub" experience.
Better to wait for Cursor to add channel-like support, or to invest this effort
in `/goal` which has much better platform support. Could prototype a minimal
CI-webhook-to-steering bridge as a low-effort experiment.

---

### 3. Kanban Multi-Agent Orchestration

**Value:** Very High  
**Feasibility:** F4

**How it works in Cline:**
Web-based task board. Each card is a live agent in its own git worktree.
Dependency chains auto-start. Auto-commit.

**Implementation path for durable-request:**

This is a separate product, not a skill. It would need:
1. A web UI (React, already have website infrastructure)
2. Agent lifecycle management (spawn, monitor, stop)
3. Git worktree management (create, symlink, cleanup)
4. Inter-agent communication (task completion → trigger next)
5. Diff review UI

**Simplified viable path (CLI-only):**
- `durable-kanban.sh` — CLI task board using tmux panes
- Each task gets a tmux window with its own worktree
- Tasks tracked in a JSON file
- Dependencies are simple: when task A's tmux window closes,
  task B auto-starts
- No web UI, just tmux + status display

**Platform support:**

| Platform | Mechanism | Quality |
|----------|-----------|---------|
| CLI (tmux) | tmux panes + worktrees | Functional but basic |
| Web UI | Separate project | Full experience but large effort |

**Verdict: FUTURE.** The value is real but the scope is a separate product.
A minimal tmux-based prototype could demonstrate the concept, but it would
compete with Cline Kanban which is already available and agent-agnostic.
Better to focus on features that enhance the single-agent durable session.

---

### 4. Context Compaction with Preservation

**Value:** Very High  
**Feasibility:** F2 (Cursor IDE), F5 (Cursor CLI)

**How it works in Claude Code:**
`/compact` manually triggers summarization. Auto-compact at ~95% context usage.
Custom preservation instructions via `CLAUDE.md` "Compact Instructions".
`PreCompact` hook allows injecting preservation directives.

**Implementation path for durable-request:**

**Cursor IDE:**
Cursor already has `preCompact` hook support. The implementation would be:

```
1. preCompact hook (compact-preserve.sh) fires before compaction
2. Hook reads current durable-request state:
   - Active goal (if /goal is active)
   - Pending steering messages
   - Recent checkpoint history
   - Key decisions from the session
3. Hook injects preservation instructions into the compaction prompt
4. After compaction, durable-request state is preserved
```

**The key question:** What does the `preCompact` hook receive and return?
From the docs, it's listed as an "observe" hook — it may not be able to
inject content into the compaction. Need to verify.

**Alternative approach (skill-level):**
- Monitor context usage via token estimation (character count / 4)
- When approaching 80%, present a special checkpoint:
  "Context is getting full. Options: A) Compact now, B) Keep going, C) Save session and start fresh"
- If user picks "Compact", the agent itself writes a summary to a file,
  then reads it back after compaction

**Cursor CLI:**
No compaction mechanism exists. Context is the full conversation history.
When it fills, the session dies. No feasible path without platform support.

**Platform support:**

| Platform | Mechanism | Quality |
|----------|-----------|---------|
| Cursor IDE | `preCompact` hook + skill-level monitoring | Good if preCompact allows injection |
| Cursor CLI | None — no compaction exists | Blocked |
| Claude Code | Native `/compact` + `PreCompact` hook | Already exists |

**Verdict: GO (Cursor IDE).** The `preCompact` hook is the foundation.
Even if it's observe-only, the skill can proactively manage context by
writing state to files before compaction occurs. The 80%-warning checkpoint
is a pure skill-level addition that works today.

---

### 5. Watch Mode (Code-Comment Steering)

**Value:** Very High  
**Feasibility:** F3

**How it works in Aider:**
`--watch-files` monitors repo for `// AI!` comments. Agent processes
instructions embedded in code files.

**Implementation path for durable-request:**

Two approaches:

**Approach A: File watcher hook**
- `afterFileEdit` hook fires after every file edit (by the agent or user)
- But this only fires for agent edits, not manual user edits
- Need `workspaceOpen` hook + a background file watcher

**Approach B: Background watcher script**
- `ai-watch.sh` — runs in background (tmux pane or daemon)
- Uses `inotifywait` (Linux) or `fswatch` (Mac) to watch for file changes
- On change, grep for `// AI!` or `# AI!` patterns
- Extract instruction, write to `~/.durable-request/data/steering-message`
- Steering hook picks it up on next Shell call

This is essentially "watch mode as steering" — the code comment becomes
a steering message. The infrastructure already exists (steering-hook.sh).

**Approach C: Periodic polling in deep-sleep**
- During `deep-sleep`, poll for AI comments in recently modified files
- Wake the agent when found
- Simpler but only works during idle periods

**Constraints:**
- Linux: `inotifywait` from `inotify-tools` package (common, easy to install)
- macOS: `fswatch` (Homebrew installable)
- Must exclude `.git/`, `node_modules/`, etc.
- Pattern matching: `// AI!`, `# AI!`, `/* AI! */`, `<!-- AI! -->`
- Must handle the case where the user writes multiple AI comments
  before the agent processes the first one

**Platform support:**

| Platform | Mechanism | Quality |
|----------|-----------|---------|
| Cursor IDE/CLI | Background watcher + steering pipeline | Good |
| Claude Code | Not needed (has native watch alternatives) | N/A |

**Verdict: GO.** Approach B is the most practical. Reuses the existing
steering infrastructure. The file watcher is a small shell script.
The only new piece is the comment pattern extraction.

---

## Tier 2 Features (High Value)

### 6. `/loop` — Session-Scoped Cron

**Value:** High  
**Feasibility:** F2

**Implementation path:**

The `deep-sleep.sh` pattern already demonstrates blocking Shell loops.
A `/loop` skill would:

```
1. User invokes: /loop 5m "check CI status"
2. Skill writes loop config to ~/.durable-request/data/loop.json
3. loop.sh runs in Shell:
   a. Sleep for interval
   b. Print "[loop] Executing: check CI status"
   c. Return output to agent
   d. Agent processes, presents mini-checkpoint or auto-continues
   e. Back to step a
4. User can /loop stop or /loop list
```

**Key difference from deep-sleep:** Loop executes a prompt each cycle,
not just a keep-alive message. The agent does real work each iteration.

**Challenge:** The Shell call blocks on `loop.sh`, so the agent can't
do other work while the loop runs. Two options:
- **Sequential**: Loop blocks, agent processes each iteration, loop resumes
- **Background**: Loop runs in background, writes output to file, agent
  checks via steering-style injection

Sequential is simpler and matches Claude Code's behavior (loop runs
between turns, not during turns).

**For Cursor IDE:**
The `stop` hook with `followup_message` is actually the better mechanism.
Instead of a blocking Shell loop:
1. Agent does work, reaches end of turn
2. `stop` hook checks if a loop is active
3. If active and interval elapsed, sends `followup_message` with the loop prompt
4. Agent executes the loop prompt as a new turn
5. Repeat

This is cleaner than the Shell-blocking approach.

**Platform support:**

| Platform | Mechanism | Quality |
|----------|-----------|---------|
| Cursor IDE | `stop` hook + `followup_message` | Clean |
| Cursor CLI | `stop` hook (same) or Shell-blocking | Functional |
| Claude Code | Native `/loop` | Already exists |

**Verdict: GO.** Two implementation options, both viable. The `stop` hook
approach is preferred for IDE, Shell-blocking for CLI fallback.

---

### 7. Flow Awareness

**Value:** High  
**Feasibility:** F4-F5

**How it works in Windsurf/Trae:**
Proprietary models track edits, terminal commands, clipboard, file views
in real-time. Agent infers intent without explicit prompting.

**Implementation path:**
This requires deep IDE integration. Windsurf and Trae built this into
their IDE forks. For Cursor:

- `afterFileEdit` hook: can track which files the agent edited
- No hook for: user manual edits, clipboard, file views
- `afterShellExecution` hook: can track terminal commands

The available hooks only cover agent actions, not user actions.
True flow awareness requires access to the IDE's event stream,
which is not exposed to skills or hooks.

**Simplified viable path:**
- Track git diff to see what changed since last checkpoint
- On checkpoint, summarize "Files changed: X, Y, Z" to help the agent
  understand the current state
- This is a poor approximation of flow awareness

**Verdict: SKIP.** Requires IDE-level integration that Cursor doesn't
expose. The available hooks are insufficient for the user's side of the
equation. If Cursor adds user-action hooks in the future, revisit.

---

### 8. Memory Bank (Structured Persistence)

**Value:** High  
**Feasibility:** F2

**How it works in Cline:**
Structured markdown files in `memory-bank/`. Decision records, architecture
state, progress tracking. Read on session start via `sessionStart` hook.

**Implementation path:**

```
memory-bank/
├── decisions.md       # Decisions made, with reasoning and alternatives
├── architecture.md    # Current system state and patterns
├── progress.md        # What's done, what's left
└── constraints.md     # Rules and constraints discovered during work
```

**Implementation:**
1. `sessionStart` hook reads memory bank and injects into context
2. SKILL.md instructs agent to update memory bank after significant decisions
3. `preCompact` hook ensures memory bank content survives compaction
   (by writing it to files, which are re-read post-compaction)
4. `todo-cleanup.sh` extended to also prune old memory entries

**Key advantage over Cline's approach:**
Durable-request sessions are long-lived, so the memory bank accumulates
more context within a single session. Cross-session persistence is a bonus.

**Simplified MVP:**
- Single file: `~/.durable-request/memory/<project-name>.md`
- SKILL.md tells agent to append key decisions
- `sessionStart` hook injects the file content
- No automatic extraction — agent writes naturally

**Platform support:**

| Platform | Mechanism | Quality |
|----------|-----------|---------|
| Cursor IDE | `sessionStart` hook + SKILL.md instructions | Good |
| Cursor CLI | Same hooks | Good |
| All platforms | Skill-level (agent reads file explicitly) | Functional |

**Verdict: GO.** Simple to implement, high value. Start with a single
memory file per project, evolve to structured sub-files later.

---

### 9. Architect Mode (Two-Model Planning)

**Value:** High  
**Feasibility:** F3

**How it works in Aider:**
Reasoning model plans the change. Editor model implements it.
Two separate LLM calls with different prompts.

**Implementation path for durable-request:**

In Cursor, the user selects the model per conversation. The skill can't
change models mid-session. However, subagents (Task tool) CAN use different
models:

```
1. User requests a complex change
2. Main agent (using main model) creates plan
3. Main agent launches subagent (Task tool) with implementation instructions
4. Subagent (potentially using a different/faster model) implements
5. Main agent reviews the result
6. Checkpoint
```

This is already how durable-request's `/enhance-me` works — a subagent
handles a specific sub-task with its own model.

**Alternative: Skill-level architect mode**
- SKILL.md instructs the agent to first plan in a structured format
  (numbered steps, files to modify, tests to run)
- Present the plan at a checkpoint: "Here's my plan. Proceed?"
- Then execute the plan step by step

This doesn't use two models but achieves the same separation of concerns.

**Platform support:**

| Platform | Mechanism | Quality |
|----------|-----------|---------|
| Cursor IDE | Subagent with different model (if user specifies) | Moderate |
| All platforms | Skill-level plan-then-execute | Good |

**Verdict: GO (skill-level).** The plan-then-execute pattern is a pure
SKILL.md addition. The two-model variant depends on subagent model selection
which the user must configure. Start with skill-level planning, add subagent
orchestration as an enhancement.

---

### 10. Auto Lint/Test Fix Loops

**Value:** High  
**Feasibility:** F1

**How it works in Aider:**
After generating code, automatically runs linter, detects errors,
re-prompts model to fix.

**Implementation path:**
This is already largely supported by Cursor's auto-run with test allowlists.
The skill enhancement would be:

SKILL.md addition:
```
After making code changes, if the project has a test suite or linter configured:
1. Run the relevant test/lint command
2. If failures are found, fix them before presenting the checkpoint
3. Only checkpoint when tests pass (or after N fix attempts)
```

This is a pure instruction-level change. No new scripts needed.

**For deeper integration:**
- `afterFileEdit` hook could auto-run linter
- Feed lint errors back into agent context
- But this is what Cursor's built-in auto-fix already does

**Verdict: GO.** Add to SKILL.md as a best-practice instruction.
No new infrastructure needed.

---

### 11. Named Checkpoints / Snapshots

**Value:** High  
**Feasibility:** F2

**Implementation path:**

```
/snapshot "pre-refactor"
  → git stash push -m "durable-request-snapshot: pre-refactor"
  → Record in ~/.durable-request/data/snapshots.json

/revert "pre-refactor"
  → Find matching stash
  → git stash pop
  → Update snapshots.json

/snapshots
  → List all named snapshots with timestamps
```

Alternative using git tags:
```
/snapshot "pre-refactor"
  → git tag "durable-snapshot/pre-refactor"

/revert "pre-refactor"
  → git checkout "durable-snapshot/pre-refactor" -- .
```

Git tags are simpler and don't conflict with user's stash usage.

**Files to create:**
- `snapshot.sh` — create/list/revert snapshots
- SKILL.md update with `/snapshot` and `/revert` instructions

**Verdict: GO.** Simple git operations wrapped in a script. Low risk.

---

### 12. Worktree Isolation

**Value:** High  
**Feasibility:** F3

**Implementation path:**

```
/worktree "feature-x"
  → git worktree add /tmp/durable-worktrees/feature-x -b feature-x
  → Symlink node_modules, .env, etc.
  → Tell agent to work in the worktree path
```

**Challenge:** The agent's working directory is controlled by the IDE.
In Cursor IDE, the workspace root is fixed. Changing it requires
Cursor's `move_agent_to_root` MCP tool (from cursor-app-control).

**For CLI:**
- Straightforward — change directory in Shell calls
- The agent can `cd /tmp/durable-worktrees/feature-x` and work there

**For IDE:**
- Use `move_agent_to_root` from cursor-app-control MCP to move workspace
- Or have the agent prefix all file paths with the worktree path
  (error-prone, not recommended)

**Platform support:**

| Platform | Mechanism | Quality |
|----------|-----------|---------|
| Cursor IDE | `move_agent_to_root` MCP | Works but changes workspace |
| Cursor CLI | `cd` in Shell | Works naturally |

**Verdict: GO (CLI), MODERATE (IDE).** CLI implementation is straightforward.
IDE implementation works but requires cursor-app-control MCP and changes
the visible workspace, which may confuse the user.

---

### 13. Auto-Run Allowlists

**Value:** High  
**Feasibility:** F1

**Implementation path:**
This is already a Cursor setting. The skill just needs to tell users
to enable it. Add to SKILL.md and install.md:

```
For maximum durable session throughput, enable auto-run in Cursor Settings:
- Auto-run: ON
- Allowlist: npm test, npm run lint, pytest, make test, etc.
```

No code needed — just documentation.

**Verdict: GO.** Documentation-only change.

---

### 14. Cross-Session Resume

**Value:** High  
**Feasibility:** F3

**Implementation path:**

```
sessionEnd hook → writes session state to file:
  ~/.durable-request/sessions/<project>-<timestamp>.json
  {
    "project": "/path/to/project",
    "last_task": "Implementing user auth",
    "completed_tasks": ["Added login form", "Set up JWT"],
    "pending_tasks": ["Add password reset", "Write tests"],
    "key_decisions": ["Using bcrypt for hashing", "JWT expires in 1h"],
    "git_branch": "feature/auth",
    "git_diff_summary": "3 files changed, 150 insertions"
  }

sessionStart hook → reads latest session state:
  If a recent session file exists for this project:
  Inject: "[SESSION RESUME] Continuing from previous session: ..."
```

**Challenge:** The `sessionEnd` hook fires when the conversation ends.
At that point, the agent is done — it can't write anything. The hook
script itself must extract the state from available sources:
- Read TodoWrite state from... where? TodoWrite data isn't accessible to hooks.
- Read git status/diff (available)
- Read recent file changes (available)

**Alternative: Proactive state saving**
- SKILL.md instructs the agent to write state to a file periodically
  (e.g., after each checkpoint)
- `sessionEnd` hook reads the agent-written state file
- `sessionStart` hook injects the state file

This is more reliable because the agent writes the state while it has
full context, not the hook trying to reconstruct it.

**Verdict: GO.** Combine agent-written state files with sessionStart/End
hooks. The state file approach is robust and platform-independent.

---

### 15. Self-Review Before Delivery

**Value:** High  
**Feasibility:** F2

**Implementation path:**
Add to SKILL.md:

```
Before presenting a checkpoint after code changes:
1. Review your own changes (git diff)
2. Check for: missing error handling, unused imports, inconsistent naming,
   missing tests, security issues
3. Fix any issues found
4. Only then present the checkpoint
```

For deeper integration, launch a subagent with "review these changes"
prompt and incorporate its feedback before checkpointing.

**Verdict: GO.** SKILL.md instruction for basic version.
Subagent-based review for enhanced version.

---

## Tier 3 Features (Nice to Have)

### 16. `/schedule` — Durable Cron

**Feasibility:** F5  
**Verdict: SKIP.** Crosses session boundaries, triggers new requests.
Not compatible with the "maximize work per request" philosophy.

### 17. Voice Input

**Feasibility:** F5  
**Verdict: SKIP.** Requires speech-to-text infrastructure (Whisper).
Out of scope for a skill suite. Users can use OS-level dictation.

### 18. Parallel Subagents (beyond current Task tool)

**Feasibility:** F1  
**Verdict: ALREADY EXISTS.** Cursor's Task tool already supports parallel
subagents. SKILL.md can add best practices for when to parallelize.

### 19. Custom Agents

**Feasibility:** F2  
**Verdict: DEFER.** The skills system is the durable-request equivalent
of custom agents. Each skill IS a custom agent configuration.

### 20. Sandbox Tiers

**Feasibility:** F5  
**Verdict: SKIP.** Platform-level infrastructure, not a skill concern.

---

## Summary Matrix

| # | Feature | Value | Feasibility | Verdict | Priority |
|---|---------|-------|-------------|---------|----------|
| 1 | `/goal` — Autonomous goal loop | Very High | F2-F3 | **GO** | P0 |
| 2 | Channels — Event-driven | Very High | F4-F5 | DEFER | — |
| 3 | Kanban multi-agent | Very High | F4 | FUTURE | — |
| 4 | Context compaction | Very High | F2 (IDE) | **GO** | P1 |
| 5 | Watch mode steering | Very High | F3 | **GO** | P2 |
| 6 | `/loop` — Session cron | High | F2 | **GO** | P1 |
| 7 | Flow Awareness | High | F4-F5 | SKIP | — |
| 8 | Memory Bank | High | F2 | **GO** | P1 |
| 9 | Architect mode | High | F3 | **GO** | P2 |
| 10 | Auto lint/test fix | High | F1 | **GO** | P0 |
| 11 | Named snapshots | High | F2 | **GO** | P1 |
| 12 | Worktree isolation | High | F3 | **GO** | P2 |
| 13 | Auto-run allowlists | High | F1 | **GO** | P0 |
| 14 | Cross-session resume | High | F3 | **GO** | P2 |
| 15 | Self-review | High | F2 | **GO** | P1 |
| 16 | `/schedule` | Medium | F5 | SKIP | — |
| 17 | Voice input | Medium | F5 | SKIP | — |
| 18 | Parallel subagents | High | F1 | EXISTS | — |
| 19 | Custom agents | Medium-High | F2 | DEFER | — |
| 20 | Sandbox tiers | Medium | F5 | SKIP | — |

---

## Recommended Implementation Order

### Phase 0 — Quick Wins (F1, days of effort)

| Feature | Effort | What to do |
|---------|--------|-----------|
| Auto lint/test fix (#10) | 1 day | Add SKILL.md instructions |
| Auto-run allowlists (#13) | 1 day | Add install.md + SKILL.md documentation |

### Phase 1 — Core Extensions (F2, 1-2 weeks each)

| Feature | Effort | What to do |
|---------|--------|-----------|
| `/goal` (#1) | 2 weeks | `stop` hook + evaluator + SKILL.md |
| `/loop` (#6) | 1 week | `stop` hook + interval logic |
| Memory Bank (#8) | 1 week | sessionStart hook + state files |
| Named snapshots (#11) | 3 days | `snapshot.sh` + git tags |
| Self-review (#15) | 3 days | SKILL.md + optional subagent |
| Context awareness (#4) | 1 week | `preCompact` hook + 80% warning |

### Phase 2 — Advanced Features (F3, 2-4 weeks each)

| Feature | Effort | What to do |
|---------|--------|-----------|
| Watch mode (#5) | 2 weeks | File watcher + steering pipeline |
| Architect mode (#9) | 2 weeks | Plan-execute skill + subagent |
| Worktree isolation (#12) | 2 weeks | Script + MCP integration |
| Cross-session resume (#14) | 3 weeks | sessionEnd/Start hooks + state files |

### Deferred / Future

| Feature | Reason |
|---------|--------|
| Channels (#2) | Wait for Cursor platform support |
| Kanban (#3) | Separate product scope |
| Flow Awareness (#7) | Requires IDE-level integration |
