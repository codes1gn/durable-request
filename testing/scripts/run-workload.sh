#!/usr/bin/env bash
# run-workload.sh — Run a single durable-request workload and save the transcript
#
# Usage:
#   ./testing/scripts/run-workload.sh <workload_file> [results_dir] [run_index]
#
# Examples:
#   ./testing/scripts/run-workload.sh testing/workloads/01-simple-task.md
#   ./testing/scripts/run-workload.sh testing/workloads/06-steering.md testing/results/run-2026-04-15 3
#
# Output:
#   <results_dir>/<workload-id>-<NNN>.txt   — plain-text transcript of the session
#
# Requires: cursor-agent (Cursor CLI) available in PATH

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# ── Args ──────────────────────────────────────────────────────────────────────

WORKLOAD_FILE="${1:-}"
if [ -z "$WORKLOAD_FILE" ]; then
  echo "Usage: $0 <workload_file> [results_dir] [run_index]" >&2
  exit 1
fi

if [ ! -f "$WORKLOAD_FILE" ]; then
  echo "Error: workload file not found: $WORKLOAD_FILE" >&2
  exit 1
fi

TODAY="$(date +%Y-%m-%d)"
RESULTS_DIR="${2:-$REPO_ROOT/testing/results/run-$TODAY}"
RUN_INDEX="${3:-001}"

# Pad index to 3 digits
RUN_INDEX="$(printf '%03d' "$RUN_INDEX")"

# Derive workload ID from filename (e.g. "01-simple-task" from "01-simple-task.md")
WORKLOAD_BASENAME="$(basename "$WORKLOAD_FILE" .md)"

TRANSCRIPT_FILE="$RESULTS_DIR/${WORKLOAD_BASENAME}-${RUN_INDEX}.txt"

# ── Colors ────────────────────────────────────────────────────────────────────

GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'
BOLD='\033[1m'

# ── Extract prompt from workload file ─────────────────────────────────────────

extract_prompt() {
  local file="$1"
  # Extract content between the first ```...``` block under "## Prompt"
  awk '
    /^## Prompt/ { in_section=1; next }
    in_section && /^```/ {
      if (!in_block) { in_block=1; next }
      else { exit }
    }
    in_block { print }
  ' "$file"
}

PROMPT="$(extract_prompt "$WORKLOAD_FILE")"

if [ -z "$PROMPT" ]; then
  echo -e "${RED}Error:${NC} Could not extract prompt from $WORKLOAD_FILE" >&2
  echo "  Make sure the workload has a '## Prompt' section with a fenced code block." >&2
  exit 1
fi

# ── Special setup for steering workloads ──────────────────────────────────────

is_steering_workload() {
  grep -q "Special Setup\|steer\b" "$1" 2>/dev/null
}

STEERING_MSG=""
if is_steering_workload "$WORKLOAD_FILE"; then
  # Extract steering message from the workload file if present
  STEERING_MSG="$(awk '/steer "/{match($0,/steer "([^"]+)"/,a); if(a[1]) print a[1]}' "$WORKLOAD_FILE" | head -1)"
fi

# ── Ensure results dir ────────────────────────────────────────────────────────

mkdir -p "$RESULTS_DIR"

# ── Run the workload ──────────────────────────────────────────────────────────

echo ""
echo -e "${BLUE}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}${BOLD} Workload: ${WORKLOAD_BASENAME}${NC}"
echo -e "${BLUE}${BOLD} Run:      #${RUN_INDEX}${NC}"
echo -e "${BLUE}${BOLD} Output:   ${TRANSCRIPT_FILE}${NC}"
echo -e "${BLUE}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Check cursor-agent is available
if ! command -v cursor-agent &>/dev/null; then
  echo -e "${RED}Error:${NC} cursor-agent not found in PATH." >&2
  echo "  Start Cursor CLI session: tmux new-session -A -s cursor -- cursor-agent" >&2
  exit 1
fi

# Write the prompt to a temp file for piping
PROMPT_FILE="$(mktemp)"
trap 'rm -f "$PROMPT_FILE"' EXIT
printf '%s\n' "$PROMPT" > "$PROMPT_FILE"

echo -e "${GREEN}Prompt:${NC}"
echo "$PROMPT" | head -5
[ "$(echo "$PROMPT" | wc -l)" -gt 5 ] && echo "  ..."
echo ""

# For steering workloads: schedule the steer command to fire after a delay
STEER_PID=""
if [ -n "$STEERING_MSG" ]; then
  echo -e "${YELLOW}Steering:${NC} Will inject \"$STEERING_MSG\" after 8 seconds"
  (sleep 8 && steer "$STEERING_MSG" && echo -e "${GREEN}[runner]${NC} Steering injected: \"$STEERING_MSG\"") &
  STEER_PID=$!
fi

# Run cursor-agent non-interactively, capture full output as transcript
echo -e "${GREEN}[runner]${NC} Starting cursor-agent session..."

{
  echo "=== durable-request test session ==="
  echo "Workload: $WORKLOAD_BASENAME"
  echo "Run: $RUN_INDEX"
  echo "Date: $(date -Iseconds)"
  echo "Prompt:"
  echo "$PROMPT"
  echo ""
  echo "=== Session transcript ==="
  echo ""
} > "$TRANSCRIPT_FILE"

# Run cursor-agent, piping prompt in, appending output to transcript
# --no-interactive feeds the prompt and lets the agent respond fully
# The session ends when the agent reaches a "Done" checkpoint option
if cursor-agent --no-interactive < "$PROMPT_FILE" >> "$TRANSCRIPT_FILE" 2>&1; then
  echo -e "${GREEN}[runner]${NC} Session completed successfully"
else
  RC=$?
  echo -e "${YELLOW}[runner]${NC} cursor-agent exited with code $RC (may be normal)"
fi

# Clean up steering timer if still running
if [ -n "$STEER_PID" ] && kill -0 "$STEER_PID" 2>/dev/null; then
  kill "$STEER_PID" 2>/dev/null || true
fi

echo ""
echo -e "${GREEN}[runner]${NC} Transcript saved: ${TRANSCRIPT_FILE}"
LINES="$(wc -l < "$TRANSCRIPT_FILE")"
echo -e "${GREEN}[runner]${NC} Lines: $LINES"
echo ""

# Quick pattern check
echo -e "${BLUE}Quick pattern check:${NC}"
SCRIPT_DIR_PY="$(cd "$SCRIPT_DIR" && pwd)"
python3 - <<PYEOF
import sys
sys.path.insert(0, '$SCRIPT_DIR_PY')
from patterns import WORKLOAD_FEATURES, check_feature

with open('$TRANSCRIPT_FILE') as f:
    transcript = f.read()

workload_id = '$WORKLOAD_BASENAME'
features = WORKLOAD_FEATURES.get(workload_id, [])
if not features:
    print("  (no features defined for this workload)")
else:
    passed = 0
    for fid in features:
        r = check_feature(transcript, fid)
        sym = '✓' if r['found'] else '✗'
        print(f"  {sym} {fid}: {r.get('feature', fid)}")
        if r['found']:
            passed += 1
    print(f"\n  Result: {passed}/{len(features)} features detected")
PYEOF
