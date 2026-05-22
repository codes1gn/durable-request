# durable-request PRD (Product Requirements Document)

> **Author:** Heng Shi  
> **Version:** 1.2.0  
> **Last updated:** 2026-05-22  
> **Target users:** Request-based pricing users (Cursor, Claude, Copilot, etc.)

---

## 1. Product Vision and Design Philosophy

### Core Problem

On request-based pricing plans (Cursor, Claude, Copilot, etc.), each agent request is a paid interaction. Without intervention, AI agents follow a **single-task-then-stop** pattern:

```
Request 1: "Add auth"    → Agent: "Done." (silent exit)
Request 2: "Add tests"   → Agent: "Done." (silent exit)
Request 3: "Rate limit"  → Agent: "Done." (silent exit)
= 3 requests, 3 tasks
```

The user pays for N requests to complete N tasks, losing context between each request.

### Design Philosophy: "Never End Silently"

durable-request inverts the agent lifecycle from **fire-and-forget** to **durable loop**:

```
Request 1: "Add auth"
  → Agent: "Done. What's next?"
  → User: "Add tests"
  → Agent: "Done. What's next?"
  → User: "Rate limit"
  → Agent: "Done. What's next?"
  → User: "Done"
= 1 request, 3 tasks
```

**Key architectural insight**: The agent never terminates on its own — it always presents an interactive checkpoint that blocks the current turn without ending the request. The user stays in the same session, preserving context and amortizing the request cost across multiple tasks.

### Three Design Pillars

1. **Blocking > Conversational**: Use platform-native blocking tools (`AskQuestion`, Shell checkpoint) rather than text-based prompts. Blocking tools guarantee the loop stays alive.
2. **Structural Reinforcement > Prose Instructions**: `TodoWrite` creates an unfulfilled obligation (`in_progress` item) that structurally prevents the agent from ending silently, even when the LLM "forgets" the skill instructions.
3. **Platform Adaptation > One-Size-Fits-All**: Each platform has its own optimal checkpoint mechanism. The skill detects the environment and uses the best available tool, with explicit fallback hierarchy.

---

## 2. Feature Decomposition

### F1 — Checkpoint After Task Completion (Core)

| Attribute | Detail |
|-----------|--------|
| **What** | Agent calls `AskQuestion` / `checkpoint.sh` / fallback after ANY completed task |
| **Why** | The fundamental "never end silently" behavior |
| **Mechanism** | Platform detection → appropriate blocking tool |
| **Evidence** | 100% activation rate across 170 A/B experiments (vs 0–5% in control) |

### F2 — TodoWrite + Checkpoint Reinforcement (Structural Anchor)

| Attribute | Detail |
|-----------|--------|
| **What** | Before every checkpoint, agent writes `{id: "durable-checkpoint", status: "in_progress"}` to `TodoWrite` |
| **Why** | Double-lock pattern — even if the checkpoint tool fails, the `in_progress` todo prevents silent completion |
| **Philosophy** | Trust structure over LLM memory. An unfinished todo is an obligation the agent cannot ignore |

### F3 — Context-Adaptive Options (A/B/C/D Format)

| Attribute | Detail |
|-----------|--------|
| **What** | 4 options where A/B/C are AI-generated most-likely-next-actions, D is always `/deep-sleep` |
| **Why** | Reduces friction — user picks instead of types. AI predicts intent so the user often just clicks |
| **Philosophy** | The checkpoint should accelerate the user, not slow them down |

### F4 — Task Summary in Prompt

| Attribute | Detail |
|-----------|--------|
| **What** | 1–2 sentence summary of completed work embedded in the checkpoint prompt |
| **Why** | User gets instant status without reading back through the conversation |

### F5 — Multi-Step Checkpoint Loop

| Attribute | Detail |
|-----------|--------|
| **What** | After each significant step in a multi-step task, present a brief checkpoint |
| **Why** | "Significant step" checkpoints (file changes, output generation, >30s work) give the user control without micro-managing |

### F6 — Durable Loop (Continue Until Done)

