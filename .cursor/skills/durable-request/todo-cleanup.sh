#!/usr/bin/env bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# durable-request todo-cleanup — mechanical todo list cleanup
#
# Author: Heng Shi <heng.shi@enflame-tech.com>
#
# Takes a JSON array of todos via stdin, applies cleanup rules, outputs
# the cleaned list. The agent should pass the result to TodoWrite.
#
# Usage:
#   echo '[{"id":"x","content":"...","status":"completed"},...]' | todo-cleanup.sh
#
# Rules:
#   1. If count <= 20, output unchanged
#   2. Never delete pending or in_progress items
#   3. Never delete durable-checkpoint
#   4. Delete oldest completed items until count <= 5 (or no more completed)
#
# Output: JSON array of cleaned todos (for TodoWrite with merge: false)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

set -euo pipefail

MAX_ITEMS=20
TARGET_ITEMS=5
PROTECTED_ID="durable-checkpoint"

# Read JSON from stdin
INPUT=$(cat)

# Use jq for JSON processing
if ! command -v jq &>/dev/null; then
  echo "[durable-request] ERROR: jq is required but not installed" >&2
  echo "$INPUT"  # Pass through unchanged
  exit 1
fi

# Validate input is a JSON array
if ! echo "$INPUT" | jq -e 'type == "array"' >/dev/null 2>&1; then
  echo "[durable-request] ERROR: Input must be a JSON array" >&2
  echo "$INPUT"
  exit 1
fi

TOTAL=$(echo "$INPUT" | jq 'length')

# No cleanup needed if <= MAX_ITEMS
if [ "$TOTAL" -le "$MAX_ITEMS" ]; then
  echo "[durable-request] No cleanup needed ($TOTAL items <= $MAX_ITEMS)" >&2
  echo "$INPUT"
  exit 0
fi

echo "[durable-request] Cleanup triggered: $TOTAL items > $MAX_ITEMS" >&2

# Cleanup logic in jq
CLEANED=$(echo "$INPUT" | jq --arg protected "$PROTECTED_ID" --argjson target "$TARGET_ITEMS" '
  # Partition into active (pending/in_progress) and completed
  def is_active: .status == "pending" or .status == "in_progress";
  
  # Get active and completed separately
  (map(select(is_active))) as $active |
  (map(select(is_active | not))) as $completed |
  
  # Calculate how many completed items to keep
  ([$target - ($active | length), 0] | max) as $keep_completed |
  
  # Keep newest completed items (last N in the array)
  # Handle keep_completed == 0 case explicitly
  (if $keep_completed == 0 then [] else ($completed | .[-$keep_completed:]) end) as $kept_completed |
  
  # Combine: all active + kept completed
  ($active + $kept_completed) as $result |
  
  # Ensure protected item is never removed
  if ($result | map(.id) | index($protected)) then
    $result
  else
    # Find protected item in original and add it
    (map(select(.id == $protected)) | .[0]) as $protected_item |
    if $protected_item then
      $result + [$protected_item]
    else
      $result
    end
  end
')

CLEANED_COUNT=$(echo "$CLEANED" | jq 'length')
REMOVED=$((TOTAL - CLEANED_COUNT))

echo "[durable-request] Cleaned: $TOTAL -> $CLEANED_COUNT items (removed $REMOVED completed)" >&2
echo "$CLEANED"
