# Durable Request 改进调研报告

## 概述

本报告调研两个改进方向：
1. **GitHub Copilot (VSCode)** 是否有内置的交互式问答工具
2. **Steering in-continuation** 在 Cursor IDE 上的实现方式

---

## 1. GitHub Copilot VSCode — `askQuestions` 工具

### 发现

**是的，Copilot 在 VSCode 中已有内置的 `askQuestions` 工具。**

根据 VS Code 1.110 版本 (2026年2月发布) 的更新日志：

> The `askQuestions` tool, which presents a **question carousel UI** during chat interactions, has been moved into VS Code core. This improves reliability when canceling requests and enables the tool to work consistently across different contexts, including subagents.

### 关键特性

| 特性 | 描述 |
|------|------|
| **Question Carousel UI** | 在聊天过程中呈现问题轮播界面 |
| **VS Code Core 集成** | 已移入 VS Code 核心，非扩展层 |
| **Subagent 支持** | 在所有上下文（包括子代理）中一致工作 |
| **Steering 支持** | 当轮播激活时，可发送 steering message 而无需先回复或关闭问题 |
| **键盘导航** | `Alt+N` (下一题) / `Alt+P` (上一题) |
| **取消可靠性** | 改进了取消请求时的可靠性 |

### Steering 集成 (已原生支持!)

VS Code 1.110 文档明确指出：

> When the carousel is active, you can now send a **steering message without needing to reply to or dismiss pending questions first**. This allows you to redirect the agent's response on the fly, even in the middle of a question sequence.

这意味着 Copilot 的 `askQuestions` 工具已经**原生支持 steering-in-continuation**。

### Steering 计费影响 ⚠️

**重要: Steering message 会产生额外 Premium Request 费用!**

