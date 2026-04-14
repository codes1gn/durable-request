#!/usr/bin/env bash
# Find duplicate files in a directory tree by MD5 hash (content-based).
# Usage: treatment_02.sh [DIR]
# Default DIR is current directory.

set -euo pipefail

ROOT="${1:-.}"

if [[ ! -d "$ROOT" ]]; then
  echo "Not a directory: $ROOT" >&2
  exit 1
fi

# Sort by hash; print all lines that belong to duplicate hash groups (GNU uniq).
find "$ROOT" -type f -print0 \
  | xargs -0 -r md5sum -- \
  | sort -k1,1 \
  | uniq -w32 --all-repeated=separate
