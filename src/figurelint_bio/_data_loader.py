"""YAML data loader for figurelint_bio.

Loads rule files from the shared data/ directory at the repository root.
Both pubchroma and figurelint_bio read from the same YAML files —
this module is a sibling loader that resolves paths independently.
"""

from __future__ import annotations

import functools
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore[assignment]

# src/figurelint_bio/_data_loader.py → ../../../data/
_DATA_DIR = Path(__file__).parent.parent.parent / "data"


def _load_yaml(filename: str) -> dict[str, Any]:
    if yaml is None:
        raise ImportError(
            "PyYAML is required. Install it with: pip install pubchroma[recommend]"
        )
    path = _DATA_DIR / filename
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


@functools.lru_cache(maxsize=None)
def load_palettes_yaml() -> dict[str, Any]:
    return _load_yaml("palettes.yml")


@functools.lru_cache(maxsize=None)
def load_field_rules() -> dict[str, Any]:
    return _load_yaml("field_rules.yml")


@functools.lru_cache(maxsize=None)
def load_lint_rules() -> dict[str, Any]:
    return _load_yaml("lint_rules.yml")


@functools.lru_cache(maxsize=None)
def load_accessibility_rules() -> dict[str, Any]:
    return _load_yaml("accessibility_rules.yml")
