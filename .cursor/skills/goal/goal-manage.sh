#!/usr/bin/env bash
set -euo pipefail

# goal-manage.sh — State management for /goal skill
# Usage: goal-manage.sh <command> [args...]
#   create "<condition>" [--test "<cmd>"] [--budget <N>]
#   status
#   pause
#   resume
#   clear
#   done

DATA_DIR="${HOME}/.durable-request/data"
GOAL_FILE="${DATA_DIR}/goal.json"

mkdir -p "$DATA_DIR"

now_iso() {
  date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date +"%Y-%m-%dT%H:%M:%SZ"
}

cmd_create() {
  local condition=""
  local test_cmd=""
  local budget=20

  # First positional arg is the condition
  condition="${1:-}"
  shift 2>/dev/null || true

  # Parse remaining flags
  while [ $# -gt 0 ]; do
    case "$1" in
      --test)
        test_cmd="${2:-}"
        shift 2
        ;;
      --budget)
        budget="${2:-20}"
        shift 2
        ;;
      *)
        shift
        ;;
    esac
  done

  if [ -z "$condition" ]; then
    echo "[goal] Error: condition is required. Usage: goal-manage.sh create \"<condition>\"" >&2
    exit 1
  fi

  # Enforce 4000 char limit (matching Claude Code)
  if [ "${#condition}" -gt 4000 ]; then
    echo "[goal] Error: condition exceeds 4000 character limit (${#condition} chars)" >&2
    exit 1
  fi

  local now
  now=$(now_iso)

  # Write goal state — jq for safe JSON encoding
  jq -n \
    --argjson active true \
    --arg condition "$condition" \
    --arg validation_command "$test_cmd" \
    --arg created_at "$now" \
    --argjson turn_budget "$budget" \
    --argjson turns_used 0 \
    --arg status "pursuing" \
    --arg last_reason "" \
    --arg last_validation_output "" \
    '{
      active: $active,
      condition: $condition,
      validation_command: $validation_command,
      created_at: $created_at,
      turn_budget: $turn_budget,
      turns_used: $turns_used,
      status: $status,
      last_reason: $last_reason,
      last_validation_output: $last_validation_output
    }' > "$GOAL_FILE"

  echo "[goal] Goal created:"
  echo "  Condition: $condition"
  [ -n "$test_cmd" ] && echo "  Validation: $test_cmd"
  echo "  Budget: $budget turns"
  echo "  Status: pursuing"
}

cmd_status() {
  if [ ! -f "$GOAL_FILE" ]; then
    echo "[goal] No active goal."
    exit 0
  fi

  local active condition status turns_used turn_budget validation_command last_reason created_at
  active=$(jq -r '.active' "$GOAL_FILE")
  condition=$(jq -r '.condition' "$GOAL_FILE")
  status=$(jq -r '.status' "$GOAL_FILE")
  turns_used=$(jq -r '.turns_used' "$GOAL_FILE")
  turn_budget=$(jq -r '.turn_budget' "$GOAL_FILE")
  validation_command=$(jq -r '.validation_command // empty' "$GOAL_FILE")
  last_reason=$(jq -r '.last_reason // empty' "$GOAL_FILE")
  created_at=$(jq -r '.created_at' "$GOAL_FILE")

  echo "[goal] Status Report"
  echo "  Active: $active"
  echo "  Status: $status"
  echo "  Condition: $condition"
  echo "  Progress: $turns_used / $turn_budget turns"
  [ -n "$validation_command" ] && echo "  Validation: $validation_command"
  [ -n "$last_reason" ] && echo "  Last evaluation: $last_reason"
  echo "  Created: $created_at"
}

cmd_pause() {
  if [ ! -f "$GOAL_FILE" ]; then
    echo "[goal] No active goal to pause."
    exit 1
  fi

  local current_status
  current_status=$(jq -r '.status' "$GOAL_FILE")
  if [ "$current_status" != "pursuing" ]; then
    echo "[goal] Cannot pause: goal is '$current_status', not 'pursuing'."
    exit 1
  fi

  jq '.status = "paused"' "$GOAL_FILE" > "${GOAL_FILE}.tmp" \
    && mv "${GOAL_FILE}.tmp" "$GOAL_FILE"
  echo "[goal] Goal paused. Auto-continuation disabled. Use 'goal-manage.sh resume' to continue."
}

cmd_resume() {
  if [ ! -f "$GOAL_FILE" ]; then
    echo "[goal] No goal to resume."
    exit 1
  fi

  local current_status
  current_status=$(jq -r '.status' "$GOAL_FILE")
  if [ "$current_status" != "paused" ]; then
    echo "[goal] Cannot resume: goal is '$current_status', not 'paused'."
    exit 1
  fi

  jq '.status = "pursuing" | .active = true' "$GOAL_FILE" > "${GOAL_FILE}.tmp" \
    && mv "${GOAL_FILE}.tmp" "$GOAL_FILE"

  local condition
  condition=$(jq -r '.condition' "$GOAL_FILE")
  echo "[goal] Goal resumed. Continuing toward: $condition"
}

cmd_done() {
  if [ ! -f "$GOAL_FILE" ]; then
    echo "[goal] No active goal to mark done."
    exit 1
  fi

  jq '.status = "achieved" | .active = false' "$GOAL_FILE" > "${GOAL_FILE}.tmp" \
    && mv "${GOAL_FILE}.tmp" "$GOAL_FILE"

  local condition turns_used
  condition=$(jq -r '.condition' "$GOAL_FILE")
  turns_used=$(jq -r '.turns_used' "$GOAL_FILE")
  echo "[goal] ✓ Goal achieved in $turns_used turns: $condition"
}

cmd_clear() {
  if [ -f "$GOAL_FILE" ]; then
    rm -f "$GOAL_FILE"
    echo "[goal] Goal cleared."
  else
    echo "[goal] No active goal."
  fi
}

# Dispatch
case "${1:-help}" in
  create) shift; cmd_create "$@" ;;
  status) cmd_status ;;
  pause)  cmd_pause ;;
  resume) cmd_resume ;;
  done)   cmd_done ;;
  clear)  cmd_clear ;;
  help|*)
    echo "Usage: goal-manage.sh <command> [args...]"
    echo "  create \"<condition>\" [--test \"<cmd>\"] [--budget <N>]"
    echo "  status     Show current goal state"
    echo "  pause      Pause auto-continuation"
    echo "  resume     Resume a paused goal"
    echo "  done       Mark goal as achieved"
    echo "  clear      Remove goal entirely"
    ;;
esac
