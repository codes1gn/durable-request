from __future__ import annotations

from typing import Any


def nested_dict_to_flat_dict(
    nested: dict[str, Any],
    *,
    separator: str = ".",
) -> dict[str, Any]:
    """
    Convert a nested mapping into a flat dict whose keys encode nesting with
    ``separator`` (default: dot notation). Values that are plain dicts are
    walked recursively; any other value becomes a leaf.
    """
    flat: dict[str, Any] = {}

    def walk(obj: dict[str, Any], prefix: str) -> None:
        for key, value in obj.items():
            path = f"{prefix}{separator}{key}" if prefix else key
            if isinstance(value, dict):
                if value:
                    walk(value, path)
                else:
                    flat[path] = {}
            else:
                flat[path] = value

    walk(nested, "")
    return flat
