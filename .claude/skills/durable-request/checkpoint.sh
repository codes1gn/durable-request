#!/usr/bin/env bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# durable-request checkpoint — interactive CLI checkpoint via tmux split pane
#
# Author: Heng Shi <heng.shi@enflame-tech.com>
#
# Called by the agent via the Shell tool. Creates a tmux split pane where
# the user selects their next action, then returns their choice to the agent.
#
# Usage:
#   checkpoint.sh "What would you like to do next?" \
#                 "Run tests" "Iterate" "Review diff" "Done"
#
# Requirements: tmux (cursor-agent must be running inside a tmux session)
#
# File protocol (self-contained in the skills folder):
#   .ckpt-question   — serialized question (prompt + options)
#   .ckpt-answer     — user's response (written by checkpoint-ui.sh)
#   .ckpt-lock       — present while waiting for user input
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
QUESTION_FILE="$SKILL_DIR/.ckpt-question"
ANSWER_FILE="$SKILL_DIR/.ckpt-answer"
LOCK_FILE="$SKILL_DIR/.ckpt-lock"
UI_SCRIPT="$SKILL_DIR/checkpoint-ui.sh"

PROMPT="${1:-What would you like to do next?}"
shift || true
OPTIONS=("$@")

if [ ${#OPTIONS[@]} -eq 0 ]; then
  OPTIONS=("Continue" "Done")
fi

OPTIONS+=("I'll type my own instruction")
NUM_OPTIONS=${#OPTIONS[@]}

cleanup() {
  rm -f "$LOCK_FILE" "$QUESTION_FILE"
}
trap cleanup EXIT

# ── 1. Serialize question to file ────────────────────────────────────────
rm -f "$ANSWER_FILE" "$QUESTION_FILE" "$LOCK_FILE"

{
  echo "$PROMPT"
  for opt in "${OPTIONS[@]}"; do
    echo "$opt"
  done
} > "$QUESTION_FILE"

touch "$LOCK_FILE"

# ── 2. Detect tmux and launch UI pane ────────────────────────────────────
find_tmux_session() {
  # Strategy 1: Find cursor-agent process with a real TTY, match to tmux pane
  local pids ttys
  pids=$(pgrep -f 'cursor-agent' 2>/dev/null || true)
  for pid in $pids; do
    local tty
    tty=$(ps -o tty= -p "$pid" 2>/dev/null | tr -d ' ' || true)
    [ -z "$tty" ] || [ "$tty" = "?" ] && continue
    local target
    target=$(tmux list-panes -a -F '#{pane_tty} #{session_name}:#{window_index}' 2>/dev/null \
      | grep "/dev/$tty" \
      | head -1 \
      | awk '{print $2}')
    if [ -n "$target" ]; then
      echo "$target"
      return 0
    fi
  done

  # Strategy 2: Check if there's a tmux session named "cursor"
  if tmux has-session -t cursor 2>/dev/null; then
    echo "cursor:0"
    return 0
  fi

  # Strategy 3: Use the first available tmux session
  local first_session
  first_session=$(tmux list-sessions -F '#{session_name}' 2>/dev/null | head -1 || true)
  if [ -n "$first_session" ]; then
    echo "$first_session:0"
    return 0
  fi

  return 1
}

TMUX_TARGET=""

if [ -n "${TMUX:-}" ]; then
  TMUX_TARGET=$(tmux display-message -p '#{session_name}:#{window_index}' 2>/dev/null || true)
elif command -v tmux &>/dev/null; then
  TMUX_TARGET=$(find_tmux_session || true)
fi

if [ -n "$TMUX_TARGET" ]; then
  echo "[durable-request] Opening checkpoint in tmux pane ($TMUX_TARGET)..."
  echo "[durable-request] Waiting for user response..."
  # Launch UI in a split pane (bottom, 14 lines)
  tmux split-window -t "$TMUX_TARGET" -v -l 14 \
    "bash '$UI_SCRIPT' '$SKILL_DIR'" 2>/dev/null || {
    echo "[durable-request] ERROR: Failed to create tmux split pane."
    echo "[durable-request] Falling back to non-interactive mode."
    echo "${OPTIONS[0]}" > "$ANSWER_FILE"
    rm -f "$LOCK_FILE"
    echo "[durable-request] Auto-selected: ${OPTIONS[0]}"
    exit 0
  }
else
  echo "[durable-request] ERROR: tmux session not found."
  echo "[durable-request] For CLI checkpoints, run cursor-agent inside tmux:"
  echo "[durable-request]   tmux new-session -- cursor-agent"
  echo "[durable-request] Or add this alias to ~/.bashrc:"
  echo "[durable-request]   alias cursor-agent='tmux new-session -A -s cursor -- cursor-agent'"
  echo "[durable-request] Falling back to non-interactive mode."
  echo "${OPTIONS[0]}" > "$ANSWER_FILE"
  rm -f "$LOCK_FILE"
  echo "[durable-request] Auto-selected: ${OPTIONS[0]}"
  exit 0
fi

# ── 3. Poll for answer (print keep-alive messages to prevent Shell timeout) ─
TIMEOUT=1200  # 10 minutes max (in quarter-second ticks)
ELAPSED=0
KEEPALIVE_INTERVAL=40  # Print a message every 10 seconds (40 * 0.25s)

while [ ! -f "$ANSWER_FILE" ] && [ "$ELAPSED" -lt "$TIMEOUT" ]; do
  sleep 0.25
  ELAPSED=$((ELAPSED + 1))
  if [ $((ELAPSED % KEEPALIVE_INTERVAL)) -eq 0 ]; then
    echo "[durable-request] Still waiting for user response... ($((ELAPSED / 4))s)"
  fi
done

if [ ! -f "$ANSWER_FILE" ]; then
  echo "[durable-request] Timeout waiting for user response."
  echo "[durable-request] Auto-selected: ${OPTIONS[0]}"
  echo "${OPTIONS[0]}" > "$ANSWER_FILE"
fi

# ── 4. Read and return answer ────────────────────────────────────────────
ANSWER=$(cat "$ANSWER_FILE")
rm -f "$ANSWER_FILE" "$LOCK_FILE" "$QUESTION_FILE"

echo ""
echo "[durable-request] ================================"
echo "[durable-request] User responded: $ANSWER"
echo "[durable-request] ================================"
