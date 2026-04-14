#!/bin/bash
# steering-hook.sh - PreToolUse hook for steering message injection
#
# This hook is called before each tool execution in Cursor IDE.
# It checks for a pending steering message and injects it as additionalContext.
#
# Installation:
#   Add to ~/.cursor/hooks.json:
#   {
#     "version": 1,
#     "hooks": {
#       "preToolUse": [
#         {
#           "command": "~/.durable-request/hooks/steering-hook.sh",
#           "timeout_ms": 2000
#         }
#       ]
#     }
#   }

set -euo pipefail

# Configuration
STEERING_DIR="${DURABLE_REQUEST_DATA_DIR:-$HOME/.durable-request/data}"
STEERING_FILE="$STEERING_DIR/steering-message"

# Exit early if no steering file
[ -f "$STEERING_FILE" ] || exit 0

# Read the message
MSG=$(cat "$STEERING_FILE" 2>/dev/null || echo "")

# Exit if empty
if [ -z "$MSG" ]; then
  rm -f "$STEERING_FILE"
  exit 0
fi

# Consume the message (delete file)
rm -f "$STEERING_FILE"

# Determine the tool being called (from stdin JSON, if available)
TOOL_NAME=""
if [ -t 0 ]; then
  # No stdin, skip tool detection
  :
else
  # Try to parse tool name from hook input
  INPUT=$(cat)
  if command -v jq &> /dev/null; then
    TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null || echo "")
  fi
fi

# Format the context injection
CONTEXT="⚡ [USER STEERING]: $MSG"

# Add tool context if available
if [ -n "$TOOL_NAME" ]; then
  CONTEXT="$CONTEXT (received before $TOOL_NAME)"
fi

# Output hook response
# The additionalContext will be appended to the model's context
if command -v jq &> /dev/null; then
  jq -n --arg context "$CONTEXT" '{
    "hookSpecificOutput": {
      "hookEventName": "preToolUse",
      "additionalContext": $context
    }
  }'
else
  # Fallback without jq (less safe for special characters)
  cat << EOF
{
  "hookSpecificOutput": {
    "hookEventName": "preToolUse",
    "additionalContext": "$CONTEXT"
  }
}
EOF
fi

exit 0
