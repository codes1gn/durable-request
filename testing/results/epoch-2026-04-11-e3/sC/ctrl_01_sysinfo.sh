#!/usr/bin/env bash
set -euo pipefail
echo "hostname: $(hostname)"
echo "date: $(date -Is 2>/dev/null || date)"
echo "uptime: $(uptime -p 2>/dev/null || uptime)"
