# Changelog

All notable changes to durable-request are documented here.

## [1.2.1] - 2026-04-14

### Fixed
- `steer-ui.sh` now installs to `~/.durable-request/bin/` instead of `skill/`
- `steer` CLI updated to prioritize `bin/` path when searching for UI script
- `install-steering.sh` cleans up old `skill/steer-ui.sh` location during install
- Updated `steer` header comments to reflect Shell command modification workaround
- Improved Cursor extension install status detection in install script

## [1.2.0] - 2026-04-14

### Added
- **Copilot IDE (VSCode) support** — `#vscode/askQuestions` integration with Question Carousel UI
- **Cursor IDE steering** — mid-task steering messages via preToolUse hook
  - `steer` CLI tool for sending steering messages
  - `steer-ui.sh` for interactive tmux popup
  - `steering-hook.sh` preToolUse hook with Shell command modification workaround
  - Cursor extension for StatusBar button + keyboard shortcut (Ctrl+Shift+S)
- **One-click install script** — `install-steering.sh` installs CLI, hook, extension, and tmux keybinding

### Technical Details
- Shell command modification workaround: steering injected via `updated_input.command` prepending echo
- Non-Shell tools: steering kept pending until next Shell call (due to Cursor `additionalContext` bug)
- Supports both Cursor IDE and CLI modes

### Research
- **Cursor hooks bug analysis**: documented that `additionalContext`, `agent_message`, and `postToolUse additional_context` do NOT surface to model
- Workaround strategy: modify Shell commands to include steering in stdout
- `docs/research/cursor-steering-implementation.md` — updated with bug findings and workaround

### Documentation
- `docs/research/copilot-askquestions-steering.md` — Copilot tools, steering, and billing
- `docs/research/cursor-extension-feasibility.md` — VSCode extension technical analysis
- `docs/research/steering-ux-comparison.md` — CLI vs extension UX comparison

## [1.1.1] - 2026-04-14

### Added
- **Copilot IDE (VSCode) support** — `#vscode/askQuestions` integration (research phase)
- Environment detection for Copilot IDE in checkpoint priority table

### Research
- `PreToolUse` hook steering design documentation

## [1.1.0] - 2026-04-12

### Added
- **Cursor CLI checkpoint** (`checkpoint.sh` + `checkpoint-ui.sh`) — true blocking interactive checkpoints in Cursor CLI via tmux split panes, achieving the same durable loop as `AskQuestion` in the editor
- Three-layer checkpoint architecture: AskQuestion (editor) → checkpoint.sh (CLI) → conversational fallback (subagents)

### Automated Testing
- **20-checkpoint continuation batch**: 60/60 passed (20×continue, 20×iterate, 20×done = 100%)
- Fresh install verification: SKILL.md + checkpoint scripts validated end-to-end
- Graceful fallback without tmux confirmed (exit 0, explicit messaging)

## [1.0.1] - 2026-04-11

### Added
- Epoch 3 A/B experiments (30 control + 30 treatment subagents)
- Product website with animated feature demos
- LAN serving script (`serve.sh`) + systemd service file

## [1.0.0] - 2026-04-10

### Added
- Initial release of durable-request skill
- AskQuestion integration for Cursor editor
- AskUserQuestion integration for Claude Code
- `question` tool integration for OpenCode
- Conversational fallback for all platforms
- TodoWrite + AskQuestion reinforcement pattern
- A/B experiment harness with 170 total subagent experiments across 3 epochs
