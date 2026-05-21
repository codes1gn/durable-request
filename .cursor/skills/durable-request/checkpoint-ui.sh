#!/usr/bin/env bash
# durable-request checkpoint UI — runs inside a tmux split pane
# Author: Heng Shi

set -euo pipefail

SKILL_DIR="${1:?Usage: checkpoint-ui.sh <skill-dir>}"
QUESTION_FILE="$SKILL_DIR/.ckpt-question"
ANSWER_FILE="$SKILL_DIR/.ckpt-answer"
LOCK_FILE="$SKILL_DIR/.ckpt-lock"

if [ ! -f "$QUESTION_FILE" ]; then
  echo "[durable-request] No question file found. Exiting."
  rm -f "$LOCK_FILE"
  exit 1
fi

mapfile -t LINES < "$QUESTION_FILE"
PROMPT="${LINES[0]}"
OPTIONS=("${LINES[@]:1}")
NUM_OPTIONS=${#OPTIONS[@]}

# Reset terminal to a known state (prevents ACS/line-drawing mode issues)
tput sgr0 2>/dev/null || true
tput rmacs 2>/dev/null || true
printf '\033[0m\033(B' 2>/dev/null || true

echo ""
echo "  === [durable-request] Checkpoint ==="
echo ""
echo "  $PROMPT"
echo ""
for i in "${!OPTIONS[@]}"; do
  NUM=$((i + 1))
  echo "    $NUM. ${OPTIONS[$i]}"
done
echo ""
echo "  ======================================"
echo ""
printf "  > Choice (number or text): "

read -r CHOICE

ANSWER=""
if [[ "$CHOICE" =~ ^[0-9]+$ ]] && [ "$CHOICE" -ge 1 ] && [ "$CHOICE" -le "$NUM_OPTIONS" ]; then
  IDX=$((CHOICE - 1))
  SELECTED="${OPTIONS[$IDX]}"
  if [ "$CHOICE" -eq "$NUM_OPTIONS" ]; then
    printf "  > Type your instruction: "
    read -r FREEFORM
    ANSWER="$FREEFORM"
  else
    ANSWER="$SELECTED"
  fi
else
  ANSWER="$CHOICE"
fi

echo "$ANSWER" > "$ANSWER_FILE"

echo ""
echo "  * Sent: $ANSWER"
sleep 0.3

rm -f "$LOCK_FILE"
