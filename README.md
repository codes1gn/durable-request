<p align="center">
  <h1 align="center">durable-request</h1>
  <p align="center">
    <strong>Get more out of every AI agent request.</strong>
  </p>
</p>

<p align="center">
  <a href="http://git.enflame.cn/skills/durablerequest/-/blob/main/LICENSE"><img alt="License: Apache 2.0" src="https://img.shields.io/badge/License-Apache%202.0-blue.svg"></a>
  <a href="http://git.enflame.cn/skills/durablerequest"><img alt="Stars" src="https://img.shields.io/badge/Stars-0-blue"></a>
  <a href="http://git.enflame.cn/skills/durablerequest/-/issues"><img alt="Issues" src="https://img.shields.io/badge/Issues-0-red"></a>
</p>

<p align="center">
  <a href="http://10.12.114.217:3456/durable-request/">Website</a> &bull;
  <a href="#why">Why</a> &bull;
  <a href="#installation">Install</a> &bull;
  <a href="#quantified-results">Results</a> &bull;
  <a href="#how-it-works">How It Works</a> &bull;
  <a href="#supported-platforms">Platforms</a> &bull;
  <a href="#reproducing-the-ab-test">Reproduce</a>
</p>

---

## Why

Agent requests cost money. On Cursor, Claude, Copilot, or any usage-based plan, each request is a paid interaction. Without this skill, the agent finishes one task and stops — you have to start a new request to keep going.

```
Without this skill:                         With this skill:

  Request 1: "Add auth"                     Request 1: "Add auth"
  Agent: "Done."                            Agent: "Done. What's next?"
                                              → "Add tests"
  Request 2: "Add tests"                      → "Add rate limiting"
  Agent: "Done."                              → "Handle errors"
                                              → "Commit"
  Request 3: "Rate limiting"                  → "Done"
  Agent: "Done."
                                            1 request, 5 things done.
  Request 4: "Handle errors"
  Agent: "Done."

  Request 5: "Commit"
  Agent: "Done."

  5 requests, 5 things done.
```

With durable-request installed, the agent asks what to do next instead of stopping. You stay in the same session, keep the context, and get more done per request. Mid-task, you can also send steering messages to redirect the agent without interrupting it.

## What It Does

After finishing any task, the agent presents options instead of going silent:

> **Completed:** Added the Fibonacci function to `fib.py`.
>
> **What's next?**
> 1. Iterate / refine (add tests, change algorithm)
> 2. Continue to the next step
> 3. Review the implementation
> 4. Switch to a different task
> 5. Done

In Cursor, this shows up as a clickable UI widget (via `AskQuestion`). In CLI tools, it's numbered text options. Either way, the agent waits for you instead of disappearing.

---

## Quantified Results

Validated across **3 epochs** with **170 total subagent experiments**.

### Epoch 1 — Original Skill (2026-04-07, n=102)

