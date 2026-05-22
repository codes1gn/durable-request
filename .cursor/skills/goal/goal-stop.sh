#!/usr/bin/env bash
set -euo pipefail

# goal-stop.sh — Cursor stop hook for /goal skill
#
# This is the SAFETY NET layer. Primary evaluation happens via subagent
# within the agent's turn. This hook fires between turns to catch cases
# where the agent forgot to evaluate or ended its turn prematurely.
#
# Input (stdin): JSON from Cursor with status, loop_count, transcript_path
# Output (stdout): JSON with optional followup_message
#
# hooks.json config:
#   { "stop": [{ "command": "~/.cursor/skills/goal/goal-stop.sh", "loop_limit": null, "timeout": 30 }] }

GOAL_FILE="${HOME}/.durable-request/data/goal.json"

# Read Cursor's stop hook input
INPUT=$(cat)

STATUS=$(echo "$INPUT" | jq -r '.status // "unknown"')
LOOP_COUNT=$(echo "$INPUT" | jq -r '.loop_count // 0')

# Only process completed turns
if [ "$STATUS" != "completed" ]; then
  exit 0
fi

# No goal file → no active goal → allow normal stop
if [ ! -f "$GOAL_FILE" ]; then
  exit 0
fi

# Parse goal state — fail-open on any error
ACTIVE=$(jq -r '.active // false' "$GOAL_FILE" 2>/dev/null) || { exit 0; }
GOAL_STATUS=$(jq -r '.status // "unknown"' "$GOAL_FILE" 2>/dev/null) || { exit 0; }

# Goal not active or not pursuing → allow normal stop
if [ "$ACTIVE" != "true" ] || [ "$GOAL_STATUS" != "pursuing" ]; then
  exit 0
fi

# Read goal details
CONDITION=$(jq -r '.condition // "unknown"' "$GOAL_FILE" 2>/dev/null) || CONDITION="unknown"
TURN_BUDGET=$(jq -r '.turn_budget // 20' "$GOAL_FILE" 2>/dev/null) || TURN_BUDGET=20
TURNS_USED=$(jq -r '.turns_used // 0' "$GOAL_FILE" 2>/dev/null) || TURNS_USED=0
VALIDATION_CMD=$(jq -r '.validation_command // empty' "$GOAL_FILE" 2>/dev/null) || VALIDATION_CMD=""

# Increment turn counter
TURNS_USED=$((TURNS_USED + 1))
jq ".turns_used = $TURNS_USED" "$GOAL_FILE" > "${GOAL_FILE}.tmp" \
  && mv "${GOAL_FILE}.tmp" "$GOAL_FILE" 2>/dev/null || true

# Budget check
if [ "$TURNS_USED" -ge "$TURN_BUDGET" ] 2>/dev/null; then
  jq '.status = "budget-limited" | .active = false' "$GOAL_FILE" \
    > "${GOAL_FILE}.tmp" && mv "${GOAL_FILE}.tmp" "$GOAL_FILE" 2>/dev/null || true

  # Escape condition for JSON
  ESCAPED_CONDITION=$(echo "$CONDITION" | jq -Rs '.')
  echo "{\"followup_message\": \"[GOAL BUDGET] Turn limit ($TURN_BUDGET) reached. Wrap up current work and summarize progress toward: ${CONDITION}\"}"
  exit 0
fi

# Optional: run validation command for quick check
if [ -n "$VALIDATION_CMD" ]; then
  VALIDATION_OUTPUT=$(eval "$VALIDATION_CMD" 2>&1) && VALIDATION_EXIT=0 || VALIDATION_EXIT=$?
  LAST_LINES=$(echo "$VALIDATION_OUTPUT" | tail -10)

  # Store validation output
  jq --arg out "$LAST_LINES" '.last_validation_output = $out' "$GOAL_FILE" \
    > "${GOAL_FILE}.tmp" && mv "${GOAL_FILE}.tmp" "$GOAL_FILE" 2>/dev/null || true

  if [ "$VALIDATION_EXIT" -eq 0 ]; then
    # Validation passed — but let the agent confirm via subagent in next turn
    # Don't auto-mark achieved here; the agent should verify
    REMAINING=$((TURN_BUDGET - TURNS_USED))
    echo "{\"followup_message\": \"[GOAL] Turn $TURNS_USED/$TURN_BUDGET. Validation command PASSED (exit 0). Verify the goal is fully achieved and mark done if so. Goal: ${CONDITION}\"}"
    exit 0
  else
    REMAINING=$((TURN_BUDGET - TURNS_USED))
    jq --arg reason "Validation failed (exit $VALIDATION_EXIT)" '.last_reason = $reason' "$GOAL_FILE" \
      > "${GOAL_FILE}.tmp" && mv "${GOAL_FILE}.tmp" "$GOAL_FILE" 2>/dev/null || true
    echo "{\"followup_message\": \"[GOAL] Turn $TURNS_USED/$TURN_BUDGET ($REMAINING remaining). Validation FAILED (exit $VALIDATION_EXIT): $(echo "$LAST_LINES" | head -3 | tr '\n' ' '). Continue working toward: ${CONDITION}\"}"
    exit 0
  fi
fi

# No validation command — generic continuation
REMAINING=$((TURN_BUDGET - TURNS_USED))
echo "{\"followup_message\": \"[GOAL] Turn $TURNS_USED/$TURN_BUDGET ($REMAINING remaining). Continue working toward: ${CONDITION}. Evaluate completion via subagent when ready.\"}"
