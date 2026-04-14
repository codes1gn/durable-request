# Changelog

All notable changes to durable-request are documented here.

## [1.2.0] - 2026-04-14

### Added
- **Copilot IDE (VSCode) support** — `#vscode/askQuestions` integration with Question Carousel UI
- Environment detection for Copilot IDE in checkpoint priority table

### Research
- **Steering in-continuation** design documented for Cursor IDE (hook-based approach)
- `PreToolUse` hook steering implementation design (`docs/research/cursor-steering-implementation.md`)
- Copilot steering cost analysis (`docs/research/copilot-askquestions-steering.md`)

### Documentation
- `docs/research/copilot-askquestions-steering.md` — comprehensive research on Copilot tools, steering, and billing
- `docs/research/cursor-steering-implementation.md` — detailed implementation design for Cursor steering

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
