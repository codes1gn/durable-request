# Cursor IDE Steering Implementation Design

## 概述

本文档详细设计 Cursor IDE 上的 steering-in-continuation 实现方案。

## 方案演进历程

### 理想方案 (不可行)

**方案 1: Chat 输入框 + beforeSubmitPrompt Hook**

理想的用户体验是直接在 Cursor Chat 输入框输入 steering message，然后通过 hook 拦截处理：

```
用户在 Chat 输入 steering → beforeSubmitPrompt hook 触发 → 
写入文件 + return {continue: false} → preToolUse 读取 → 注入 context
```

**为什么不可行:**

| 问题 | 状态 | 说明 |
|------|------|------|
| Queue 消息触发 `beforeSubmitPrompt` | ❌ Bug | 走了不同代码路径，hook 不触发 |
| `beforeSubmitPrompt` 支持 `additionalContext` | ❌ 不支持 | 只能 block，无法注入 context |
| `continue: false` 阻止发送 | ⚠️ Bug | 消息仍在 history，下次会泄露 |
| 读取 queue 内容 | ❌ 无 API | Cursor 不暴露 queue 访问接口 |
| 清除 queue | ❌ 无 API | 只有手动 Alt+Enter |

**参考:**
- [Queued agent messages not triggering expected hooks](https://forum.cursor.com/t/queued-agent-messages-not-triggering-expected-hooks/155183)
- [beforeSubmitPrompt hook block is broken](https://forum.cursor.com/t/beforesubmitprompt-hook-block-is-broken/156823)
- [No mechanism to trigger hooks when agent is idle](https://forum.cursor.com/t/no-mechanism-to-trigger-hooks-or-inject-messages-into-cursor-when-agent-is-idle/153966)

### 当前方案 (推荐)

**方案 2: 文件协议 + 双入口 (CLI + 扩展)**

绕过 Cursor 的 hook 限制，提供两种输入方式：

```
┌─────────────────────────────────────────────────────────────┐
│  入口 1: Cursor 扩展 (推荐日常使用)                           │
│                                                              │
│  [状态栏 Steer 按钮] 或 [Ctrl+Shift+S]                       │
│         │                                                    │
│         ▼                                                    │
│  [输入框弹出] ──▶ 输入 steering message                       │
│         │                                                    │
│         ▼                                                    │
│  ~/.durable-request/data/steering-message                    │
├─────────────────────────────────────────────────────────────┤
│  入口 2: CLI (推荐脚本/自动化)                                │
│                                                              │
│  $ steer "focus on API layer"                                │
│         │                                                    │
│         ▼                                                    │
│  ~/.durable-request/data/steering-message                    │
└─────────────────────────────────────────────────────────────┘
           │
           ▼
  preToolUse hook 检测文件 → 读取 + 注入 additionalContext → 删除文件
```

**优点:**
- 不依赖 Cursor 的 bug 被修复
- 扩展方案提供最佳日常 UX (无需切换窗口)
- CLI 保留用于脚本化/自动化
- 两者共享相同文件协议，无额外维护成本
- `preToolUse` hook 的 `additionalContext` 功能稳定
- 可跨平台复用 (Cursor, Claude Code, OpenCode)

**UX 对比:** 详见 [steering-ux-comparison.md](./steering-ux-comparison.md)

## 核心机制: PreToolUse Hook

### 架构

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            Agent Turn (Active)                               │
│                                                                              │
│  ┌──────────┐    ┌────────────────────┐    ┌──────────────────────────────┐ │
│  │ Tool     │───▶│ PreToolUse Hook    │───▶│ Tool Execution               │ │
│  │ Queued   │    │                    │    │                              │ │
│  └──────────┘    │ 1. Check steering  │    └──────────────────────────────┘ │
│                  │    file            │                                      │
│                  │ 2. If exists:      │                                      │
│                  │    - Read content  │                                      │
│                  │    - Inject as     │                                      │
│                  │      context       │                                      │
│                  │    - Clear file    │                                      │
│                  │ 3. Return          │                                      │
│                  └────────────────────┘                                      │
│                                                                              │
│  User types: steer "focus on X" ───▶ ~/.cursor/steering-message             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 文件结构

```
~/.cursor/
├── steering-message          # 当前 steering 消息 (被 hook 消费后删除)
├── steering-history.log      # 历史记录 (可选, debug 用)
└── hooks.json                # 用户级 hook 配置

<project>/
├── .cursor/
│   ├── hooks/
│   │   └── steering-hook.sh  # 项目级 steering hook
│   └── hooks.json            # 项目级 hook 配置
└── ...
```

---

## 实现

### 1. Steering Hook (`steering-hook.sh`)

```bash
#!/bin/bash
# Cursor IDE PreToolUse hook for mid-turn steering
# Location: ~/.cursor/hooks/steering-hook.sh or .cursor/hooks/steering-hook.sh

set -euo pipefail

STEERING_FILE="${CURSOR_STEERING_FILE:-$HOME/.cursor/steering-message}"
HISTORY_FILE="${CURSOR_STEERING_HISTORY:-$HOME/.cursor/steering-history.log}"
ENABLE_HISTORY="${CURSOR_STEERING_LOG:-false}"

# No steering file, exit cleanly
[ -f "$STEERING_FILE" ] || exit 0

# Read and validate
MSG=$(cat "$STEERING_FILE" 2>/dev/null || echo "")
[ -z "$MSG" ] && { rm -f "$STEERING_FILE"; exit 0; }

# Log if enabled
if [ "$ENABLE_HISTORY" = "true" ]; then
  echo "[$(date -Iseconds)] $MSG" >> "$HISTORY_FILE"
fi

# Consume the message
rm -f "$STEERING_FILE"

# Determine priority level from message prefix
PRIORITY="normal"
case "$MSG" in
  "!!!"*|"URGENT:"*|"STOP:"*)
    PRIORITY="critical"
    ;;
  "!!"*|"ASAP:"*)
    PRIORITY="high"
    ;;
esac

# Format the context injection
CONTEXT_PREFIX="⚡ [STEERING"
[ "$PRIORITY" != "normal" ] && CONTEXT_PREFIX="$CONTEXT_PREFIX:${PRIORITY^^}"
CONTEXT_PREFIX="$CONTEXT_PREFIX]"

# Output JSON for Cursor hook system
jq -n \
  --arg context "$CONTEXT_PREFIX $MSG" \
  --arg priority "$PRIORITY" \
  '{
    "hookSpecificOutput": {
      "hookEventName": "preToolUse",
      "additionalContext": $context,
      "metadata": {
        "source": "durable-request/steering",
        "priority": $priority
      }
    }
  }'

exit 0
```

### 2. Hook 配置 (`hooks.json`)

**用户级 (`~/.cursor/hooks.json`):**

```json
{
  "version": 1,
  "hooks": {
    "preToolUse": [
      {
        "command": "~/.cursor/hooks/steering-hook.sh",
        "timeout_ms": 2000
      }
    ]
  }
}
```

**项目级 (`.cursor/hooks.json`):**

```json
{
  "version": 1,
  "hooks": {
    "preToolUse": [
      {
        "command": ".cursor/hooks/steering-hook.sh",
        "timeout_ms": 2000
      }
    ]
  }
}
```

### 3. Shell 命令 (`steer`)

**添加到 `~/.bashrc` 或 `~/.zshrc`:**

```bash
# Cursor steering command
steer() {
  local STEERING_FILE="${CURSOR_STEERING_FILE:-$HOME/.cursor/steering-message}"
  
  if [ $# -eq 0 ]; then
    echo "Usage: steer <message>"
    echo "       steer '!!! URGENT: stop current task'"
    echo "       steer 'focus on the API layer instead'"
    echo ""
    echo "Priority prefixes:"
    echo "  !!!  or URGENT: or STOP:  → Critical (immediate action)"
    echo "  !!   or ASAP:             → High priority"
    echo "  (none)                    → Normal steering"
    return 1
  fi
  
  echo "$*" > "$STEERING_FILE"
  echo "[steering] Message queued: $*"
  echo "[steering] Will be processed at next tool call"
}

# Quick aliases
alias steer-stop='steer "!!! STOP: Abort current task immediately"'
alias steer-focus='steer "Focus on"'
alias steer-skip='steer "Skip this step and"'
```

### 4. 安装脚本 (`install-steering.sh`)

```bash
#!/bin/bash
# Install Cursor steering mechanism for durable-request

set -euo pipefail

HOOK_DIR="$HOME/.cursor/hooks"
HOOKS_JSON="$HOME/.cursor/hooks.json"

echo "Installing Cursor steering mechanism..."

# Create directories
mkdir -p "$HOOK_DIR"

# Install hook script
cat > "$HOOK_DIR/steering-hook.sh" << 'HOOK_EOF'
#!/bin/bash
STEERING_FILE="${CURSOR_STEERING_FILE:-$HOME/.cursor/steering-message}"
[ -f "$STEERING_FILE" ] || exit 0
MSG=$(cat "$STEERING_FILE" 2>/dev/null || echo "")
[ -z "$MSG" ] && { rm -f "$STEERING_FILE"; exit 0; }
rm -f "$STEERING_FILE"

PRIORITY="normal"
case "$MSG" in
  "!!!"*|"URGENT:"*|"STOP:"*) PRIORITY="critical" ;;
  "!!"*|"ASAP:"*) PRIORITY="high" ;;
esac

jq -n --arg context "⚡ [STEERING:${PRIORITY^^}] $MSG" '{
  "hookSpecificOutput": {
    "hookEventName": "preToolUse",
    "additionalContext": $context
  }
}'
exit 0
HOOK_EOF

chmod +x "$HOOK_DIR/steering-hook.sh"

# Merge hooks.json
if [ -f "$HOOKS_JSON" ]; then
  # Backup existing
  cp "$HOOKS_JSON" "$HOOKS_JSON.bak"
  
  # Merge new hook
  jq '.hooks.preToolUse = (.hooks.preToolUse // []) + [{"command": "~/.cursor/hooks/steering-hook.sh", "timeout_ms": 2000}] | .hooks.preToolUse |= unique_by(.command)' \
    "$HOOKS_JSON" > "$HOOKS_JSON.tmp" && mv "$HOOKS_JSON.tmp" "$HOOKS_JSON"
else
  # Create new
  cat > "$HOOKS_JSON" << 'JSON_EOF'
{
  "version": 1,
  "hooks": {
    "preToolUse": [
      {
        "command": "~/.cursor/hooks/steering-hook.sh",
        "timeout_ms": 2000
      }
    ]
  }
}
JSON_EOF
fi

# Add shell aliases
SHELL_RC="$HOME/.bashrc"
[ -n "${ZSH_VERSION:-}" ] && SHELL_RC="$HOME/.zshrc"

if ! grep -q "CURSOR_STEERING" "$SHELL_RC" 2>/dev/null; then
  cat >> "$SHELL_RC" << 'ALIAS_EOF'

# Cursor steering (durable-request)
steer() {
  local STEERING_FILE="${CURSOR_STEERING_FILE:-$HOME/.cursor/steering-message}"
  [ $# -eq 0 ] && { echo "Usage: steer <message>"; return 1; }
  echo "$*" > "$STEERING_FILE"
  echo "[steering] Queued: $*"
}
alias steer-stop='steer "!!! STOP: Abort current task"'
ALIAS_EOF
fi

echo "✓ Steering hook installed to $HOOK_DIR/steering-hook.sh"
echo "✓ Hooks config updated: $HOOKS_JSON"
echo "✓ Shell aliases added to $SHELL_RC"
echo ""
echo "Restart your shell or run: source $SHELL_RC"
echo ""
echo "Usage:"
echo "  steer 'focus on the API layer'"
echo "  steer '!!! STOP: urgent production issue'"
```

---

## SKILL.md 集成

### 更新 Checkpoint 机制

在 `SKILL.md` 中添加 steering 检查:

```markdown
### Step 2.5: Check for Steering Messages (Cursor IDE)

Before presenting a checkpoint, check if a steering message was injected:

1. Look for `⚡ [STEERING]` or `⚡ [STEERING:CRITICAL]` in your recent context
2. If present, treat it as a high-priority user instruction
3. Acknowledge the steering in your response and adjust your plan

Example:
> **[durable-request]** Received steering message: "focus on API layer". Adjusting current task...

Steering priorities:
- **CRITICAL**: Immediate action required, may skip current checkpoint
- **HIGH**: Process before continuing, but complete current atomic operation
- **NORMAL**: Incorporate into next decision point
```

---

## 安装方案

### 文件结构

```
~/.durable-request/
├── bin/
│   └── steer              # CLI 工具
├── hooks/
│   └── steering-hook.sh   # PreToolUse hook 脚本
├── data/
│   └── steering-message   # 当前 steering 消息 (临时)
└── config/
    └── steering.json      # 配置 (可选)
```

### 安装脚本

```bash
#!/bin/bash
# install-steering.sh

INSTALL_DIR="${HOME}/.durable-request"

# 创建目录
mkdir -p "$INSTALL_DIR"/{bin,hooks,data,config}

# 安装 steer CLI
cat > "$INSTALL_DIR/bin/steer" << 'STEER_EOF'
#!/bin/bash
# steer - Send steering message to durable-request agent

DATA_DIR="${HOME}/.durable-request/data"
STEERING_FILE="$DATA_DIR/steering-message"

usage() {
  echo "Usage: steer <message>"
  echo "       steer --clear"
  echo "       steer --status"
  echo ""
  echo "Send a steering message to the running agent."
  echo "The message will be injected at the next tool call."
}

case "${1:-}" in
  -h|--help)
    usage
    exit 0
    ;;
  --clear)
    rm -f "$STEERING_FILE"
    echo "[steer] Queue cleared"
    exit 0
    ;;
  --status)
    if [ -f "$STEERING_FILE" ]; then
      echo "[steer] Pending: $(cat "$STEERING_FILE")"
    else
      echo "[steer] No pending steering message"
    fi
    exit 0
    ;;
  "")
    usage
    exit 1
    ;;
  *)
    mkdir -p "$DATA_DIR"
    echo "$*" > "$STEERING_FILE"
    echo "[steer] Queued: $*"
    echo "[steer] Will be processed at next tool call"
    ;;
esac
STEER_EOF

chmod +x "$INSTALL_DIR/bin/steer"

# 创建 symlink
if [ -w /usr/local/bin ]; then
  ln -sf "$INSTALL_DIR/bin/steer" /usr/local/bin/steer
  echo "✓ Installed: /usr/local/bin/steer"
else
  echo "⚠ Cannot write to /usr/local/bin. Add to PATH manually:"
  echo "  export PATH=\"$INSTALL_DIR/bin:\$PATH\""
fi

# 安装 hook 脚本
cat > "$INSTALL_DIR/hooks/steering-hook.sh" << 'HOOK_EOF'
#!/bin/bash
# PreToolUse hook for steering injection

STEERING_FILE="${HOME}/.durable-request/data/steering-message"

# 无文件则退出
[ -f "$STEERING_FILE" ] || exit 0

# 读取并验证
MSG=$(cat "$STEERING_FILE" 2>/dev/null || echo "")
[ -z "$MSG" ] && { rm -f "$STEERING_FILE"; exit 0; }

# 消费消息
rm -f "$STEERING_FILE"

# 输出 hook 响应
jq -n --arg msg "$MSG" '{
  "hookSpecificOutput": {
    "hookEventName": "preToolUse",
    "additionalContext": ("⚡ [USER STEERING]: " + $msg)
  }
}'
exit 0
HOOK_EOF

chmod +x "$INSTALL_DIR/hooks/steering-hook.sh"

echo "✓ Steering hook installed"
echo ""
echo "To enable in Cursor, add to ~/.cursor/hooks.json:"
echo '  "preToolUse": [{"command": "~/.durable-request/hooks/steering-hook.sh"}]'
```

## 已知限制

1. **延迟**: Steering 只在下一个工具调用时被处理，不是真正的实时
2. **Context 注入 bug**: 有社区报告 `additional_context` 有时不被正确传递
3. **单消息**: 同时只能有一条 steering message (后写覆盖前写)
4. **需要 jq**: 依赖 `jq` 生成 JSON 输出
5. **需要额外终端**: 用户需要在另一个终端窗口执行 `steer` 命令

## 测试计划

1. **基础功能测试**
   - 发送简单 steering message
   - 验证 hook 被触发
   - 确认 context 注入到 agent

2. **优先级测试**
   - 测试 `!!!` 前缀
   - 测试 `URGENT:` 前缀
   - 验证 priority metadata

3. **边界情况**
   - 空消息处理
   - 超长消息处理
   - 特殊字符处理
   - 并发写入

4. **集成测试**
   - 与 durable-request checkpoint 配合
   - 与其他 hooks 兼容性
   - 跨 session 行为

---

## 与 Claude Code 对比

| 特性 | Claude Code (Feature Request) | Cursor (Hook-based) |
|------|-------------------------------|---------------------|
| 实现状态 | ❌ 未实现 | ✅ 可实现 |
| 注入时机 | Tool call boundary | PreToolUse hook |
| 用户输入 | stdin / file | file (`steer` command) |
| 优先级支持 | 提案中 | ✅ 通过前缀 |
| 非破坏性 | 提案中 | ✅ 不中断 agent |
| IDE 集成 | 原生 (目标) | Hook (workaround) |

---

## 未来方案: Cursor 扩展开发

### 可行性分析

Cursor 基于 VSCode 二次开发，**兼容大部分 VSCode 扩展 API**。这意味着我们可以开发一个 Cursor/VSCode 扩展来提供更好的 steering UX。

### 扩展功能设计

```
┌─────────────────────────────────────────────────────────────┐
│  durable-request Steering Extension                          │
│                                                              │
│  [状态栏按钮] ──▶ 点击弹出输入框                               │
│       │                                                      │
│       ▼                                                      │
│  [InputBox] ──▶ 用户输入 steering message                    │
│       │                                                      │
│       ▼                                                      │
│  [写入文件] ──▶ ~/.durable-request/data/steering-message     │
│       │                                                      │
│       ▼                                                      │
│  [显示通知] ──▶ "Steering queued: ..."                       │
│                                                              │
│  (Hook 在下次工具调用时读取文件并注入 context)                 │
└─────────────────────────────────────────────────────────────┘
```

### 技术实现

**1. 状态栏按钮**

```typescript
// extension.ts
import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';

export function activate(context: vscode.ExtensionContext) {
  // 状态栏按钮
  const steerButton = vscode.window.createStatusBarItem(
    vscode.StatusBarAlignment.Right, 100
  );
  steerButton.text = "$(megaphone) Steer";
  steerButton.tooltip = "Send steering message to agent";
  steerButton.command = 'durable-request.steer';
  steerButton.show();

  // 注册命令
  const steerCommand = vscode.commands.registerCommand(
    'durable-request.steer',
    async () => {
      const message = await vscode.window.showInputBox({
        prompt: 'Enter steering message',
        placeHolder: 'e.g., "focus on the API layer"'
      });
      
      if (message) {
        const steeringDir = path.join(
          process.env.HOME || '', 
          '.durable-request', 'data'
        );
        fs.mkdirSync(steeringDir, { recursive: true });
        fs.writeFileSync(
          path.join(steeringDir, 'steering-message'), 
          message
        );
        vscode.window.showInformationMessage(
          `Steering queued: ${message}`
        );
      }
    }
  );

  context.subscriptions.push(steerButton, steerCommand);
}
```

**2. package.json**

```json
{
  "name": "durable-request-steer",
  "displayName": "Durable Request Steering",
  "description": "Send steering messages to AI agents mid-execution",
  "version": "0.1.0",
  "engines": { "vscode": "^1.85.0" },
  "categories": ["Other"],
  "activationEvents": ["onStartupFinished"],
  "main": "./out/extension.js",
  "contributes": {
    "commands": [{
      "command": "durable-request.steer",
      "title": "Steer Agent",
      "category": "Durable Request"
    }],
    "keybindings": [{
      "command": "durable-request.steer",
      "key": "ctrl+shift+s",
      "mac": "cmd+shift+s"
    }]
  }
}
```

### 兼容性注意事项

| 问题 | 状态 | 说明 |
|------|------|------|
| 基础 API 兼容 | ✅ | StatusBar, InputBox, Commands 均可用 |
| 文件系统访问 | ✅ | `fs` 模块正常工作 |
| 微软官方扩展限制 | ⚠️ | 不影响，我们是自定义扩展 |
| Cursor 扩展市场 | ⚠️ | 可能需要手动 .vsix 安装 |

### 开发优先级

1. **Phase 1 (当前)**: 纯文件方案 + `steer` CLI
2. **Phase 2 (未来)**: Cursor 扩展 + 状态栏按钮
3. **Phase 3 (理想)**: 等待 Cursor 修复 hook bug，实现 Chat 输入框 steering

---

*设计日期: 2026-04-14*
*更新日期: 2026-04-14 (添加扩展开发可行性分析)*
