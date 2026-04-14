#!/usr/bin/env bash
set -euo pipefail

echo "=== treat_01_sysinfo ==="
echo "timestamp_utc: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo "hostname: $(hostname 2>/dev/null || echo unknown)"
echo "kernel: $(uname -s 2>/dev/null || echo unknown) $(uname -r 2>/dev/null || echo unknown)"
echo "os_release:"
if [[ -r /etc/os-release ]]; then
  sed -n '1,6p' /etc/os-release | sed 's/^/  /'
else
  echo "  (not available)"
fi
echo "shell: ${SHELL:-unknown}"
echo "user: ${USER:-unknown}"
echo "cwd: $(pwd)"
echo "path_head: ${PATH:0:120}..."
echo "memory_mb (MemAvailable if present):"
if [[ -r /proc/meminfo ]]; then
  awk '/^MemAvailable:/ {printf "  %s kB (~%.0f MiB free)\n", $2, $2/1024}' /proc/meminfo || true
else
  echo "  (not available)"
fi
echo "disk_usage_cwd:"
df -h . 2>/dev/null | sed 's/^/  /' || echo "  (df failed)"
echo "=== end ==="
