#!/bin/bash
# install-steering.sh - Install durable-request steering for Cursor IDE
#
# Usage:
#   curl -sSL https://raw.githubusercontent.com/durable-request/durable-request/main/install-steering.sh | bash
#   # or
#   ./install-steering.sh
#
# This script installs:
#   1. steer CLI tool
#   2. steering-hook.sh (preToolUse hook)
#   3. Cursor hooks.json configuration
#   4. VSCode/Cursor extension (optional)

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
INSTALL_DIR="${HOME}/.durable-request"
BIN_DIR="${INSTALL_DIR}/bin"
HOOKS_DIR="${INSTALL_DIR}/hooks"
DATA_DIR="${INSTALL_DIR}/data"
CURSOR_HOOKS_FILE="${HOME}/.cursor/hooks.json"

# Source repo (for downloading)
REPO_URL="https://raw.githubusercontent.com/durable-request/durable-request/main"

log_info() {
  echo -e "${GREEN}[install]${NC} $1"
}

log_warn() {
  echo -e "${YELLOW}[install]${NC} $1"
}

log_error() {
  echo -e "${RED}[install]${NC} $1" >&2
}

log_step() {
  echo -e "${BLUE}==>${NC} $1"
}

# Create directories
create_directories() {
  log_step "Creating directories..."
  mkdir -p "$BIN_DIR" "$HOOKS_DIR" "$DATA_DIR"
  log_info "Created $INSTALL_DIR"
}

# Install steer CLI
install_steer_cli() {
  log_step "Installing steer CLI..."
  
  local STEER_PATH="$BIN_DIR/steer"
  
  # Check if we're running from the repo
  if [ -f "./skill/steer" ]; then
    cp "./skill/steer" "$STEER_PATH"
    log_info "Copied from local repo"
  else
    # Download from repo
    if command -v curl &> /dev/null; then
      curl -sSL "${REPO_URL}/skill/steer" -o "$STEER_PATH"
    elif command -v wget &> /dev/null; then
      wget -q "${REPO_URL}/skill/steer" -O "$STEER_PATH"
    else
      log_error "Neither curl nor wget found. Please install one."
      exit 1
    fi
    log_info "Downloaded from repo"
  fi
  
  chmod +x "$STEER_PATH"
  log_info "Installed: $STEER_PATH"
}

# Install steering hook
install_steering_hook() {
  log_step "Installing steering hook..."
  
  local HOOK_PATH="$HOOKS_DIR/steering-hook.sh"
  
  # Check if we're running from the repo
  if [ -f "./skill/steering-hook.sh" ]; then
    cp "./skill/steering-hook.sh" "$HOOK_PATH"
    log_info "Copied from local repo"
  else
    # Download from repo
    if command -v curl &> /dev/null; then
      curl -sSL "${REPO_URL}/skill/steering-hook.sh" -o "$HOOK_PATH"
    elif command -v wget &> /dev/null; then
      wget -q "${REPO_URL}/skill/steering-hook.sh" -O "$HOOK_PATH"
    else
      log_error "Neither curl nor wget found. Please install one."
      exit 1
    fi
    log_info "Downloaded from repo"
  fi
  
  chmod +x "$HOOK_PATH"
  log_info "Installed: $HOOK_PATH"
}

# Configure Cursor hooks
configure_cursor_hooks() {
  log_step "Configuring Cursor hooks..."
  
  local CURSOR_DIR="${HOME}/.cursor"
  mkdir -p "$CURSOR_DIR"
  
  local HOOK_ENTRY='{
    "command": "~/.durable-request/hooks/steering-hook.sh",
    "timeout_ms": 2000
  }'
  
  if [ -f "$CURSOR_HOOKS_FILE" ]; then
    # Check if hook already configured
    if grep -q "steering-hook.sh" "$CURSOR_HOOKS_FILE" 2>/dev/null; then
      log_info "Hook already configured in hooks.json"
      return
    fi
    
    # Backup existing
    cp "$CURSOR_HOOKS_FILE" "${CURSOR_HOOKS_FILE}.bak"
    log_info "Backed up existing hooks.json"
    
    # Try to merge with jq
    if command -v jq &> /dev/null; then
      local TEMP_FILE=$(mktemp)
      jq --argjson entry "$HOOK_ENTRY" \
        '.hooks.preToolUse = (.hooks.preToolUse // []) + [$entry]' \
        "$CURSOR_HOOKS_FILE" > "$TEMP_FILE" && mv "$TEMP_FILE" "$CURSOR_HOOKS_FILE"
      log_info "Merged hook into existing hooks.json"
    else
      log_warn "jq not found. Please manually add the hook to $CURSOR_HOOKS_FILE"
      log_warn "Add to hooks.preToolUse: $HOOK_ENTRY"
    fi
  else
    # Create new hooks.json
    cat > "$CURSOR_HOOKS_FILE" << 'EOF'
{
  "version": 1,
  "hooks": {
    "preToolUse": [
      {
        "command": "~/.durable-request/hooks/steering-hook.sh",
        "timeout_ms": 2000
      }
    ]
  }
}
EOF
    log_info "Created: $CURSOR_HOOKS_FILE"
  fi
}

