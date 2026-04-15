#!/usr/bin/env bash
# run-all.sh — Run all durable-request workloads and generate a full analysis report
#
# Usage:
#   ./testing/scripts/run-all.sh [options]
#
# Options:
#   --workloads <dir>   Directory containing workload .md files (default: testing/workloads/)
#   --results <dir>     Directory for saving results (default: testing/results/run-YYYY-MM-DD/)
#   --runs <N>          Number of runs per workload (default: 1)
#   --filter <pattern>  Only run workloads matching pattern (e.g. "06" or "steering")
#   --dry-run           Print plan without running
#   --analyze-only      Skip running; only analyze existing results in <results_dir>
#   --help              Show this help
#
# Examples:
#   ./testing/scripts/run-all.sh
#   ./testing/scripts/run-all.sh --runs 3 --filter "06"
#   ./testing/scripts/run-all.sh --analyze-only --results testing/results/run-2026-04-15

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# ── Defaults ──────────────────────────────────────────────────────────────────

WORKLOADS_DIR="$REPO_ROOT/testing/workloads"
TODAY="$(date +%Y-%m-%d)"
RESULTS_DIR="$REPO_ROOT/testing/results/run-$TODAY"
RUNS_PER_WORKLOAD=1
FILTER=""
DRY_RUN=false
ANALYZE_ONLY=false

# ── Colors ────────────────────────────────────────────────────────────────────

GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'
BOLD='\033[1m'

# ── Arg parsing ───────────────────────────────────────────────────────────────

while [[ $# -gt 0 ]]; do
  case "$1" in
    --workloads)  WORKLOADS_DIR="$2"; shift 2 ;;
    --results)    RESULTS_DIR="$2";   shift 2 ;;
    --runs)       RUNS_PER_WORKLOAD="$2"; shift 2 ;;
    --filter)     FILTER="$2";        shift 2 ;;
    --dry-run)    DRY_RUN=true;       shift   ;;
    --analyze-only) ANALYZE_ONLY=true; shift  ;;
    --help|-h)
      grep '^#' "$0" | sed 's/^# \{0,2\}//'
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

# ── Validate ──────────────────────────────────────────────────────────────────

if [ ! -d "$WORKLOADS_DIR" ]; then
  echo -e "${RED}Error:${NC} Workloads directory not found: $WORKLOADS_DIR" >&2
  exit 1
fi

# ── Collect workloads ─────────────────────────────────────────────────────────

