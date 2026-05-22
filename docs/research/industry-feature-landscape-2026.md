# Coding Agent Industry Feature Landscape (May 2026)

> **Purpose:** Identify features across the coding agent ecosystem that are valuable for
> request-based pricing users and could be ported to the durable-request skill suite.
> This document evaluates **value only** — feasibility is out of scope.

---

## 1. Feature Catalog by Source

### 1.1 Claude Code

| Feature | Description | Value for request-pricing users |
|---------|-------------|-------------------------------|
| **`/goal`** | Persistent completion condition — a fast evaluator model checks after every turn if the condition is met. Agent auto-continues turns until goal achieved. | **Very High.** Eliminates per-turn user interaction entirely for well-defined tasks. The user sets a verifiable endpoint and walks away. Pairs with durable-request: `/goal` handles the autonomous loop, durable-request handles the "what next" when the goal clears. |
| **`/loop`** | Session-scoped cron scheduler — runs a prompt on a fixed or dynamic interval. Up to 50 concurrent tasks, auto-expires after 72h. | **High.** Enables background polling (CI status, deploy health, PR reviews) within a single session. The request stays alive and productive even when the primary task is idle. |
| **`/schedule`** | Durable scheduled tasks that persist across sessions (desktop/cloud). Min interval 1 hour. | **Medium.** Useful but crosses session boundaries — likely triggers new requests. Value is in the mental model: user can delegate future work upfront. |
| **`/compact`** | Manual context compaction with custom preservation instructions. Auto-compact at ~95% token usage. | **High.** Long durable sessions will eventually hit context limits. Controlled compaction extends session lifetime dramatically. Without it, durable-request sessions have a hard ceiling. |
| **Auto Memory** | `MEMORY.md` — persistent memory across sessions, auto-loaded on startup, first 200 lines survive compaction. | **Medium-High.** Enables cross-session learning. A user's preferences, project patterns, and workflow habits persist without re-explaining. |
| **Channels** | MCP-based event push — CI results, chat messages (Telegram/Discord/iMessage), webhooks pushed into running session. | **Very High.** Event-driven reactions within a durable session. Instead of polling CI, CI pushes failures to the agent. The durable session becomes a reactive hub, not just a task executor. |
| **`PreCompact` hook** | Hook that fires before context compaction — can inject instructions into the summary prompt. | **High.** Allows durable-request to preserve its own protocol state (checkpoint intent, steering state, todo list) across compaction events. |
| **Stop hook** | Fires after every turn to evaluate whether the agent should continue. Can run scripts or prompts. | **High.** This IS the underlying mechanism for `/goal`. A skill-level implementation could add goal-like behavior to any platform. |

### 1.2 OpenAI Codex CLI

| Feature | Description | Value for request-pricing users |
|---------|-------------|-------------------------------|
| **`/goal`** | Persistent objective with lifecycle (pursuing/paused/achieved/budget-limited). Auto-continues across turns. Budget controls (token + wall-clock). | **Very High.** Same value as Claude Code's `/goal` but with explicit budget guardrails — critical for cost-conscious users. Budget-limited state triggers graceful wrap-up instead of abrupt stop. |
| **Parallel subagents** | Spawn up to N specialized agents (default 6, configurable) that work in parallel. CSV batch processing via `spawn_agents_on_csv`. | **High.** Within a single request, parallelize independent subtasks. The orchestrator agent stays alive while subagents execute, multiplying throughput per request. |
| **`/agent` thread management** | Switch between active agent threads, inspect running subagent work, steer or stop individual agents. | **Medium-High.** Visibility and control over parallel work within a single session. |
| **Auto-review mode** | A separate model auto-approves low-risk actions, only interrupting for high-risk ones. | **High.** Reduces friction in durable sessions — user doesn't have to approve every file write or shell command. More work gets done per interaction cycle. |
| **Permission profiles** | Built-in defaults for sandbox policy + per-session overrides. Sandbox policy inherited by subagents. | **Medium.** Safety without friction. Important for `/goal`-like autonomous loops. |

### 1.3 Cursor IDE

