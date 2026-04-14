"""
Flatten a nested dict to dot-notation keys.
"""

from __future__ import annotations

from typing import Any, Dict, Mapping, MutableMapping, Union

JSONValue = Union[None, bool, int, float, str, list, Mapping[str, Any]]


def flatten_dict(
    obj: Mapping[str, Any],
    *,
    sep: str = ".",
    parent_key: str = "",
) -> Dict[str, Any]:
    """
    Convert nested mappings to a flat dict with keys like ``a.b.c``.

    Only dict values are recursed into; lists and other values are stored as-is.

    Args:
        obj: Nested mapping (typically ``dict``).
        sep: Separator between path segments (default ``.``).
        parent_key: Prefix for recursion (usually empty for top-level call).

    Returns:
        A new flat ``dict`` with string keys.
    """
    flat: Dict[str, Any] = {}
    for k, v in obj.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else str(k)
        if isinstance(v, Mapping):
            flat.update(flatten_dict(v, sep=sep, parent_key=new_key))
        else:
            flat[new_key] = v
    return flat


def flatten_dict_inplace(
    target: MutableMapping[str, Any],
    obj: Mapping[str, Any],
    *,
    sep: str = ".",
    parent_key: str = "",
) -> None:
    """Like ``flatten_dict`` but writes into ``target``."""
    target.update(flatten_dict(obj, sep=sep, parent_key=parent_key))