<table>
<tr><th>Metric</th><th>Without Skill</th><th>With Skill</th></tr>
<tr><td>Offered continuation options</td><td align="center"><strong>0%</strong> (0/51)</td><td align="center"><strong>100%</strong> (51/51)</td></tr>
<tr><td>Tasks completed successfully</td><td align="center">100%</td><td align="center">100%</td></tr>
<tr><td>Context-adapted options</td><td align="center">N/A</td><td align="center">100%</td></tr>
<tr><td>Fisher's exact test</td><td align="center">-</td><td align="center"><code>p < 2.2e-16</code></td></tr>
<tr><td>Effect size (Cohen's h)</td><td align="center">-</td><td align="center"><strong>3.14 (maximum)</strong></td></tr>
</table>

### Epoch 2 — Updated Skill with TodoWrite Reinforcement (2026-04-11, n=40)

<table>
<tr><th>Metric</th><th>Without Skill</th><th>With Skill</th></tr>
<tr><td>Offered continuation options</td><td align="center"><strong>5%</strong> (1/20)*</td><td align="center"><strong>100%</strong> (20/20)</td></tr>
<tr><td>Tasks completed successfully</td><td align="center">100%</td><td align="center">100%</td></tr>
<tr><td>Context-adapted options</td><td align="center">5%*</td><td align="center">100%</td></tr>
<tr><td>Verbose fallback message</td><td align="center">5%*</td><td align="center">85% (actual)</td></tr>
<tr><td>Effect size (Cohen's h)</td><td align="center">-</td><td align="center"><strong>2.69</strong></td></tr>
</table>

<sub>*Single control contamination: task required reading SKILL.md, exposing agent to checkpoint instructions.</sub>

### Epoch 3 — Always-On Skill (2026-04-11, n=28)

<table>
<tr><th>Metric</th><th>Without Skill</th><th>With Skill</th></tr>
<tr><td>Offered continuation options</td><td align="center"><strong>85.7%</strong> (12/14)*</td><td align="center"><strong>100%</strong> (14/14)</td></tr>
<tr><td>Tasks completed successfully</td><td align="center">100%</td><td align="center">100%</td></tr>
<tr><td>Context-adapted options</td><td align="center">71.4%</td><td align="center">100%</td></tr>
</table>

<sub>*Massive control contamination: in-repo SKILL.md exposure + model capability primed uninstructed agents. Treatment still 100% consistent.</sub>

### Combined Results (n=170)

| Scenario | Epoch | Control | Treatment |
|:---------|:-----:|:-------:|:---------:|
| Code Generation | 1 (n=34) | 0% | 100% |
| Code Generation | 2 (n=20) | 0% | 100% |
| Code Generation | 3 (n=14) | 85.7% | 100% |
| Analysis & Research | 1 (n=34) | 0% | 100% |
| Analysis & Research | 2 (n=10) | 20%* | 100% |
| Analysis & Research | 3 (n=8) | 75% | 100% |
| File Manipulation | 1 (n=34) | 0% | 100% |
| File Manipulation | 2 (n=10) | 0% | 100% |
| File Manipulation | 3 (n=6) | 66.7% | 100% |

<sub>*Epoch 2: single contamination from task requiring reading SKILL.md. Epoch 3: high control contamination from in-repo skill file exposure.</sub>

> Full data in [`data/`](data/) organized by epoch. Each epoch has its own folder with results, artifacts, and statistics.

---

## Installation

### Recommended — Let Your AI Agent Install It

Paste this into any AI agent chat (Cursor, Claude Code, Codex, etc.):

```
Install durable-request by following install.md at git@git.enflame.cn:skills/durablerequest.git
```

The agent clones the repo, reads `install.md`, and handles all three components automatically: skill package, steering runtime, and Cursor extension.

### Manual

```bash
# Clone
git clone git@git.enflame.cn:skills/durablerequest.git /tmp/dr

# Install skill package — copies to all three platform directories
for DIR in ~/.cursor/skills/durable-request ~/.claude/skills/durable-request ~/.github/skills/durable-request; do
  mkdir -p "$DIR" && \
  cp /tmp/dr/.cursor/skills/durable-request/{SKILL.md,checkpoint.sh,checkpoint-ui.sh,deep-sleep.sh,steer,steer-ui.sh,steering-hook.sh,todo-cleanup.sh} "$DIR/" && \
  chmod +x "$DIR"/*.sh "$DIR/steer"
done

# Install steering runtime + Cursor extension (Cursor only)
cd /tmp/dr && bash install-steering.sh && cd -

# Cleanup
rm -rf /tmp/dr
```

See [install.md](install.md) for full step-by-step instructions and platform-specific paths.

---

## Supported Platforms

| Platform | Skill Location | Status |
|:---------|:--------------|:------:|
| Cursor | `.cursor/skills/` or `~/.cursor/skills/` | Tested |
| Claude Code | `.claude/skills/` | Tested |
| OpenCode | `.skills/` | Compatible but not tested |
| GitHub Copilot | `.github/copilot/skills/` | Compatible but not tested |
| OpenAI Codex | `.codex/skills/` | Compatible but not tested |
| Google Gemini CLI | `.gemini/skills/` | Compatible but not tested |
| Windsurf | `.windsurf/skills/` | Compatible but not tested |
| Aider | `.aider/skills/` | Compatible but not tested |
| Cody | `.cody/skills/` | Compatible but not tested |
| Continue | `.continue/skills/` | Compatible but not tested |

> **Tested** = validated with A/B tests. **Compatible but not tested** = standard skill format (YAML frontmatter + markdown), should work but not yet A/B tested.

---

## How It Works

The system operates through three layers, each providing a blocking interactive checkpoint:

```
Layer 1: AskQuestion (tool-based)   Layer 2: checkpoint.sh (CLI)        Layer 3: Conversational fallback
Built-in agent tool                  Tmux split-pane interactive UI       Numbered text options
Blocks agent turn, UI widget         Blocks via Shell + file polling      Plain text (non-blocking)
User picks from structured UI        User picks in tmux pane              User types response
Cursor editor, Claude Code           Cursor CLI (requires tmux)           Subagents, all platforms
```

### Cursor Editor: AskQuestion

In Cursor's editor, `AskQuestion` is a built-in tool that **pauses the agent's turn without ending the request**. The user responds through a structured UI widget, and the agent continues in the same request context:

```
┌─────────────────────────────────────────────────┐
│                  Single Request                  │
│                                                  │
│  ┌──────────┐    ┌────────────┐    ┌──────────┐ │
│  │ Do Work  │───▶│ AskQuestion│───▶│ User     │ │
│  │          │    │ (blocks)   │    │ Responds │ │
│  └──────────┘    └────────────┘    └─────┬────┘ │
│       ▲                                  │      │
│       │          "done" ──────────▶ END  │      │
│       └──────── anything else ◀──────────┘      │
└─────────────────────────────────────────────────┘
```

### Cursor CLI: checkpoint.sh via tmux (True Durable Loop)

In Cursor CLI, `AskQuestion` is not available. The `checkpoint.sh` tool creates a tmux split pane where the user selects their next action, then returns the choice to the agent. The Shell call blocks, achieving a true durable loop:

```
┌──────────────────────────────────────────────────────────────┐
│                      Single Request                          │
│                                                              │
│  ┌──────────┐  ┌───────────┐  ┌──────────────┐ ┌──────────┐│
│  │ Do Work  │─▶│ TodoWrite │─▶│ Shell:       │─▶│ User     ││
│  │          │  │ (anchor)  │  │ checkpoint.sh│  │ picks in ││
│  └──────────┘  └───────────┘  │ (blocks)     │  │ tmux pane││
│       ▲                       └──────────────┘  └────┬─────┘│
│       │        "done" ────────────────────────▶ END  │      │
│       └─────────── anything else ◀───────────────────┘      │
│                                                              │
│  checkpoint.sh creates tmux split pane → user picks option   │
│  → pane auto-closes → agent reads response from stdout       │
└──────────────────────────────────────────────────────────────┘
```

**Prerequisite:** Run `cursor-agent` inside tmux. Recommended alias for `~/.bashrc`:

```bash
alias cursor-agent='tmux new-session -A -s cursor -- cursor-agent'
```

**Note:** Subagents (launched via the `Task` tool) do NOT have access to `AskQuestion` or `checkpoint.sh`. The skill automatically falls back to conversational checkpoints (Layer 3) in subagent contexts.

The skill **adapts its options contextually** based on what was just completed:

| After... | Options include |
|----------|----------------|
| Code changes | Run tests, Iterate, Commit |
| Debugging | Dig deeper, Apply fix, Check similar |
| Analysis | Explore further, Different angle, Apply findings |
| Writing | Revise, Next section, Review accuracy |
| File operations | Verify output, Modify format, Additional ops |

---

## Steering (Mid-Task Instructions)

Send instructions to the agent **while it's working** without interrupting the current task.

### Cursor IDE

**Option 1: Keyboard shortcut**
- Press `Ctrl+Shift+S` (or `Cmd+Shift+S` on Mac)
- Type your steering message
- Press Enter

**Option 2: Status bar button**
- Click the "🔊 Steer" button in the bottom status bar
- Type your steering message

### Cursor CLI / Terminal

```bash
# Direct command
steer "focus on the API layer"
steer "skip tests, just implement"

# Interactive popup (requires tmux)
steer --popup

# Check pending steering
steer --status

# Clear pending steering
steer --clear
```

### tmux Integration

If you're using tmux, add this to `~/.tmux.conf`:

```bash
# Press prefix + S to open steering popup
bind-key S run-shell "~/.durable-request/bin/steer --popup"
```

Then reload: `tmux source-file ~/.tmux.conf`

### How It Works

1. User sends steering via CLI, tmux popup, or Cursor extension
2. Message is saved to `~/.durable-request/data/steering-message`
3. `preToolUse` hook reads the file before each Shell command
4. Hook modifies the command to include the steering message as output
5. Agent sees the steering in Shell output and **must acknowledge it**

**Important:** The agent is instructed to acknowledge steering with:
> **[durable-request]** Received steering: "your message". Adjusting...

**Note:** Due to Cursor hook limitations, steering only appears in Shell tool output. If the agent is only using Read/Write/Grep tools, steering remains pending until the next Shell call.

---

## Platform-Specific Behavior

| Platform | Checkpoint Tool | Blocking? | Behavior | Tested |
|:---------|:---------------|:---------:|:---------|:------:|
| Cursor editor (parent) | `AskQuestion` | Yes | UI widget, same request | Yes |
| Cursor CLI (parent) | `checkpoint.sh` via Shell | Yes | Tmux split pane, same request | Yes |
| Cursor (subagent) | Conversational fallback | No | Numbered text options | Yes (A/B) |
| Claude Code | `AskUserQuestion` | Yes | Pauses turn, same request | Yes |
| OpenCode | `question` | Yes | Pauses turn, same request | Compatible |
| CLI / other | Conversational fallback | No | Numbered text options | Yes (A/B) |

## Integration with Existing Skills

durable-request is **additive** — it doesn't interfere with task-specific loop behavior:

```
Priority:
  1. Task-specific skill loops (within the task)
  2. durable-request checkpoint (at task boundaries only)
```

Skills with their own continuation logic (tuning sweeps, FSM engines, etc.) take precedence internally. durable-request activates only when those skills reach their own completion point.

---

## Testing Framework

The `testing/` directory contains the new testing framework:

```bash
# Analyze test session transcripts
python testing/scripts/analyze.py testing/results/run-YYYY-MM-DD/

# Run checkpoint simulation
python testing/scripts/checkpoint_cli.py test-suite
```

See [testing/README.md](testing/README.md) for workload definitions and feature verification patterns.

---

## Repository Structure

```
durable-request/
├── README.md                          # This file
├── install.md                         # LLM-readable installation guide
├── install-steering.sh                # One-click Cursor steering installer
├── CHANGELOG.md                       # Version history
├── .claude/skills/durable-request/    # Claude Code skill package
├── .cursor/skills/durable-request/    # Cursor skill package
├── .github/skills/durable-request/    # GitHub Copilot skill package
│   ├── SKILL.md                       # The skill (copy to install)
│   ├── checkpoint.sh                  # CLI checkpoint tool (tmux split-pane)
│   ├── checkpoint-ui.sh               # UI script (runs inside tmux pane)
│   ├── deep-sleep.sh                  # Keep agent alive while user is away
│   ├── steer                          # Steering CLI tool
│   ├── steer-ui.sh                    # Steering tmux popup UI
│   ├── steering-hook.sh               # preToolUse hook for steering injection
│   └── todo-cleanup.sh                # Automatic todo list cleanup
├── testing/
│   ├── README.md                      # Testing framework documentation
│   ├── workloads/                     # 10 standardized test workloads
│   │   ├── 01-simple-task.md
│   │   ├── 02-multi-step.md
│   │   └── ...
│   ├── scripts/
│   │   ├── patterns.py                # Feature detection patterns
│   │   ├── analyze.py                 # Transcript analysis tool
│   │   └── checkpoint_cli.py          # CLI checkpoint simulator
│   └── results/                       # Session transcripts (gitignored)
├── extensions/
│   └── cursor-steer/                  # Cursor/VSCode steering extension
├── docs/
│   └── research/                      # Design documents and research
└── website/                           # Product website
```

---

## Contributing

Found a platform we should support? Have ideas for better checkpoint options? Open an issue or PR.

## License

[Apache License 2.0](LICENSE)

Copyright 2026 Enflame Intelligence Technologies Co., Ltd.

## Author

**Heng Shi** / [@heng.shi](http://git.enflame.cn/heng.shi)

---

<p align="center">
  <sub>Built with data-driven skill design. Every claim backed by evidence from 170 agent experiments across 3 epochs.</sub>
</p>
