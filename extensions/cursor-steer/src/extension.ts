import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';

const DEFAULT_STEERING_DIR = path.join(os.homedir(), '.durable-request', 'data');
const STEERING_FILENAME = 'steering-message';

let steerButton: vscode.StatusBarItem;
let pollInterval: NodeJS.Timeout | null = null;

function getSteeringDir(): string {
  const config = vscode.workspace.getConfiguration('durableRequest');
  const customDir = config.get<string>('steeringDataDir');
  return customDir && customDir.trim() ? customDir.trim() : DEFAULT_STEERING_DIR;
}

function getSteeringFilePath(): string {
  return path.join(getSteeringDir(), STEERING_FILENAME);
}

function ensureSteeringDir(): void {
  const dir = getSteeringDir();
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

function writeSteeringMessage(message: string): void {
  ensureSteeringDir();
  fs.writeFileSync(getSteeringFilePath(), message, 'utf-8');
}

function readSteeringMessage(): string | null {
  const filePath = getSteeringFilePath();
  try {
    if (fs.existsSync(filePath)) {
      return fs.readFileSync(filePath, 'utf-8');
    }
  } catch {
    // ignore read errors
  }
  return null;
}

function clearSteeringMessage(): boolean {
  const filePath = getSteeringFilePath();
  try {
    if (fs.existsSync(filePath)) {
      fs.unlinkSync(filePath);
      return true;
    }
  } catch {
    // ignore delete errors
  }
  return false;
}

function updateButtonState(pending: boolean, message?: string): void {
  if (!steerButton) {
    return;
  }

  if (pending) {
    const label = message ? ` — "${message}"` : '';
    steerButton.text = `$(megaphone) Steering pending${label}`;
    steerButton.backgroundColor = new vscode.ThemeColor('statusBarItem.warningBackground');
    steerButton.tooltip = message
      ? `Steering pending: "${message}"\nWill be consumed at agent's next Shell call`
      : "Steering message pending — will be consumed at agent's next Shell call";
  } else {
    steerButton.text = "$(megaphone) Steer";
    steerButton.backgroundColor = undefined;
    steerButton.tooltip = "Send steering message to agent";
  }
}

function checkPendingSteering(): void {
  const message = readSteeringMessage();
  const pending = message !== null && message.trim().length > 0;
  updateButtonState(pending, pending ? message!.trim() : undefined);
  adjustPollRate(pending);
}

function adjustPollRate(pendingNow: boolean): void {
  if (!pollInterval) {
    return;
  }
  // Fast polling (1 s) while a message is pending so the button clears promptly;
  // slow polling (5 s) when idle. Restart only if the rate needs to change.
  const currentMs = (pollInterval as any).__intervalMs as number | undefined;
  const targetMs = pendingNow ? 1000 : 5000;
  if (currentMs !== targetMs) {
    clearInterval(pollInterval);
    pollInterval = setInterval(() => checkPendingSteering(), targetMs);
    (pollInterval as any).__intervalMs = targetMs;
  }
}

export function activate(context: vscode.ExtensionContext): void {
  console.log('[durable-request-steer] Extension activated');

  const config = vscode.workspace.getConfiguration('durableRequest');

  // Create status bar button
  if (config.get<boolean>('showStatusBarButton', true)) {
    steerButton = vscode.window.createStatusBarItem(
      vscode.StatusBarAlignment.Right,
      100
    );
    steerButton.command = 'durable-request.steer';
    checkPendingSteering();
    steerButton.show();
    context.subscriptions.push(steerButton);
  }

  // Register steer command
  const steerCommand = vscode.commands.registerCommand(
    'durable-request.steer',
    async () => {
      const message = await vscode.window.showInputBox({
        prompt: 'Enter steering message for the agent',
        placeHolder: 'e.g., "focus on the API layer" or "skip tests"',
        ignoreFocusOut: true,
        validateInput: (value) => {
          if (!value || !value.trim()) {
            return 'Please enter a message';
          }
          return null;
        }
      });

      if (!message) {
        return; // User cancelled
      }

      try {
        const trimmed = message.trim();
        writeSteeringMessage(trimmed);

        // Show notification if enabled
        if (config.get<boolean>('notifyOnSteer', true)) {
          vscode.window.showInformationMessage(
            `⚡ Steering queued: "${trimmed}"`
          );
        }

        // Immediately reflect pending state; polling takes over from here
        updateButtonState(true, trimmed);
        adjustPollRate(true);

      } catch (err) {
        vscode.window.showErrorMessage(
          `Failed to queue steering: ${err instanceof Error ? err.message : String(err)}`
        );
      }
    }
  );

  // Register clear command
  const clearCommand = vscode.commands.registerCommand(
    'durable-request.clearSteering',
    () => {
      const cleared = clearSteeringMessage();
      if (cleared) {
        vscode.window.showInformationMessage('Steering cleared');
        updateButtonState(false);
      } else {
        vscode.window.showInformationMessage('No pending steering to clear');
      }
    }
  );

  // Register status command
  const statusCommand = vscode.commands.registerCommand(
    'durable-request.steeringStatus',
    () => {
      const message = readSteeringMessage();
      if (message) {
        vscode.window.showInformationMessage(
          `Pending steering: "${message}"`
        );
      } else {
        vscode.window.showInformationMessage('No pending steering');
      }
    }
  );

  // Watch for configuration changes
  context.subscriptions.push(
    vscode.workspace.onDidChangeConfiguration((e) => {
      if (e.affectsConfiguration('durableRequest.showStatusBarButton')) {
        const show = vscode.workspace
          .getConfiguration('durableRequest')
          .get<boolean>('showStatusBarButton', true);
        if (show && !steerButton) {
          steerButton = vscode.window.createStatusBarItem(
            vscode.StatusBarAlignment.Right,
            100
          );
          steerButton.command = 'durable-request.steer';
          checkPendingSteering();
          steerButton.show();
          context.subscriptions.push(steerButton);
        } else if (!show && steerButton) {
          steerButton.hide();
        }
      }
    })
  );

  // Start idle polling (5 s). Switches to 1 s automatically while a message is pending.
  pollInterval = setInterval(() => checkPendingSteering(), 5000);
  (pollInterval as any).__intervalMs = 5000;

  context.subscriptions.push(
    steerCommand,
    clearCommand,
    statusCommand,
    { dispose: () => { if (pollInterval) { clearInterval(pollInterval); } } }
  );
}

export function deactivate(): void {
  if (pollInterval) {
    clearInterval(pollInterval);
    pollInterval = null;
  }
}
