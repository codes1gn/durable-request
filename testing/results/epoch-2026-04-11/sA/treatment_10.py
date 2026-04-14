"""Nested mapping flattened to dot-notation string keys."""

from __future__ import annotations

from typing import Any


def nested_dict_to_flat(
    nested: dict[str, Any],
    *,
    separator: str = ".",
    prefix: str = "",
) -> dict[str, Any]:
    """
    Convert a nested dict into a single-level dict whose keys use dot notation.

    Only dict values are recursed; other values (including lists) are kept as-is.
    Empty nested dicts are preserved as a value under their dotted key.

    Examples:
        {"a": {"b": 1}} -> {"a.b": 1}
        {"x": 2, "y": {"z": 3}} -> {"x": 2, "y.z": 3}
        {"a": {}} -> {"a": {}}
    """
    flat: dict[str, Any] = {}
    for key, value in nested.items():
        path = f"{prefix}{separator}{key}" if prefix else key
        if isinstance(value, dict):
            if not value:
                flat[path] = {}
            else:
                flat.update(
                    nested_dict_to_flat(
                        value,
                        separator=separator,
                        prefix=path,
                    )
                )
        else:
            flat[path] = value
    return flat