# Add to PATH
configure_path() {
  log_step "Configuring PATH..."
  
  local PATH_EXPORT="export PATH=\"$BIN_DIR:\$PATH\""
  local SHELL_RC=""
  
  # Detect shell
  case "${SHELL:-/bin/bash}" in
    */zsh)
      SHELL_RC="$HOME/.zshrc"
      ;;
    */bash)
      if [ -f "$HOME/.bashrc" ]; then
        SHELL_RC="$HOME/.bashrc"
      elif [ -f "$HOME/.bash_profile" ]; then
        SHELL_RC="$HOME/.bash_profile"
      fi
      ;;
    *)
      SHELL_RC="$HOME/.profile"
      ;;
  esac
  
  if [ -n "$SHELL_RC" ] && [ -f "$SHELL_RC" ]; then
    if ! grep -q "durable-request" "$SHELL_RC" 2>/dev/null; then
      echo "" >> "$SHELL_RC"
      echo "# durable-request steering" >> "$SHELL_RC"
      echo "$PATH_EXPORT" >> "$SHELL_RC"
      log_info "Added to $SHELL_RC"
    else
      log_info "PATH already configured in $SHELL_RC"
    fi
  else
    log_warn "Could not find shell config. Add manually:"
    log_warn "  $PATH_EXPORT"
  fi
  
  # Also try to add symlink to /usr/local/bin if writable
  if [ -w /usr/local/bin ]; then
    ln -sf "$BIN_DIR/steer" /usr/local/bin/steer 2>/dev/null && \
      log_info "Created symlink: /usr/local/bin/steer"
  fi
}

# Install VSCode extension (optional)
install_extension() {
  log_step "Installing VSCode/Cursor extension..."
  
  local VSIX_PATH="./extensions/cursor-steer/durable-request-steer-0.1.0.vsix"
  
  # Check if VSIX exists locally
  if [ ! -f "$VSIX_PATH" ]; then
    # Try to download
    local DOWNLOAD_DIR=$(mktemp -d)
    VSIX_PATH="$DOWNLOAD_DIR/durable-request-steer-0.1.0.vsix"
    
    if command -v curl &> /dev/null; then
      curl -sSL "${REPO_URL}/extensions/cursor-steer/durable-request-steer-0.1.0.vsix" -o "$VSIX_PATH" 2>/dev/null || true
    fi
    
    if [ ! -f "$VSIX_PATH" ] || [ ! -s "$VSIX_PATH" ]; then
      log_warn "Extension VSIX not available for download"
      log_warn "Build manually: cd extensions/cursor-steer && npm install && npm run package"
      return 0
    fi
  fi
  
  # Try to install in Cursor
  if command -v cursor &> /dev/null; then
    cursor --install-extension "$VSIX_PATH" 2>/dev/null && \
      log_info "Installed extension in Cursor" || \
      log_warn "Could not install extension automatically"
  else
    log_warn "Cursor CLI not found. Install extension manually:"
    log_warn "  Extensions: Install from VSIX... → $VSIX_PATH"
  fi
}

# Print summary
print_summary() {
  echo ""
  echo -e "${GREEN}============================================${NC}"
  echo -e "${GREEN} Durable Request Steering - Installed!     ${NC}"
  echo -e "${GREEN}============================================${NC}"
  echo ""
  echo "Components installed:"
  echo "  ✓ steer CLI:       $BIN_DIR/steer"
  echo "  ✓ Steering hook:   $HOOKS_DIR/steering-hook.sh"
  echo "  ✓ Cursor config:   $CURSOR_HOOKS_FILE"
  echo ""
  echo "Usage:"
  echo "  # From terminal:"
  echo "  steer \"focus on the API layer\""
  echo "  steer --status"
  echo "  steer --clear"
  echo ""
  echo "  # From Cursor (if extension installed):"
  echo "  Press Ctrl+Shift+S (or Cmd+Shift+S on Mac)"
  echo "  Or click the 🔊 Steer button in the status bar"
  echo ""
  echo -e "${YELLOW}Note: Restart your shell or run:${NC}"
  echo "  source ~/.bashrc  # or ~/.zshrc"
  echo ""
}

# Main
main() {
  echo ""
  echo -e "${BLUE}================================${NC}"
  echo -e "${BLUE} Installing durable-request    ${NC}"
  echo -e "${BLUE} Steering for Cursor IDE       ${NC}"
  echo -e "${BLUE}================================${NC}"
  echo ""
  
  create_directories
  install_steer_cli
  install_steering_hook
  configure_cursor_hooks
  configure_path
  install_extension
  print_summary
}

main "$@"
