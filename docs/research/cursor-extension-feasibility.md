# Cursor Steering Extension - 技术可行性分析

## 概述

本文档分析开发一个 Cursor/VSCode 扩展的可行性，该扩展将提供一个独立的 steering UI（绕开默认的 Chat 消息框），直接写入监控文件供 hook 读取。

## 目标

```
┌─────────────────────────────────────────────────────────────┐
│  用户体验目标                                                 │
│                                                              │
│  [状态栏 Steer 按钮] ──▶ 点击                                 │
│         │                                                    │
│         ▼                                                    │
│  [输入框弹出] ──▶ 输入 steering message                       │
│         │                                                    │
│         ▼                                                    │
│  [直接写入文件] ──▶ ~/.durable-request/data/steering-message │
│         │                                                    │
│         ▼                                                    │
│  [通知显示] ──▶ "Steering queued: ..."                        │
│                                                              │
│  ✅ 绕开 Chat 消息框                                          │
│  ✅ 不触发新 request                                          │
│  ✅ preToolUse hook 在下次工具调用时读取                      │
└─────────────────────────────────────────────────────────────┘
```

## 技术可行性分析

### 1. Cursor 兼容性

| 功能 | VSCode API | Cursor 兼容性 | 状态 |
|------|-----------|---------------|------|
| StatusBar 状态栏 | `vscode.window.createStatusBarItem` | ✅ 完全兼容 | 可用 |
| InputBox 输入框 | `vscode.window.showInputBox` | ✅ 完全兼容 | 可用 |
| Command 命令 | `vscode.commands.registerCommand` | ✅ 完全兼容 | 可用 |
| File System | `vscode.workspace.fs` / `fs` module | ✅ 完全兼容 | 可用 |
| Notification | `vscode.window.showInformationMessage` | ✅ 完全兼容 | 可用 |
| Keybinding | `contributes.keybindings` | ✅ 完全兼容 | 可用 |

**结论**: 所有需要的 API 都与 Cursor 兼容。

### 2. 核心组件实现

#### 2.1 StatusBar 按钮

```typescript
import * as vscode from 'vscode';

export function createSteerButton(context: vscode.ExtensionContext) {
  // 创建状态栏按钮
  const steerButton = vscode.window.createStatusBarItem(
    vscode.StatusBarAlignment.Right,
    100 // 优先级，数字越大越靠左
  );
  
  steerButton.text = "$(megaphone) Steer"; // 使用 Codicon 图标
  steerButton.tooltip = "Send steering message to agent (Ctrl+Shift+S)";
  steerButton.command = 'durable-request.steer';
  steerButton.backgroundColor = new vscode.ThemeColor(
    'statusBarItem.warningBackground'
  );
  steerButton.show();
  
  context.subscriptions.push(steerButton);
  return steerButton;
}
```

#### 2.2 InputBox 输入框

```typescript
async function showSteeringInput(): Promise<string | undefined> {
  return vscode.window.showInputBox({
    prompt: 'Enter steering message for the agent',
    placeHolder: 'e.g., "focus on the API layer" or "skip tests"',
    ignoreFocusOut: true, // 点击其他区域不关闭
    validateInput: (value) => {
      if (!value.trim()) {
        return 'Please enter a message';
      }
      return null; // 验证通过
    }
  });
}
```

#### 2.3 文件写入

```typescript
import * as fs from 'fs';
import * as path from 'path';

const STEERING_DIR = path.join(
  process.env.HOME || process.env.USERPROFILE || '',
  '.durable-request',
  'data'
);
const STEERING_FILE = path.join(STEERING_DIR, 'steering-message');

function writeSteeringMessage(message: string): void {
  // 确保目录存在
  fs.mkdirSync(STEERING_DIR, { recursive: true });
  
  // 写入消息
  fs.writeFileSync(STEERING_FILE, message, 'utf-8');
}

function readSteeringMessage(): string | null {
  try {
    if (fs.existsSync(STEERING_FILE)) {
      return fs.readFileSync(STEERING_FILE, 'utf-8');
    }
  } catch {
    // ignore
  }
  return null;
}

function clearSteeringMessage(): void {
  try {
    fs.unlinkSync(STEERING_FILE);
  } catch {
    // ignore
  }
}
```

#### 2.4 完整扩展入口