mapfile -t ALL_WORKLOADS < <(ls "$WORKLOADS_DIR"/*.md 2>/dev/null | sort)

if [ "${#ALL_WORKLOADS[@]}" -eq 0 ]; then
  echo -e "${RED}Error:${NC} No workload files found in $WORKLOADS_DIR" >&2
  exit 1
fi

# Apply filter
WORKLOADS=()
for wf in "${ALL_WORKLOADS[@]}"; do
  if [ -z "$FILTER" ] || [[ "$(basename "$wf")" == *"$FILTER"* ]]; then
    WORKLOADS+=("$wf")
  fi
done

if [ "${#WORKLOADS[@]}" -eq 0 ]; then
  echo -e "${YELLOW}No workloads match filter:${NC} $FILTER" >&2
  exit 1
fi

TOTAL_RUNS=$(( ${#WORKLOADS[@]} * RUNS_PER_WORKLOAD ))

# ── Plan ──────────────────────────────────────────────────────────────────────

echo ""
echo -e "${CYAN}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}${BOLD}  durable-request Test Suite${NC}"
echo -e "${CYAN}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "  Workloads:  ${#WORKLOADS[@]} (${TOTAL_RUNS} total runs)"
echo -e "  Runs each:  $RUNS_PER_WORKLOAD"
echo -e "  Results:    $RESULTS_DIR"
[ -n "$FILTER" ] && echo -e "  Filter:     $FILTER"
$DRY_RUN && echo -e "  Mode:       ${YELLOW}DRY RUN${NC}"
$ANALYZE_ONLY && echo -e "  Mode:       ${YELLOW}ANALYZE ONLY${NC}"
echo ""

for wf in "${WORKLOADS[@]}"; do
  echo -e "  • $(basename "$wf" .md)"
done
echo ""

if $DRY_RUN; then
  echo -e "${YELLOW}Dry run complete. No sessions were started.${NC}"
  exit 0
fi

# ── Analyze-only mode ─────────────────────────────────────────────────────────

if $ANALYZE_ONLY; then
  if [ ! -d "$RESULTS_DIR" ]; then
    echo -e "${RED}Error:${NC} Results directory not found: $RESULTS_DIR" >&2
    exit 1
  fi
  echo -e "${BLUE}Analyzing existing results in:${NC} $RESULTS_DIR"
  python3 "$SCRIPT_DIR/analyze.py" "$RESULTS_DIR"
  exit 0
fi

# ── Check prerequisites ───────────────────────────────────────────────────────

if ! command -v cursor-agent &>/dev/null; then
  echo -e "${RED}Error:${NC} cursor-agent not found in PATH." >&2
  echo "  Start a Cursor CLI session inside tmux:" >&2
  echo "    tmux new-session -A -s cursor -- cursor-agent" >&2
  exit 1
fi

mkdir -p "$RESULTS_DIR"

# ── Run workloads ─────────────────────────────────────────────────────────────

PASS_COUNT=0
FAIL_COUNT=0
SKIPPED=0
FAILED_WORKLOADS=()

START_TIME="$(date +%s)"

for wf in "${WORKLOADS[@]}"; do
  WL_NAME="$(basename "$wf" .md)"
  echo -e "${BLUE}${BOLD}[$(date +%H:%M:%S)]${NC} Running: ${WL_NAME}"

  for run in $(seq 1 "$RUNS_PER_WORKLOAD"); do
    echo -e "  Run $run/$RUNS_PER_WORKLOAD..."

    if bash "$SCRIPT_DIR/run-workload.sh" "$wf" "$RESULTS_DIR" "$run" 2>&1 | \
       sed 's/^/    /'; then
      PASS_COUNT=$(( PASS_COUNT + 1 ))
    else
      FAIL_COUNT=$(( FAIL_COUNT + 1 ))
      FAILED_WORKLOADS+=("${WL_NAME}-$(printf '%03d' "$run")")
    fi

    # Brief pause between runs to avoid rate limits
    [ "$run" -lt "$RUNS_PER_WORKLOAD" ] && sleep 5
  done

  echo ""
done

# ── Analyze results ───────────────────────────────────────────────────────────

END_TIME="$(date +%s)"
ELAPSED=$(( END_TIME - START_TIME ))
ELAPSED_FMT="$(printf '%02d:%02d' $(( ELAPSED / 60 )) $(( ELAPSED % 60 )))"

echo ""
echo -e "${CYAN}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}${BOLD}  Results Summary${NC}"
echo -e "${CYAN}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "  Total runs:  $TOTAL_RUNS  (elapsed: $ELAPSED_FMT)"
echo -e "  Runner pass: ${GREEN}$PASS_COUNT${NC}  fail: ${RED}$FAIL_COUNT${NC}"
echo ""

if [ "${#FAILED_WORKLOADS[@]}" -gt 0 ]; then
  echo -e "  ${RED}Failed runs:${NC}"
  for f in "${FAILED_WORKLOADS[@]}"; do
    echo -e "    • $f"
  done
  echo ""
fi

echo -e "${BLUE}Running pattern analysis...${NC}"
echo ""
python3 "$SCRIPT_DIR/analyze.py" "$RESULTS_DIR"

# Save a summary markdown
SUMMARY_FILE="$RESULTS_DIR/summary.md"
{
  echo "# durable-request Test Run — $TODAY"
  echo ""
  echo "| Field | Value |"
  echo "|-------|-------|"
  echo "| Date | $(date -Iseconds) |"
  echo "| Total runs | $TOTAL_RUNS |"
  echo "| Runner pass | $PASS_COUNT |"
  echo "| Runner fail | $FAIL_COUNT |"
  echo "| Elapsed | $ELAPSED_FMT |"
  echo ""
  echo "## Workloads Run"
  echo ""
  for wf in "${WORKLOADS[@]}"; do
    echo "- $(basename "$wf" .md)"
  done
  echo ""
  echo "## Analysis"
  echo ""
  echo '```'
  python3 "$SCRIPT_DIR/analyze.py" "$RESULTS_DIR" 2>/dev/null || echo "(see analysis.json)"
  echo '```'
} > "$SUMMARY_FILE"

echo ""
echo -e "${GREEN}Summary saved:${NC} $SUMMARY_FILE"
echo -e "${GREEN}Analysis JSON:${NC} $RESULTS_DIR/analysis.json"
echo ""
