#!/usr/bin/env bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# durable-request steering UI — runs inside a tmux popup or split pane
#
# Provides a simple input prompt for sending steering messages to the agent.
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

set -euo pipefail

DATA_DIR="${DURABLE_REQUEST_DATA_DIR:-$HOME/.durable-request/data}"
STEERING_FILE="$DATA_DIR/steering-message"
STEER_CLI="${HOME}/.durable-request/bin/steer"

# Reset terminal to a known state
tput sgr0 2>/dev/null || true
tput rmacs 2>/dev/null || true
printf '\033[0m\033(B' 2>/dev/null || true

# Colors
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

clear 2>/dev/null || true

echo ""
echo -e "  ${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "  ${BOLD}⚡ Steering Message${NC}"
echo -e "  ${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Show current status
if [ -f "$STEERING_FILE" ]; then
  PENDING=$(cat "$STEERING_FILE")
  echo -e "  ${YELLOW}Pending:${NC} ${PENDING}"
  echo ""
fi

echo -e "  ${GREEN}Enter steering message (or press Enter to cancel):${NC}"
echo ""
printf "  > "

read -r MESSAGE

if [ -z "$MESSAGE" ]; then
  echo ""
  echo -e "  ${YELLOW}Cancelled.${NC}"
  sleep 0.3
  exit 0
fi

# Write the steering message
mkdir -p "$DATA_DIR"
echo "$MESSAGE" > "$STEERING_FILE"

echo ""
echo -e "  ${GREEN}✓ Steering queued:${NC} ${BLUE}\"$MESSAGE\"${NC}"
echo -e "  ${GREEN}  Will be processed at next tool call.${NC}"
sleep 0.5
