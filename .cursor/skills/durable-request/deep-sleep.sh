#!/usr/bin/env bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# deep-sleep — keeps agent alive while waiting for user to return
#
# Author: Heng Shi <heng.shi@enflame-tech.com>
#
# When the agent reaches a checkpoint but the user is away, this script
# blocks the Shell tool with periodic keep-alive messages to prevent the
# request from timing out. It polls a wake file; when the user returns and
# triggers a wake signal, the script exits and the agent resumes.
#
# Usage (called by agent via Shell tool):
#   bash ~/.cursor/skills/durable-request/deep-sleep.sh [timeout_minutes]
#
# Wake mechanism:
#   The user (or another script) touches the wake file to signal return:
#     touch ~/.cursor/skills/durable-request/.deep-sleep-wake
#
# Defaults:
#   - Keep-alive interval: 60 seconds
#   - Max sleep: 1440 minutes (24 hours)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
WAKE_FILE="$SKILL_DIR/.deep-sleep-wake"
SLEEP_LOG="$SKILL_DIR/.deep-sleep-log"

TIMEOUT_MINUTES="${1:-1440}"
POLL_SECONDS=5
KEEPALIVE_SECONDS=60
MAX_POLLS=$(( TIMEOUT_MINUTES * 60 / POLL_SECONDS ))
POLLS_PER_KEEPALIVE=$(( KEEPALIVE_SECONDS / POLL_SECONDS ))

cleanup() {
  rm -f "$SLEEP_LOG"
}
trap cleanup EXIT

rm -f "$WAKE_FILE"

echo "[deep-sleep] Agent entering deep sleep mode."
echo "[deep-sleep] Will keep alive for up to ${TIMEOUT_MINUTES} minutes."
echo "[deep-sleep] To wake: touch $WAKE_FILE"
echo "[deep-sleep] ---"

POLL=0
while [ "$POLL" -lt "$MAX_POLLS" ]; do
  sleep "$POLL_SECONDS"
  POLL=$((POLL + 1))

  if [ -f "$WAKE_FILE" ]; then
    ELAPSED_MIN=$(( POLL * POLL_SECONDS / 60 ))
    rm -f "$WAKE_FILE"
    echo ""
    echo "[deep-sleep] ================================"
    echo "[deep-sleep] Wake signal received after ${ELAPSED_MIN} minute(s)."
    echo "[deep-sleep] Agent resuming — continue your work and present a checkpoint."
    echo "[deep-sleep] ================================"
    exit 0
  fi

  if [ $((POLL % POLLS_PER_KEEPALIVE)) -eq 0 ]; then
    ELAPSED_MIN=$(( POLL * POLL_SECONDS / 60 ))
    echo "[deep-sleep] Still sleeping... ${ELAPSED_MIN}/${TIMEOUT_MINUTES} min elapsed. I am working, keep waiting..."
  fi
done

echo ""
echo "[deep-sleep] ================================"
echo "[deep-sleep] Max sleep time (${TIMEOUT_MINUTES} min) reached."
echo "[deep-sleep] Agent resuming — continue your work and present a checkpoint."
echo "[deep-sleep] ================================"