| Attribute | Detail |
|-----------|--------|
| **What** | The full loop: work → checkpoint → user responds → work → checkpoint → ... → "Done" |
| **Why** | This IS the product — one request, unlimited tasks, full context preservation |

### F7 — Subagent Conversational Fallback

| Attribute | Detail |
|-----------|--------|
| **What** | Subagents (launched via Task tool) lack `AskQuestion` access, so they use numbered text options |
| **Why** | Graceful degradation — the protocol applies even in restricted environments |

### F8/F8a/F8b — In-Continuation Steering

| Attribute | Detail |
|-----------|--------|
| **What** | User sends mid-task instructions (via CLI `steer`, tmux popup, or VSCode extension) without interrupting the agent |
| **F8a** | Steering message appears in Shell tool output via `preToolUse` hook |
| **F8b** | Agent acknowledges steering with a mandatory bounding box format |
| **Why** | The user shouldn't have to wait for a checkpoint to redirect the agent |
| **Philosophy** | Asynchronous communication within a synchronous request |

### F9 — Todo Cleanup at >20 Items

| Attribute | Detail |
|-----------|--------|
| **What** | Automatic cleanup of completed todos when list exceeds 20 items |
| **Why** | Long durable sessions accumulate todos; cleanup prevents context pollution |
| **Mechanism** | `todo-cleanup.sh` preserves active items, removes oldest completed, never deletes `durable-checkpoint` |

### F10 — No Silent Completion (Meta-Verification)

| Attribute | Detail |
|-----------|--------|
| **What** | The overarching guarantee that no task ends without user interaction |
| **Why** | This is the quality gate — every other feature serves this guarantee |

---

## 3. Auxiliary Features (Beyond Core Skill)

### /deep-sleep — Agent Keep-Alive Mode

| Attribute | Detail |
|-----------|--------|
| **Trigger** | User selects D at checkpoint, says "brb", or "back in X min" |
| **What** | `deep-sleep.sh` enters a blocking polling loop, printing keep-alive messages every 60s |
| **Why** | Prevents request timeout when user is temporarily away |
| **Wake** | User runs `touch ~/.cursor/skills/durable-request/.deep-sleep-wake` |
| **Philosophy** | The request should survive user absence, not just task completion |

### /enhance-me — Prompt Enhancer Router

| Attribute | Detail |
|-----------|--------|
| **What** | Launches a subagent to enhance the user's raw prompt using model-specific best practices (Claude vs GPT/Codex), displays the enhanced prompt, then executes it |
| **Model routing** | Default Claude; GPT only when explicitly specified |
| **Why** | Better prompts = better results within the same request. The enhancement happens inside the same request via subagent — zero extra request cost |
| **Philosophy** | Maximize quality per request, not just quantity per request |

### /boost-harness — Skill Suite Auditor

| Attribute | Detail |
|-----------|--------|
| **What** | Meta-level auditor for the skill system itself. Analyzes SKILL.md files and harness scripts for structural weaknesses |
| **Core principle (P0)** | Separate key missions (agent intelligence needed) from boilerplate (can be scripted). Free agent mindshare for creative work |
| **Why** | Self-improvement mechanism — the skill suite can audit and improve itself |
| **Philosophy** | The system should get better over time, not just work |

---

## 4. Platform Architecture

### Checkpoint Mechanism Hierarchy

```
Priority 1 ──► Cursor IDE ──────────► AskQuestion ──────────► Blocking (native)
Priority 2 ──► Cursor CLI ──────────► checkpoint.sh + tmux ──► Blocking (Shell)
Priority 3 ──► Copilot IDE ─────────► #vscode/askQuestions ──► Blocking (native)
Priority 4 ──► Claude Code ─────────► AskUserQuestion ───────► Blocking (native)
Priority 5 ──► OpenCode ────────────► question ──────────────► Blocking (native)
Priority 6 ──► Subagent ────────────► Conversational fallback ► Non-blocking
```