```typescript
// extension.ts
import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';

const STEERING_DIR = path.join(
  process.env.HOME || process.env.USERPROFILE || '',
  '.durable-request', 'data'
);
const STEERING_FILE = path.join(STEERING_DIR, 'steering-message');

export function activate(context: vscode.ExtensionContext) {
  console.log('durable-request-steer extension activated');

  // 1. 创建状态栏按钮
  const steerButton = vscode.window.createStatusBarItem(
    vscode.StatusBarAlignment.Right, 100
  );
  steerButton.text = "$(megaphone) Steer";
  steerButton.tooltip = "Send steering message to agent (Ctrl+Shift+S)";
  steerButton.command = 'durable-request.steer';
  steerButton.show();

  // 2. 注册 steer 命令
  const steerCommand = vscode.commands.registerCommand(
    'durable-request.steer',
    async () => {
      // 显示输入框
      const message = await vscode.window.showInputBox({
        prompt: 'Enter steering message for the agent',
        placeHolder: 'e.g., "focus on API layer" or "skip tests"',
        ignoreFocusOut: true,
        validateInput: (v) => v.trim() ? null : 'Please enter a message'
      });

      if (!message) {
        return; // 用户取消
      }

      try {
        // 写入文件
        fs.mkdirSync(STEERING_DIR, { recursive: true });
        fs.writeFileSync(STEERING_FILE, message.trim(), 'utf-8');

        // 显示通知
        vscode.window.showInformationMessage(
          `⚡ Steering queued: "${message.trim()}"`
        );

        // 临时改变按钮外观表示有 pending steering
        steerButton.text = "$(megaphone) Steering...";
        steerButton.backgroundColor = new vscode.ThemeColor(
          'statusBarItem.errorBackground'
        );

        // 5秒后恢复
        setTimeout(() => {
          steerButton.text = "$(megaphone) Steer";
          steerButton.backgroundColor = undefined;
        }, 5000);

      } catch (err) {
        vscode.window.showErrorMessage(
          `Failed to queue steering: ${err}`
        );
      }
    }
  );

  // 3. 注册 clear 命令
  const clearCommand = vscode.commands.registerCommand(
    'durable-request.clearSteering',
    () => {
      try {
        if (fs.existsSync(STEERING_FILE)) {
          fs.unlinkSync(STEERING_FILE);
          vscode.window.showInformationMessage('Steering cleared');
        } else {
          vscode.window.showInformationMessage('No pending steering');
        }
      } catch (err) {
        vscode.window.showErrorMessage(`Failed to clear: ${err}`);
      }
    }
  );

  // 4. 注册 status 命令
  const statusCommand = vscode.commands.registerCommand(
    'durable-request.steeringStatus',
    () => {
      try {
        if (fs.existsSync(STEERING_FILE)) {
          const msg = fs.readFileSync(STEERING_FILE, 'utf-8');
          vscode.window.showInformationMessage(
            `Pending steering: "${msg}"`
          );
        } else {
          vscode.window.showInformationMessage('No pending steering');
        }
      } catch (err) {
        vscode.window.showErrorMessage(`Failed to check: ${err}`);
      }
    }
  );

  context.subscriptions.push(
    steerButton,
    steerCommand,
    clearCommand,
    statusCommand
  );
}

export function deactivate() {}
```

### 3. package.json 配置

```json
{
  "name": "durable-request-steer",
  "displayName": "Durable Request Steering",
  "description": "Send steering messages to AI agents mid-execution",
  "version": "0.1.0",
  "publisher": "durable-request",
  "engines": {
    "vscode": "^1.85.0"
  },
  "categories": ["Other"],
  "keywords": ["ai", "agent", "steering", "copilot", "cursor"],
  "activationEvents": ["onStartupFinished"],
  "main": "./out/extension.js",
  "contributes": {
    "commands": [
      {
        "command": "durable-request.steer",
        "title": "Steer Agent",
        "category": "Durable Request",
        "icon": "$(megaphone)"
      },
      {
        "command": "durable-request.clearSteering",
        "title": "Clear Steering",
        "category": "Durable Request"
      },
      {
        "command": "durable-request.steeringStatus",
        "title": "Steering Status",
        "category": "Durable Request"
      }
    ],
    "keybindings": [
      {
        "command": "durable-request.steer",
        "key": "ctrl+shift+s",
        "mac": "cmd+shift+s",
        "when": "editorTextFocus"
      }
    ],
    "menus": {
      "commandPalette": [
        {
          "command": "durable-request.steer",
          "when": "true"
        },
        {
          "command": "durable-request.clearSteering",
          "when": "true"
        },
        {
          "command": "durable-request.steeringStatus",
          "when": "true"
        }
      ]
    }
  },
  "scripts": {
    "vscode:prepublish": "npm run compile",
    "compile": "tsc -p ./",
    "watch": "tsc -watch -p ./",
    "package": "vsce package"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/vscode": "^1.85.0",
    "typescript": "^5.0.0",
    "@vscode/vsce": "^2.22.0"
  }
}
```

### 4. 项目结构

```
durable-request-steer/
├── src/
│   └── extension.ts
├── package.json
├── tsconfig.json
├── .vscodeignore
└── README.md
```

### 5. 安装方式

#### 5.1 开发模式

```bash
cd durable-request-steer
npm install
npm run compile
# 按 F5 启动调试
```

#### 5.2 打包发布

```bash
npm run package
# 生成 durable-request-steer-0.1.0.vsix
```

#### 5.3 在 Cursor 中安装

```bash
# 方法 1: 命令面板
# Extensions: Install from VSIX...

# 方法 2: 命令行
cursor --install-extension durable-request-steer-0.1.0.vsix
```

## 与 CLI 方案对比

| 特性 | CLI (steer 命令) | Extension (状态栏按钮) |
|------|------------------|------------------------|
| 安装复杂度 | 低 (单脚本) | 中 (需要打包 vsix) |
| 用户体验 | 需要终端窗口 | IDE 内直接操作 |
| 快捷键支持 | 无 | ✅ Ctrl+Shift+S |
| 视觉反馈 | 终端输出 | ✅ 状态栏 + 通知 |
| 跨平台 | ✅ | ✅ |
| 与 IDE 集成 | 无 | ✅ 命令面板、菜单 |

## 结论

**技术上完全可行**，且能提供比 CLI 更好的用户体验：

1. ✅ 所有需要的 VSCode API 都与 Cursor 兼容
2. ✅ 不依赖 Chat 消息框，直接写入文件
3. ✅ 支持快捷键 (Ctrl+Shift+S)
4. ✅ 提供视觉反馈（状态栏变色、通知）
5. ✅ 可通过命令面板访问

## 下一步

1. 创建扩展项目骨架
2. 实现核心功能
3. 测试在 Cursor 中的兼容性
4. 打包并发布

---

*分析日期: 2026-04-14*
