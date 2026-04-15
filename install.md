# Durable Request — Installation Guide

This guide is designed to be read and executed by an LLM agent.

## What You're Installing

Three components:

1. **Skill package** (`skill/` — 7 files) — teaches any AI agent to present interactive checkpoints, handle steering acknowledgements, and manage the durable loop. Works on all platforms. Includes SKILL.md, checkpoint scripts, steering tools, and todo-cleanup.
2. **CLI checkpoint tool** (`skill/checkpoint.sh` + `skill/checkpoint-ui.sh`, Cursor CLI only) — enables true blocking interactive checkpoints in Cursor CLI via tmux split panes. Already included in the skill package above.
3. **Steering runtime + IDE extension** (Cursor only) — mid-task instructions via CLI (`steer`), tmux popup, or Cursor IDE extension (status bar button + Ctrl+Shift+S). Installed by running `install-steering.sh`.

## Step 1: Clone the Repository

Clone the repo via SSH (requires a git.enflame.cn account with SSH key configured):

```bash
git clone git@git.enflame.cn:skills/durablerequest.git /tmp/durable-request-repo
```

## Step 2: Install Skill Package to Agent Skill Directories

Copy all skill files into the relevant directories for every platform the user has. Create directories if they don't exist.

Install to **project-level** (current directory) and **personal** (`~`) for each platform:

| Platform | Project path | Personal path |
|----------|-------------|---------------|
| Cursor | `.cursor/skills/durable-request/` | `~/.cursor/skills/durable-request/` |
| Claude Code | `.claude/skills/durable-request/` | `~/.claude/skills/durable-request/` |
| GitHub Copilot | `.github/copilot/skills/durable-request/` | `~/.github/copilot/skills/durable-request/` |
| OpenAI Codex | `.codex/skills/durable-request/` | `~/.codex/skills/durable-request/` |
| Google Gemini CLI | `.gemini/skills/durable-request/` | `~/.gemini/skills/durable-request/` |
| Windsurf | `.windsurf/skills/durable-request/` | `~/.windsurf/skills/durable-request/` |
| Aider | `.aider/skills/durable-request/` | `~/.aider/skills/durable-request/` |
| Cody | `.cody/skills/durable-request/` | `~/.cody/skills/durable-request/` |
| Continue | `.continue/skills/durable-request/` | `~/.continue/skills/durable-request/` |

For **Cursor** (personal), run:

```bash
DIR=~/.cursor/skills/durable-request && mkdir -p "$DIR" && \
cp /tmp/durable-request-repo/skill/{SKILL.md,checkpoint.sh,checkpoint-ui.sh,steer,steer-ui.sh,steering-hook.sh,todo-cleanup.sh} "$DIR/" && \
chmod +x "$DIR"/*.sh "$DIR/steer"
```

For **other platforms** (SKILL.md is sufficient — no shell scripts needed):

```bash
mkdir -p <directory> && cp /tmp/durable-request-repo/skill/SKILL.md <directory>/SKILL.md
```

## Step 3: Configure tmux for Cursor CLI (Cursor CLI only)

This step is **only for Cursor CLI** users. The checkpoint scripts were already copied in Step 2. This step configures tmux, which is required for the blocking checkpoint UI.

Skip this step if:
- You are installing for Cursor IDE (graphical editor), not Cursor CLI
- You are installing for any non-Cursor platform

### 3a: Set up tmux + locale (required for Cursor CLI)

Add these to `~/.bashrc`:

```bash
cat >> ~/.bashrc << 'BASHEOF'
# UTF-8 locale for proper terminal rendering
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# Run cursor-agent inside tmux for interactive checkpoints
alias cursor-agent='tmux new-session -A -s cursor -- cursor-agent'
BASHEOF
source ~/.bashrc
```

Set the tmux terminal type for proper Unicode support:

```bash
cat >> ~/.tmux.conf << 'TMUXEOF'
set -g default-terminal "tmux-256color"
set -gq utf8 on
TMUXEOF
```

If tmux is already running, kill it so it picks up the new config: `tmux kill-server`

### 3b: Verify checkpoint scripts

```bash
ls -la ~/.cursor/skills/durable-request/checkpoint*.sh
```

## Step 4: Install Steering Feature (Cursor only)

This step is **only for Cursor** users (both IDE and CLI). Skip for other platforms.

Run the one-click installation script **from the repo directory** so it can resolve `./skill/` locally:

```bash
cd /tmp/durable-request-repo && bash install-steering.sh
```

This installs:
- `steer` CLI tool to `~/.durable-request/bin/`
- `steer-ui.sh` tmux popup to `~/.durable-request/bin/`
- `steering-hook.sh` preToolUse hook to `~/.durable-request/hooks/`
- Cursor hooks configuration to `~/.cursor/hooks.json`
- tmux keybinding (prefix + S) to `~/.tmux.conf`
- Optional: Cursor/VSCode extension for status bar button + Ctrl+Shift+S

After installation:
```bash
# Verify CLI
~/.durable-request/bin/steer --help

# Test steering
steer "test message"
steer --status
steer --clear
```

## Step 5: Verify

Confirm the skill file exists:

```bash
ls ~/.cursor/skills/durable-request/SKILL.md 2>/dev/null \
  || ls .cursor/skills/durable-request/SKILL.md 2>/dev/null \
  && echo "Skill file verified." || echo "Not found — check other platform paths."
```

Confirm steering is installed (Cursor only):

```bash
~/.durable-request/bin/steer --status 2>/dev/null \
  && echo "Steering verified." \
  || echo "Steering not installed (optional, Cursor only)."
```

## Step 6: Restart Your Agent Session

The skill is active the next time you start an agent session. No config changes needed. The CLI checkpoint tool is picked up automatically.

## Cleanup

```bash
rm -rf /tmp/durable-request-repo
```

## Uninstall

To remove the skill, delete the installed directories:

```bash
rm -rf ~/.cursor/skills/durable-request \
       ~/.claude/skills/durable-request \
       ~/.github/copilot/skills/durable-request \
       .cursor/skills/durable-request \
       .claude/skills/durable-request
# ... repeat for other platforms as needed
```