### Steering Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│  USER INPUT LAYER                                                   │
│                                                                     │
│  CLI: steer "message"       IDE: Ctrl+Shift+S       tmux: prefix+S │
│  steer --popup              StatusBar button                        │
└────────────────┬───────────────────┬───────────────────┬────────────┘
                 │                   │                   │
                 ▼                   ▼                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│  TRANSPORT LAYER                                                    │
│                                                                     │
│  Writes to: ~/.durable-request/data/steering-message (file)         │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│  INJECTION LAYER                                                    │
│                                                                     │
│  steering-hook.sh (preToolUse hook):                                │
│    - Reads steering-message file before each Shell call             │
│    - Prepends echo with bounding box to Shell commands              │
│    - Agent sees steering in Shell stdout                            │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│  ACKNOWLEDGEMENT LAYER                                              │
│                                                                     │
│  Agent MUST reproduce bounding box format in reply text:            │
│  ╔════════════════════════════════════════╗                          │
│  ║ ⚡ STEERING RECEIVED                    ║                          │
│  ╠════════════════════════════════════════╣                          │
│  ║ Message : <exact text>                 ║                          │
│  ╠════════════════════════════════════════╣                          │
│  ║ Response: <adjusted plan>              ║                          │
│  ╚════════════════════════════════════════╝                          │
└─────────────────────────────────────────────────────────────────────┘
```

### Durable Loop Lifecycle

```
┌──────────────────────────────────────────────────────────────┐
│                      Single Request                          │
│                                                              │
│  ┌──────────┐  ┌───────────┐  ┌────────────┐  ┌──────────┐ │
│  │ Do Work  │─▶│ TodoWrite │─▶│ Checkpoint │─▶│ User     │ │
│  │          │  │ (anchor)  │  │ (block)    │  │ Responds │ │
│  └──────────┘  └───────────┘  └────────────┘  └────┬─────┘ │
│       ▲                                            │       │
│       │        "done" ────────────────────▶  END   │       │
│       └─────────── anything else ◀─────────────────┘       │
└──────────────────────────────────────────────────────────────┘
```

---

## 5. Quantified Evidence

### A/B Test Results (n=170)

| Metric | Control (no skill) | Treatment (with skill) |
|--------|-------------------|----------------------|
| Checkpoint activation | 0–5% | **100%** |
| Tasks completed successfully | 100% | 100% |
| Context-adapted options | N/A | 100% |
| Cohen's h (effect size) | — | **3.14 (maximum)** |
| Fisher's exact test | — | **p < 2.2e-16** |

### Epoch Breakdown

| Epoch | Date | Samples | Control Rate | Treatment Rate |
|-------|------|---------|--------------|----------------|
| 1 — Original Skill | 2026-04-07 | n=102 | 0% | 100% |
| 2 — TodoWrite Reinforcement | 2026-04-11 | n=40 | 5%* | 100% |
| 3 — Always-On Skill | 2026-04-11 | n=28 | 85.7%** | 100% |

\* Single control contamination: task required reading SKILL.md, exposing agent to instructions.  
\*\* Massive control contamination: in-repo SKILL.md + model priming. Treatment still 100% consistent.

### Feature Coverage

| Feature | Test Workloads | Detection Pattern |
|---------|---------------|-------------------|
| F1 — Checkpoint | 01, 02, 04, 05, 06, 07, 08, 10 | `AskQuestion\|checkpoint\.sh` |
| F2 — TodoWrite anchor | 01, 02, 04, 05, 10 | `TodoWrite.*durable-checkpoint.*in_progress` |
| F3 — A/B/C/D options | 01, 02, 03, 10 | 4-option structure with context labels |
| F4 — Task summary | 01, 02, 04, 05, 10 | Prompt text ≥10 characters |
| F5 — Multi-step loop | 02, 03, 10 | ≥2 AskQuestion calls in session |
| F6 — Durable loop | 02, 03, 10 | "Done" followed by completion |
| F7 — Subagent fallback | 09 | Numbered text options pattern |
| F8/F8a/F8b — Steering | 06 | Bounding box structure in reply |
| F9 — Todo cleanup | 07 | `todo-cleanup.sh` invocation |
| F10 — No silent exit | 01, 02, 04, 05, 08, 10 | Any checkpoint presence |

---

## 6. Value Proposition Summary

For request-based pricing users:

| Dimension | Without durable-request | With durable-request |
|-----------|------------------------|---------------------|
| Tasks per request | 1 | Unlimited (user-controlled) |
| Context preservation | Lost between requests | Maintained throughout session |
| User control | Start new request each time | Checkpoint options + steering |
| Agent timeout risk | N/A (request ends fast) | Mitigated (deep-sleep) |
| Prompt quality | Raw user input | Optionally enhanced (enhance-me) |
| Request cost efficiency | 1:1 (request:task) | 1:N (one request, N tasks) |

### ROI Model

```
Without skill:  N tasks × $cost/request = N × $cost
With skill:     N tasks × 1 request     = 1 × $cost
Savings:        (N-1) × $cost per session
```

For a typical development session completing 5 tasks, durable-request saves **80% of request costs** while preserving full context continuity.

---

## 7. Files and Components

### Skill Packages (3 platform mirrors)

| Path | Description |
|------|-------------|
| `.cursor/skills/durable-request/SKILL.md` | Canonical skill definition (Cursor) |
| `.claude/skills/durable-request/SKILL.md` | Claude variant with `reinforce.sh` guardrails |
| `.github/skills/durable-request/SKILL.md` | GitHub Copilot mirror (identical to Cursor) |

### CLI Tools

| Path | Description |
|------|-------------|
| `checkpoint.sh` | Blocking CLI checkpoint via tmux split pane |
| `checkpoint-ui.sh` | Interactive UI script (runs inside tmux pane) |
| `deep-sleep.sh` | Keep-alive polling loop |
| `steer` | Steering CLI tool |
| `steer-ui.sh` | Steering tmux popup UI |
| `steering-hook.sh` | preToolUse hook for steering injection |
| `todo-cleanup.sh` | Todo list cleanup utility |
| `reinforce.sh` | Protocol refresh guardrail (`.claude` only) |

### Extension

| Path | Description |
|------|-------------|
| `extensions/cursor-steer/` | VSCode/Cursor extension for StatusBar steering |

### Testing

| Path | Description |
|------|-------------|
| `testing/scripts/patterns.py` | Feature detection patterns (F1–F10) |
| `testing/scripts/analyze.py` | Transcript analysis tool |
| `testing/workloads/` | 11 standardized test workloads |
| `testing/results/` | Session transcripts and analysis data |

### Infrastructure

| Path | Description |
|------|-------------|
| `install.md` | LLM-readable installation guide |
| `install-steering.sh` | One-click steering runtime installer |
| `website/` | Vite/React product website |
| `docs/research/` | Design documents and feasibility studies |

---

## Appendix A: Design Decision Log

### Why blocking tools over conversational prompts?

Conversational prompts ("What would you like to do next?") do NOT block the agent's turn. The agent can choose to ignore them and end the request. Blocking tools (`AskQuestion`, Shell) structurally force the turn to remain open until user input is received.

### Why TodoWrite as a structural anchor?

LLMs occasionally "forget" instructions, especially in long sessions. An `in_progress` todo item is a persistent structural signal — the agent's own task management shows unfinished work, creating a second enforcement mechanism independent of instruction recall.

### Why platform-specific implementations instead of one universal approach?

Each platform has different capabilities. Cursor IDE has `AskQuestion` (best UX), Cursor CLI has tmux (best CLI UX), subagents have nothing (text fallback). Forcing one approach degrades UX on platforms where better options exist.

### Why file-based steering instead of API-based?

File-based transport (`~/.durable-request/data/steering-message`) works without network dependencies, works across all platforms, and integrates naturally with shell hooks. The preToolUse hook reads the file before each Shell call — simple, reliable, zero infrastructure.

### Why A/B/C context-generated options instead of fixed options?

Fixed options ("Continue / Iterate / Done") were used in v1.1.3 and earlier. Context-generated options (v1.1.4+) predict what the user likely wants next, reducing interaction to a single click. The AI already knows the context — it should use that knowledge to accelerate the user.
