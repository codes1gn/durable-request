#!/usr/bin/env bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# durable-request reinforce — periodic protocol refresh guardrail
#
# Called internally by checkpoint.sh after the user responds. Tracks how
# many checkpoints have occurred and periodically instructs the agent to
# re-read SKILL.md to prevent attention decay in long sessions.
#
# Usage (called by checkpoint.sh, not by agents directly):
#   bash reinforce.sh --skill-path "/path/to/SKILL.md"
#
# State file: $SKILL_DIR/.reinforce-counter
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

set -euo pipefail

SKILL_PATH=""
REFRESH_INTERVAL="${DURABLE_REFRESH_INTERVAL:-5}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --skill-path)       SKILL_PATH="$2"; shift 2 ;;
    --refresh-interval) REFRESH_INTERVAL="$2"; shift 2 ;;
    *) shift ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
COUNTER_FILE="$SCRIPT_DIR/.reinforce-counter"

# Read and increment counter
COUNTER=0
if [ -f "$COUNTER_FILE" ]; then
  COUNTER=$(cat "$COUNTER_FILE" 2>/dev/null || echo "0")
  COUNTER=$((COUNTER + 1))
else
  COUNTER=1
fi
echo "$COUNTER" > "$COUNTER_FILE"

# G2: Structural continuation anchor reminder (every checkpoint)
echo ""
echo "[ANCHOR] Ensure todo 'durable-checkpoint' stays in_progress until user says done."

# G3: Protocol refresh (every N checkpoints)
if [ -n "$SKILL_PATH" ] && (( COUNTER % REFRESH_INTERVAL == 0 )) && (( COUNTER > 0 )); then
  echo ""
  echo "[PROTOCOL REFRESH] Checkpoint #$COUNTER reached (refresh every $REFRESH_INTERVAL)."
  echo "[PROTOCOL REFRESH] Re-read the durable-request protocol before continuing:"
  echo "[PROTOCOL REFRESH]   Read file: $SKILL_PATH"
  echo "[PROTOCOL REFRESH]   Focus sections: Checkpoint Mechanism, Anti-Silent-Completion Rules"
fi