| Feature | Description | Value for request-pricing users |
|---------|-------------|-------------------------------|
| **Background/Cloud Agent** | Runs tasks on isolated cloud VMs. Creates own branch, opens PR when done. Works while user is offline. | **Medium.** Powerful but likely triggers separate request. Value: user can dispatch background work while primary durable session handles interactive work. |
| **`/worktree`** | Each agent gets its own git worktree — full isolation from main workspace. | **High.** Long durable sessions accumulate changes. Worktree isolation prevents interference between parallel tasks within the same request. |
| **`/best-of-n`** | Run N agents on the same task with different models/strategies, compare results. | **Medium.** Useful for optimization tasks but token-expensive. Value is in quality, not quantity per request. |
| **`/multitask`** | Decompose one prompt into parallel subagent tasks. | **High.** Direct multiplier on work-per-request. One prompt spawns N parallel tasks, all within the same request. |
| **Agents Window** | Multi-pane view — multiple agents with their own mode, model, and worktree, running side by side. | **High.** Visual management of parallel durable sessions. Each pane is its own durable loop. |
| **Hooks (full lifecycle)** | `sessionStart/End`, `preToolUse/postToolUse`, `subagentStart/Stop`, `beforeShellExecution`, `preCompact`, `stop`, `afterAgentResponse`. | **Very High.** The hook surface is what makes durable-request's steering work. More hooks = more control points for the skill suite. `stop` hook is particularly valuable for goal-like behavior. |
| **Auto-run allowlists** | Agent auto-runs approved terminal commands (e.g., `npm test`) without user approval. | **High.** Removes friction in durable sessions. Agent writes code, runs tests, iterates — all without user clicking "approve." |

### 1.4 GitHub Copilot

| Feature | Description | Value for request-pricing users |
|---------|-------------|-------------------------------|
| **Cloud Agent** | Background agent that creates implementation plan, makes changes, self-reviews with Copilot code review, runs security scanning, opens PR. | **Medium.** Similar to Cursor's background agent — separate request, but user can dispatch while staying in primary session. |
| **Self-review before PR** | Agent reviews its own changes using Copilot code review before opening PR. | **High.** Quality gate within the same session. The agent iterates on its own work before presenting it — fewer "go back and fix" cycles. |
| **Custom agents** | `.github/agents/` — define specialized agents with custom tools, instructions, and MCP servers. | **Medium-High.** Specialized agents for specific task types (performance optimizer, security auditor) that can be invoked within a durable session. |
| **CLI agent with worktree/workspace isolation** | Choose between worktree (isolated) and workspace (direct) modes per session. | **High.** Same worktree isolation value as Cursor. |
| **Ask question tool in agent mode** | Agent can ask user for clarification mid-task. | **High.** This IS durable-request's core concept, but native. Validates the approach. |

### 1.5 Aider

| Feature | Description | Value for request-pricing users |
|---------|-------------|-------------------------------|
| **Watch mode (`--watch-files`)** | Monitor repo for `AI!` / `AI?` comments in any file. Agent auto-processes instructions embedded in code comments. | **Very High.** The user writes instructions *in their IDE* as code comments. The agent picks them up without context-switching. This is a different steering paradigm — the code itself becomes the instruction channel. |
| **Architect mode** | Two-model workflow: reasoning model plans, editor model implements. | **High.** Better quality per request — the planning model catches issues the editor model would miss. More first-time-right results = fewer correction cycles in the durable loop. |
| **Automatic atomic git commits** | Every change is auto-committed as an atomic unit. `/undo` reverts cleanly. | **High.** Safety net for long durable sessions. If the agent makes a bad change 20 tasks deep, you can undo just that change without losing everything. |
| **Auto lint/test fix loops** | After generating code, automatically runs linter, detects errors, re-prompts model to fix. Same for test failures. | **High.** Self-healing within each task cycle. The agent doesn't present broken code at the checkpoint — it fixes it first. |
| **Voice input (`/voice`)** | Whisper-based speech-to-text for instructions. | **Medium.** Accessibility and convenience. Reduces friction for quick instructions during a durable session. |

### 1.6 Windsurf (Cascade)

| Feature | Description | Value for request-pricing users |
|---------|-------------|-------------------------------|
| **Flow Awareness** | Tracks edits, terminal commands, clipboard, file views in real-time. Agent infers user intent without explicit prompting. | **Very High.** The agent doesn't need to be told what you're working on — it already knows. In a durable session, this eliminates re-context-setting between tasks. "Continue my work" becomes a valid prompt. |
| **Auto-generated Memories** | Agent autonomously creates and stores memories per workspace. Loaded when relevant, persisted across sessions. | **High.** The durable session builds up institutional knowledge that carries forward. User preferences, project patterns, and past decisions inform future work. |
| **Workflows (slash commands)** | User-defined reusable prompt templates for multi-step tasks. Invoked via `/workflow-name`. | **Medium-High.** Composable task templates within a durable session. Instead of explaining a deploy process each time, `/deploy` runs the full workflow. |
| **Named checkpoints/snapshots** | Create named snapshots of project state during conversation. Revert to any snapshot. | **High.** Critical safety net for long durable sessions. Bookmark known-good states so adventurous experimentation is risk-free. |
| **Devin cloud agent integration** | Delegate to Devin (cloud agent) from Cascade, manage in Agent Command Center. | **Medium.** Cross-agent delegation within the same workflow surface. |
| **Built-in Todo/plan tracking** | Cascade auto-creates todo lists for complex tasks, updates as it learns. | **Medium.** Similar to durable-request's TodoWrite but native. Validates the approach. |

