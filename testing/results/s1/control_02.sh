#!/usr/bin/env bash
# Find duplicate files in a directory tree by MD5 hash.
# Usage: control_02.sh [directory]
set -euo pipefail

DIR="${1:-.}"

if [[ ! -d "$DIR" ]]; then
  echo "Not a directory: $DIR" >&2
  exit 1
fi

# md5sum output: "hash  path"; group by hash and show groups with >1 file
find "$DIR" -type f -print0 | xargs -0 md5sum 2>/dev/null | sort | awk '
  {
    h = $1
    $1 = ""
    sub(/^ /, "", $0)
    path = $0
    if (paths[h] != "") paths[h] = paths[h] "\n  " path
    else paths[h] = "  " path
    count[h]++
  }
  END {
    for (h in count) if (count[h] > 1) print h " (" count[h] " files):\n" paths[h] "\n"
  }
'
