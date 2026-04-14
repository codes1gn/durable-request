"""Flatten nested dicts to dot-notation keys."""

from __future__ import annotations

from typing import Any, Dict, Mapping


def flatten_dict(
    nested: Mapping[str, Any],
    *,
    parent_key: str = "",
    sep: str = ".",
) -> Dict[str, Any]:
    """
    Convert a nested dict to a flat dict with dot-separated keys.

    Nested dict-like mappings are recursed; lists, scalars, and other values are leaves.
    """
    out: Dict[str, Any] = {}
    for k, v in nested.items():
        key = f"{parent_key}{sep}{k}" if parent_key else str(k)
        if isinstance(v, Mapping) and not isinstance(v, (str, bytes)):
            out.update(flatten_dict(v, parent_key=key, sep=sep))
        else:
            out[key] = v
    return out