### 1.7 Cline

| Feature | Description | Value for request-pricing users |
|---------|-------------|-------------------------------|
| **Plan & Act mode** | Separate planning (read-only exploration) from execution. Align on strategy before making changes. | **High.** Prevents wasted work in durable sessions. Plan first, execute once. No "oops, wrong approach, let me redo" cycles that consume the session. |
| **Memory Bank** | Structured markdown files (`memory-bank/`) that the agent reads at start of each task. Decision records, architecture state, progress tracking. | **Very High.** Structured, queryable persistence. Not prose summaries — actual records with reasoning and alternatives. Survives compaction, session restarts, and agent handoffs. |
| **Kanban board** | Multi-agent task board — each card is a live agent in its own worktree. Dependency chains auto-start. Auto-commit. Monitor hundreds of agents at a glance. | **Very High.** Project-level orchestration of durable sessions. Not "one session, many tasks" but "many sessions, coordinated tasks." The Kanban is the meta-durable-loop. |
| **Agent teams** | Coordinator + specialist agents sharing a task board, inter-agent mailbox, and mission log. | **High.** Specialized agents for different task types, orchestrated by a coordinator. The coordinator runs the durable loop, specialists handle specific work. |
| **Checkpoints with diff review** | Every step tracked with checkpoint. See diff between any two points. One-click undo. | **High.** Same value as Windsurf's named checkpoints. |
| **SDK (programmatic API)** | Run Cline agents programmatically — scripts, CI, cron, custom integrations. | **Medium-High.** Enables durable-request-like behavior in automated pipelines, not just interactive sessions. |

### 1.8 Trae IDE

| Feature | Description | Value for request-pricing users |
|---------|-------------|-------------------------------|
| **SOLO autonomous mode** | Full-speed autonomous execution. Plans, executes, coordinates sub-agents. Multiple agents on different tasks simultaneously. | **High.** Autonomous work without per-step approval. More throughput per request. |
| **Real-time action awareness** | Agent tracks editor actions, terminal activity, file views — responds to "continue my work" naturally. | **High.** Same concept as Windsurf's Flow Awareness. Reduces re-prompting overhead in durable sessions. |
| **Skills (progressive disclosure)** | Skills loaded on-demand by description match. Instructions stay out of context until needed. | **Medium-High.** Token-efficient skill system. Important for long sessions where context budget matters. |

### 1.9 Gemini CLI

| Feature | Description | Value for request-pricing users |
|---------|-------------|-------------------------------|
| **Plan mode with `ask_user`** | Read-only planning phase where agent explores, asks clarifying questions, produces strategy. | **High.** Safe exploration before committing to changes. Combined with durable-request, the checkpoint after planning could confirm the approach. |
| **Subagents with separate context** | Each subagent gets its own context window — main session stays lean. | **High.** Context budget management. Long durable sessions can offload heavy reads to subagents and keep the main context clean. |
| **Conductor** | Orchestrator for multi-step development tracks. Guides through complex migrations or features. | **Medium-High.** Project-level orchestration within a durable session. |
| **Sandbox (gVisor, Bubblewrap, LXC)** | Multiple sandboxing tiers for safe autonomous execution. | **Medium.** Safety infrastructure for autonomous modes like `/goal`. |

### 1.10 Cross-Agent Tools

