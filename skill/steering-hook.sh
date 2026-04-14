#!/bin/bash
# steering-hook.sh - PreToolUse hook for steering message injection
#
# STRATEGY: Modify Shell command to prepend steering message as output
# This ensures the steering message appears in the tool's stdout,
# which IS visible to the model as part of the tool result.
#
# KNOWN CURSOR BUGS (March 2026):
# - additionalContext: NOT surfaced to model
# - agent_message: NOT surfaced to model
# - postToolUse additional_context: NOT surfaced to model
#
# WORKAROUND:
# For Shell tools: prepend `echo "[STEERING] ..." &&` to the command
#   - Message is consumed (file deleted)
#   - Steering appears in tool output, model WILL see it
#
# For non-Shell tools: KEEP the message pending
#   - File is NOT deleted
#   - Steering will be delivered on the next Shell tool call
#   - This avoids blocking non-Shell tools with unreliable deny/agent_message

set -euo pipefail

# Configuration
STEERING_DIR="${DURABLE_REQUEST_DATA_DIR:-$HOME/.durable-request/data}"
STEERING_FILE="$STEERING_DIR/steering-message"
LOG_FILE="${DURABLE_REQUEST_LOG_FILE:-$HOME/.durable-request/data/steering-hook.log}"

# Log function
log() {
  echo "[$(date -Is)] [preToolUse] $*" >> "$LOG_FILE" 2>/dev/null || true
}

# Read stdin - MUST read to not hang
INPUT_JSON=""
if [ ! -t 0 ]; then
  INPUT_JSON=$(cat)
fi

# Exit early if no steering file
if [ ! -f "$STEERING_FILE" ]; then
  exit 0
fi

# Read the message
MSG=$(cat "$STEERING_FILE" 2>/dev/null || echo "")

# Exit if empty
if [ -z "$MSG" ]; then
  rm -f "$STEERING_FILE"
  exit 0
fi

# Get tool name and input
TOOL_NAME=""
ORIGINAL_COMMAND=""
if [ -n "$INPUT_JSON" ] && command -v jq &> /dev/null; then
  TOOL_NAME=$(echo "$INPUT_JSON" | jq -r '.tool_name // empty' 2>/dev/null || echo "")
  ORIGINAL_COMMAND=$(echo "$INPUT_JSON" | jq -r '.tool_input.command // empty' 2>/dev/null || echo "")
fi

log "Tool: $TOOL_NAME, Pending steering: $MSG"

# Strategy based on tool type
if [ "$TOOL_NAME" = "Shell" ] && [ -n "$ORIGINAL_COMMAND" ]; then
  # For Shell: consume message and prepend echo to command
  # This makes the steering appear in stdout which model WILL see
  rm -f "$STEERING_FILE"
  log "Steering consumed for Shell tool"
  
  # Escape single quotes in message for shell
  ESCAPED_MSG=$(printf '%s' "$MSG" | sed "s/'/'\\\\''/g")
  
  # Build new command with steering prefix
  NEW_COMMAND="echo '╔══════════════════════════════════════════════════════════════╗
║ ⚡ USER STEERING MESSAGE                                       ║
╠══════════════════════════════════════════════════════════════╣
║ $ESCAPED_MSG
╚══════════════════════════════════════════════════════════════╝
Please acknowledge and incorporate this instruction.' && $ORIGINAL_COMMAND"
  
  log "Modified command to include steering"
  
  # Output with updated_input
  if command -v jq &> /dev/null; then
    jq -n --arg cmd "$NEW_COMMAND" '{
      "permission": "allow",
      "updated_input": {
        "command": $cmd
      }
    }'
  else
    ESCAPED_CMD=$(printf '%s' "$NEW_COMMAND" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))' 2>/dev/null || echo '""')
    echo "{\"permission\": \"allow\", \"updated_input\": {\"command\": $ESCAPED_CMD}}"
  fi
else
  # For non-Shell tools: DO NOT consume the message
  # Keep it pending until the next Shell tool call
  # This way the steering will eventually be delivered when a Shell tool is used
  log "Non-Shell tool ($TOOL_NAME), keeping steering pending"
  
  # Just allow the tool to proceed, don't deny
  # The steering will be processed on the next Shell call
  exit 0
fi

exit 0
