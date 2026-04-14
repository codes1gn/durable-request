# Durable Request Steering

Send steering messages to AI agents mid-execution without interrupting the current task.

## Features

- **Status Bar Button**: Click "🔊 Steer" in the status bar to send a steering message
- **Keyboard Shortcut**: `Ctrl+Shift+S` (Windows/Linux) or `Cmd+Shift+S` (macOS)
- **Command Palette**: Search for "Durable Request: Steer Agent"
- **Visual Feedback**: Status bar changes color when steering is pending

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│  1. Click [🔊 Steer] or press Ctrl+Shift+S                  │
│                                                              │
│  2. Enter your steering message                              │
│     e.g., "focus on the API layer"                          │
│                                                              │
│  3. Message is written to ~/.durable-request/data/          │
│                                                              │
│  4. preToolUse hook detects file at next tool call          │
│                                                              │
│  5. Agent sees: "⚡ [USER STEERING]: focus on API layer"    │
│                                                              │
│  6. Agent adjusts its behavior accordingly                   │
└─────────────────────────────────────────────────────────────┘
```

## Requirements

- Cursor IDE or VS Code
- The `steering-hook.sh` must be installed and configured in `.cursor/hooks.json`

### Hook Setup

1. Copy `steering-hook.sh` to `~/.durable-request/hooks/`
2. Add to `~/.cursor/hooks.json`:

```json
{
  "version": 1,
  "hooks": {
    "preToolUse": [
      {
        "command": "~/.durable-request/hooks/steering-hook.sh",
        "timeout_ms": 2000
      }
    ]
  }
}
```

## Commands

| Command | Description |
|---------|-------------|
| `Durable Request: Steer Agent` | Send a steering message |
| `Durable Request: Clear Steering` | Remove pending steering |
| `Durable Request: Steering Status` | Check pending steering |

## Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `durableRequest.steeringDataDir` | `~/.durable-request/data` | Custom directory for steering data |
| `durableRequest.showStatusBarButton` | `true` | Show the Steer button |
| `durableRequest.notifyOnSteer` | `true` | Show notification when steering is queued |

## Building

```bash
npm install
npm run compile
npm run package
```

This creates `durable-request-steer-0.1.0.vsix`.

## Installing

```bash
# In Cursor
cursor --install-extension durable-request-steer-0.1.0.vsix

# Or via Command Palette
# Extensions: Install from VSIX...
```

## License

Apache-2.0