| Tool | Description | Value for request-pricing users |
|------|-------------|-------------------------------|
| **sessionmark** | Save and resume AI coding sessions across agents and machines. LPIC+CSV encoding (~40 tokens). Auto-injection into agent config files. | **Very High.** When a durable session ends (timeout, crash, context full), sessionmark preserves the state. The next session (even on a different agent) picks up where the last left off. True cross-session durability. |
| **agent-recall-ai** | Structured session checkpointing — decisions stored as queryable records, not prose. ~270 token resume prompt. Survives compaction. | **Very High.** Unlike `/compact` which loses structure, agent-recall preserves decisions, constraints, and alternatives. Perfect complement to durable-request for ultra-long sessions. |
| **magic-context** | Background historian model compresses older conversation. Cache-aware drops. Dreamer mode for offline context building. | **High.** Active context management that keeps the session running longer without degradation. |
| **`/goal` MCP server** | Cross-platform goal persistence via MCP (works in Claude Code, Cursor, OpenCode). Auto-continuation via hooks in Claude Code. | **Very High.** The `/goal` concept isn't locked to one platform. This MCP server brings it to any agent — including Cursor. |

---

## 2. Value-Ranked Feature Shortlist

Features ranked by value for request-based pricing users, scored on:
- **Request efficiency:** How much more work per request?
- **Session extension:** Does it keep the session alive longer?
- **Quality per cycle:** Better results on each task iteration?
- **User friction reduction:** Fewer interruptions and re-explanations?

### Tier 1 — Transformative (redefine what a single request can accomplish)

| # | Feature | Source | Why Transformative |
|---|---------|--------|--------------------|
| 1 | **`/goal` — Autonomous goal loop** | Claude Code, Codex, MCP | The agent works for hours on a single objective without user interaction. One request = one project-scale outcome. Budget controls prevent runaway cost. |
| 2 | **Channels — Event-driven reactions** | Claude Code | The durable session becomes reactive. CI failures, chat messages, webhooks flow in. One request handles an entire development cycle: code → push → CI fails → agent fixes → push again. |
| 3 | **Kanban multi-agent orchestration** | Cline | Project-level parallelization. Not one agent doing many tasks, but many agents doing many tasks, all coordinated from one surface. |
| 4 | **Context compaction with preservation** | Claude Code, magic-context | Extends the theoretical maximum session length from "context window" to "unlimited." The session never has to end because of token limits. |
| 5 | **Watch mode (code-comment steering)** | Aider | A different steering paradigm. The user writes `// AI! add error handling here` in their editor. The agent picks it up. No context switch, no chat window. |

### Tier 2 — High Value (significant improvement to existing workflow)

| # | Feature | Source | Why High Value |
|---|---------|--------|---------------|
| 6 | **`/loop` — Session-scoped cron** | Claude Code | Background polling within the durable session. Monitor CI, babysit PRs, check deploys — all while the primary task continues. |
| 7 | **Flow Awareness** | Windsurf, Trae | Agent knows what you're doing without being told. Reduces prompt overhead in multi-task durable sessions. |
| 8 | **Memory Bank (structured persistence)** | Cline, agent-recall-ai | Decisions, constraints, and progress survive session boundaries and compaction. Better than prose summaries. |
| 9 | **Architect mode (two-model planning)** | Aider, Cline (Plan & Act) | More correct on first attempt = fewer "fix this" cycles in the durable loop. |
| 10 | **Auto lint/test fix loops** | Aider, Cline | Agent self-heals before presenting results. Each checkpoint shows working code, not broken code. |
| 11 | **Named checkpoints/snapshots** | Windsurf, Cline | Safety net for adventurous durable sessions. Bookmark good states, experiment freely. |
| 12 | **Worktree isolation** | Cursor, Copilot, Cline | Parallel tasks within a durable session without interference. |
| 13 | **Auto-run allowlists** | Cursor, Codex | Removes "approve this command?" friction. The agent runs `npm test` 50 times without asking. |
| 14 | **Cross-session resume** | sessionmark, agent-recall-ai | When a durable session *does* end (crash, timeout), recovery is automatic. |
| 15 | **Self-review before delivery** | Copilot | Quality gate — agent reviews its own work before presenting. Fewer wasted checkpoint cycles. |

### Tier 3 — Nice to Have (incremental improvement)

| # | Feature | Source | Why Nice to Have |
|---|---------|--------|-----------------|
| 16 | **`/schedule` — Durable cron** | Claude Code | Persistent scheduling across sessions. Less critical if `/loop` covers in-session needs. |
| 17 | **Voice input** | Aider | Convenience, not transformation. |
| 18 | **Parallel subagents** | Codex, Gemini | Already available via Cursor's Task tool. Value is in orchestration, not the primitive. |
| 19 | **Custom agents** | Copilot, Gemini | Specialized agents per task type. Useful but requires significant setup. |
| 20 | **Sandbox tiers** | Gemini, Codex | Safety for autonomous modes. Infrastructure, not user-facing value. |

---

## 3. Integration Analysis with durable-request

### Naturally Compatible Features

