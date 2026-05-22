#!/bin/bash
# install-goal.sh - Install /goal autonomous loop skill for Cursor IDE
#
# Usage:
#   ./install-goal.sh
#
# This script installs:
#   1. goal-manage.sh (state management)
#   2. goal-stop.sh (stop hook for auto-continuation)
#   3. SKILL.md (agent behavior definition)
#   4. Cursor hooks.json stop hook configuration

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

INSTALL_DIR="${HOME}/.cursor/skills/goal"
DATA_DIR="${HOME}/.durable-request/data"
CURSOR_HOOKS_FILE="${HOME}/.cursor/hooks.json"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

log_info()  { echo -e "${GREEN}[install-goal]${NC} $1"; }
log_warn()  { echo -e "${YELLOW}[install-goal]${NC} $1"; }
log_error() { echo -e "${RED}[install-goal]${NC} $1" >&2; }
log_step()  { echo -e "${BLUE}==>${NC} $1"; }

check_dependencies() {
  log_step "Checking dependencies..."
  local missing=()
  command -v jq &>/dev/null || missing+=("jq")
  if [ ${#missing[@]} -gt 0 ]; then
    log_error "Missing required dependencies: ${missing[*]}"
    log_error "Install with: sudo apt install ${missing[*]}"
    exit 1
  fi
  log_info "All dependencies found"
}

install_skill_files() {
  log_step "Installing skill files..."
  mkdir -p "$INSTALL_DIR" "$DATA_DIR"

  local SOURCE_DIR="${SCRIPT_DIR}/.cursor/skills/goal"
  if [ ! -d "$SOURCE_DIR" ]; then
    log_error "Source directory not found: $SOURCE_DIR"
    log_error "Run this script from the durable-request repo root."
    exit 1
  fi

  cp "$SOURCE_DIR/goal-manage.sh" "$INSTALL_DIR/goal-manage.sh"
  cp "$SOURCE_DIR/goal-stop.sh"   "$INSTALL_DIR/goal-stop.sh"
  cp "$SOURCE_DIR/SKILL.md"       "$INSTALL_DIR/SKILL.md"

  chmod +x "$INSTALL_DIR/goal-manage.sh"
  chmod +x "$INSTALL_DIR/goal-stop.sh"

  log_info "Installed: $INSTALL_DIR/goal-manage.sh"
  log_info "Installed: $INSTALL_DIR/goal-stop.sh"
  log_info "Installed: $INSTALL_DIR/SKILL.md"
}

configure_stop_hook() {
  log_step "Configuring Cursor stop hook..."

  local CURSOR_DIR="${HOME}/.cursor"
  mkdir -p "$CURSOR_DIR"

  local HOOK_ENTRY='{
    "command": "~/.cursor/skills/goal/goal-stop.sh",
    "loop_limit": null,
    "timeout": 30
  }'

  if [ -f "$CURSOR_HOOKS_FILE" ]; then
    if grep -q "goal-stop.sh" "$CURSOR_HOOKS_FILE" 2>/dev/null; then
      log_info "Stop hook already configured in hooks.json"
      return
    fi

    cp "$CURSOR_HOOKS_FILE" "${CURSOR_HOOKS_FILE}.bak"
    log_info "Backed up existing hooks.json"

    if command -v jq &>/dev/null; then
      local TEMP_FILE
      TEMP_FILE=$(mktemp)
      jq --argjson entry "$HOOK_ENTRY" \
        '.hooks.stop = (.hooks.stop // []) + [$entry]' \
        "$CURSOR_HOOKS_FILE" > "$TEMP_FILE" && mv "$TEMP_FILE" "$CURSOR_HOOKS_FILE"
      log_info "Merged stop hook into existing hooks.json"
    else
      log_warn "jq not found. Please manually add the stop hook to $CURSOR_HOOKS_FILE"
      log_warn "Add to hooks.stop: $HOOK_ENTRY"
    fi
  else
    cat > "$CURSOR_HOOKS_FILE" << 'EOF'
{
  "version": 1,
  "hooks": {
    "stop": [
      {
        "command": "~/.cursor/skills/goal/goal-stop.sh",
        "loop_limit": null,
        "timeout": 30
      }
    ]
  }
}
EOF
    log_info "Created: $CURSOR_HOOKS_FILE"
  fi
}

print_summary() {
  echo ""
  echo -e "${GREEN}============================================${NC}"
  echo -e "${GREEN} /goal Autonomous Loop - Installed!         ${NC}"
  echo -e "${GREEN}============================================${NC}"
  echo ""
  echo "Components:"
  echo "  goal-manage.sh   $INSTALL_DIR/goal-manage.sh"
  echo "  goal-stop.sh     $INSTALL_DIR/goal-stop.sh"
  echo "  SKILL.md         $INSTALL_DIR/SKILL.md"
  echo "  hooks.json       $CURSOR_HOOKS_FILE (stop hook added)"
  echo "  Data dir         $DATA_DIR"
  echo ""
  echo "Usage in Cursor agent:"
  echo "  /goal \"all tests pass\" --test \"npm test\""
  echo "  /goal \"build succeeds\" --test \"npm run build\" --budget 30"
  echo "  /goal status"
  echo "  /goal pause | resume | clear"
  echo ""
}

main() {
  echo ""
  echo -e "${BLUE}================================${NC}"
  echo -e "${BLUE} Installing /goal skill         ${NC}"
  echo -e "${BLUE} Autonomous Loop for Cursor     ${NC}"
  echo -e "${BLUE}================================${NC}"
  echo ""

  check_dependencies
  install_skill_files
  configure_stop_hook
  print_summary
}

main "$@"