根据 [GitHub Copilot Requests 文档](https://docs.github.com/en/copilot/concepts/billing/copilot-requests):

| 行为 | 计费 |
|------|------|
| 启动 Agent 任务 | 1 × Premium Request × Model Multiplier |
| 发送 Steering Message | 1 × Premium Request × Model Multiplier |
| Agent 自主工具调用 | 免费 (不额外计费) |

**模型倍率示例:**
- GPT-5 mini, GPT-4.1, GPT-4o: 0x (基础模型，不消耗额度)
- Claude Sonnet 4.5: 1x
- Claude Opus 4.6: 3x
- GPT-5.2: 2x

**月度配额:**
- Free: 50 Premium Requests/月
- Pro ($10/月): 300 Premium Requests/月
- Pro+ ($39/月): 1,500 Premium Requests/月
- Business: 300/用户/月
- Enterprise: 1,000/用户/月

**超额处理:** 超出配额后:
1. 默认: 回退到基础模型 (不消耗额度)
2. 如启用 "Premium request paid usage": $0.04/请求

**对 durable-request 的影响:**
- durable-request 的 checkpoint 模式**不会触发 steering 计费**，因为 checkpoint 使用 `askQuestions` 工具本身，而非发送 steering message
- 只有当用户在 question carousel 激活时主动输入新指令时才计费
- 建议: 在文档中说明此行为，让用户知晓

### 对 durable-request 的影响

1. **可以支持 Copilot IDE**: 添加 `askQuestions` 作为新的 checkpoint 工具选项
2. **环境检测**:
   - 如果运行在 VS Code + Copilot 环境中
   - 检测 `askQuestions` 工具可用性
   - 调用方式可能与 Cursor 的 `AskQuestion` 类似

### 待确认

- `askQuestions` 的确切调用 schema (是否与 Cursor 的 `AskQuestion` 相同?)
- 是否需要特定的 Copilot 版本或 VS Code 设置
- 是否有公开的 API 文档

---

## 2. Steering in-Continuation — Cursor IDE 实现方案

### 当前状态

**Cursor IDE 目前不支持原生的 mid-execution steering。**

根据调研：
- 中断 agent (点击 Stop) 会执行**破坏性回滚**，撤销已完成的更改
- 用户在 agent 运行期间输入的指令会被**排队**，直到当前回合结束才处理
- 没有原生的 "priority message channel" 机制

### 可行的实现方案

#### 方案 A: Hook-based Steering (推荐)

Cursor 支持 `PreToolUse` hook，可以在每次工具调用前检查用户输入。

**实现原理:**

```
┌────────────────────────────────────────────────────────────────┐
│                     Agent Turn (Running)                        │
│                                                                │
│   Tool 1 ──▶ PreToolUse Hook ──▶ Check steering file ──▶ Tool 2│
│                     │                                           │
│                     ▼                                           │
│              Steering file exists?                              │
│              ├─ YES: Inject as additional_context               │
│              │       Clear file                                 │
│              │       Agent sees: "⚡ PRIORITY: <user msg>"      │
│              └─ NO:  Continue normally                          │
└────────────────────────────────────────────────────────────────┘
```

**实现步骤:**

1. **创建 steering hook** (`.cursor/hooks/steering-hook.sh`):

```bash
#!/bin/bash
STEERING_FILE="${HOME}/.cursor/steering-message"

[ -f "$STEERING_FILE" ] || exit 0

MSG=$(cat "$STEERING_FILE")
rm -f "$STEERING_FILE"
[ -z "$MSG" ] && exit 0

jq -n --arg m "$MSG" '{
  "hookSpecificOutput": {
    "hookEventName": "preToolUse",
    "additionalContext": "⚡ STEERING: " + $m
  }
}'
exit 0
```

2. **配置 hooks.json** (`.cursor/hooks.json`):

```json
{
  "version": 1,
  "hooks": {
    "preToolUse": [
      {
        "command": ".cursor/hooks/steering-hook.sh"
      }
    ]
  }
}
```

3. **提供 steering 命令** (`steer` alias):

```bash
# 添加到 ~/.bashrc
steer() {
  echo "$*" > ~/.cursor/steering-message
  echo "[steering] Message queued: $*"
}
```

4. **使用方式**:

```bash
# 在另一个终端中，agent 正在运行时
steer "Skip the tests, focus on implementation"
steer "Stop current task, urgent bug in production"
```

**优点:**
- 利用现有的 hook 机制，无需等待官方支持
- 非破坏性 — agent 在下一个工具调用时看到 steering message
- 与 Claude Code 的 hook 系统兼容

**缺点:**
- 需要额外终端窗口输入
- 不是实时的 — 需等到下一个工具调用
- 某些场景下 `additional_context` 可能未被正确处理 (已有 bug 报告)

#### 方案 B: 轮询式 Steering (备选)

如果 hook 方案不稳定，可以用轮询方式：

```
┌─────────────────────────────────────────────────────────────────┐
│  Durable Checkpoint Loop                                        │
│                                                                 │
│  ┌─────────┐   ┌─────────────────┐   ┌─────────────────────────┐│
│  │ Do Work │──▶│ Check Steering  │──▶│ Present Checkpoint      ││
│  │         │   │ File            │   │ (with steering context) ││
│  └─────────┘   └─────────────────┘   └─────────────────────────┘│
│       ▲                                         │               │
│       │                                         │               │
│       └─────────────────────────────────────────┘               │
└─────────────────────────────────────────────────────────────────┘
```

在每个 checkpoint 前检查 steering file，如果存在则:
- 将 steering message 注入到 checkpoint prompt 中
- 或直接作为用户选择处理

#### 方案 C: AskQuestion 内的 Steering (当前可用)

VS Code 1.110 更新提到 Copilot 的 `askQuestions` 已支持 steering:

> When the carousel is active, you can now send a steering message without needing to reply to or dismiss pending questions first.

**问题:** Cursor 的 `AskQuestion` 是否也支持此行为?

根据 VS Code 1.110 更新，`askQuestions` 已移入 VS Code core。如果 Cursor 基于较新的 VS Code，可能已继承此功能。

**测试方法:**
1. 触发一个 `AskQuestion` checkpoint
2. 在 carousel 激活时，尝试在聊天输入框中输入新指令
3. 观察 agent 是否响应 steering message

### 综合建议

| 优先级 | 方案 | 工作量 | 可行性 |
|--------|------|--------|--------|
| 1 | 测试 Cursor AskQuestion 是否已支持 steering | 低 | 高 |
| 2 | Hook-based steering (PreToolUse) | 中 | 中-高 |
| 3 | 等待 Cursor 官方 steering API | 无 | 未知 |

---

## 3. 对比总结: 各平台 Steering 支持

| 平台 | 原生 Steering | Hook-based Steering | Checkpoint 中 Steering |
|------|---------------|---------------------|------------------------|
| **VS Code + Copilot** | ✅ (1.110+) | ✅ | ✅ |
| **Cursor IDE** | ❌ | ✅ (PreToolUse hook) | ❓ 待测试 |
| **Claude Code** | ❌ (Feature Request) | ✅ (workaround) | ❌ |
| **OpenCode** | ❌ | ✅ | ❌ |

---

## 4. 下一步行动

### 已完成 ✅

1. **添加 Copilot IDE 支持**
   - ✅ 调研 `#vscode/askQuestions` 的调用 schema
   - ✅ 在 SKILL.md 中添加 Copilot 环境检测
   - ✅ 添加 `#vscode/askQuestions` checkpoint 调用示例
   - ✅ 添加 Copilot 计费说明

### 待后续实现 (Steering)

Steering 功能调研已完成并记录，暂时搁置以专注于基础 checkpoint 支持。

2. **验证 Cursor AskQuestion steering**
   - 创建测试用例，在 checkpoint 激活时发送 steering message
   - 记录行为，确认是否与 Copilot 一致

3. **实现 Hook-based steering for Cursor**
   - 创建 `steering-hook.sh`
   - 配置 `.cursor/hooks.json`
   - 添加 `steer` shell alias
   - 详细设计见 `cursor-steering-implementation.md`

4. **统一 steering 接口**
   - 定义 `steering-message` 文件格式
   - 跨平台兼容: Cursor, Claude Code, OpenCode
   - 在 durable-request skill 中集成 steering 检查

5. **更新 Roadmap**
   - 将 "Steering in continuation" 从 planned 改为 in_progress
   - 添加具体实现里程碑

---

## 参考资料

1. [VS Code 1.110 Release Notes](https://code.visualstudio.com/updates/v1_110)
2. [Cursor Third-party Hooks Documentation](https://cursor.com/cn/docs/reference/third-party-hooks)
3. [Claude Code Real-time Steering Feature Request #30492](https://github.com/anthropics/claude-code/issues/30492)
4. [Cursor Forum: Interrupting agent mid-work](https://forum.cursor.com/t/interrupting-the-agent-mid-work-automatically-reverts-all-work-done-so-far-this-is-a-bad-bad-idea/141284)

---

*调研日期: 2026-04-14*
