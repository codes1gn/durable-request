# Cursor IDE Steering Implementation Design

## 概述

本文档详细设计 Cursor IDE 上的 steering-in-continuation 实现方案。

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

## 已知限制

1. **延迟**: Steering 只在下一个工具调用时被处理，不是真正的实时
2. **Context 注入 bug**: 有社区报告 `additional_context` 有时不被正确传递
3. **单消息**: 同时只能有一条 steering message (后写覆盖前写)
4. **需要 jq**: 依赖 `jq` 生成 JSON 输出

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

*设计日期: 2026-04-14*