These features align with durable-request's "keep the session alive, do more per request" philosophy and could integrate as new skills or extensions:

| Feature | Integration Path | Compatibility |
|---------|-----------------|---------------|
| `/goal` | New `/goal` skill that wraps the durable loop with a stop-condition evaluator. Instead of checkpoint → user picks → work → checkpoint, it becomes: set goal → work → evaluate → work → ... → goal met → checkpoint. | Natural extension. `/goal` handles the autonomous phase; durable-request handles the "what next" when the goal clears. |
| `/loop` | New `/loop` skill that runs a prompt on an interval within the durable session. Uses Shell + sleep for CLI; uses Cursor hooks for IDE. | Natural fit. The durable session already stays alive — `/loop` adds recurring work within it. |
| Context compaction | New `/compact` checkpoint type. When context is nearing limits, present a checkpoint that says "Context is 80% full. Compact now?" with options to preserve specific information. | Defensive mechanism. Prevents the durable session from dying to context limits. |
| Memory Bank | New `/memory` skill that maintains structured decision records. Auto-persisted, survives compaction. Read on session start. | Complements existing TodoWrite. Todos track *what to do*; memory tracks *what was decided and why*. |
| Watch mode | Extend steering to watch for `// AI!` comments in files. The preToolUse hook could check for AI comments in recently modified files. | Alternative steering channel. Instead of `steer "message"`, user writes `// AI! message` in their code. |
| Named checkpoints | Extend TodoWrite with snapshot capability. `/snapshot "pre-refactor"` saves current git state + todo list. `/revert "pre-refactor"` restores. | Safety net for the durable loop. Especially valuable for multi-step tasks. |
| Cross-session resume | New `reinstate` skill that writes structured state on session end (via hook) and reads it on session start. | Graceful degradation. When the durable session ends despite best efforts, recovery is automatic. |

### Requires Architecture Change

These features would need new infrastructure beyond the current skill+script model:

| Feature | What's Needed | Difficulty |
|---------|--------------|------------|
| Channels (event push) | MCP server implementation + webhook endpoint | Significant — needs a running server process |
| Kanban orchestration | Web UI + multi-agent coordination | Large project — but could start as a CLI task board |
| Flow Awareness | File watcher + editor activity monitor | Needs IDE integration beyond hooks |
| Parallel agents with worktrees | Git worktree management + agent lifecycle | Moderate — worktree logic is scriptable, lifecycle needs hooks |

---

## 4. Recommended Exploration Priorities

Based on value-to-effort ratio and compatibility with the current durable-request architecture:

### Immediate (can prototype with current infrastructure)

1. **`/goal`** — Implement as a Stop hook + evaluator model. The durable loop already exists; add a "keep going until X" mode.
2. **Context awareness** — Add a context usage monitor. When approaching limits, auto-trigger a checkpoint with compaction options.
3. **`/loop`** — Implement as a background Shell + sleep loop within the durable session. Already have `deep-sleep.sh` as a pattern.
4. **Named snapshots** — Extend checkpoint with `git stash`-like save/restore points.

### Short-term (needs some new infrastructure)

5. **Memory Bank** — Structured `.durable-request/memory/` files that survive compaction and session boundaries.
6. **Cross-session resume** — Session state serialization via hooks. Write on `sessionEnd`, read on `sessionStart`.
7. **Watch mode steering** — Extend `steering-hook.sh` to watch for AI comments in files.

### Medium-term (needs significant new work)

8. **Channels integration** — Build an MCP server that bridges CI/chat events into the durable session.
9. **Multi-agent coordination** — Task board (even CLI-based) for orchestrating parallel durable sessions.
10. **Architect mode** — Two-phase workflow skill: plan (cheap model) → execute (capable model).

---

## 5. Key Insight

The industry is converging on a shared primitives stack:

```
Layer 4: Orchestration     Kanban, /multitask, agent teams
Layer 3: Autonomy          /goal, auto-approve, stop hooks
Layer 2: Persistence       Memory, checkpoints, cross-session resume
Layer 1: Session Control   Durable loop, steering, deep-sleep  ← durable-request is here
Layer 0: Platform          Hooks, MCP, sandboxing
```

durable-request currently owns **Layer 1** thoroughly. The biggest growth opportunity
is moving up to **Layer 2 (Persistence)** and **Layer 3 (Autonomy)** while maintaining
the "more work per request" philosophy. The `/goal` feature is the single highest-value
addition because it directly multiplies work-per-request without requiring user
interaction for each task cycle.
