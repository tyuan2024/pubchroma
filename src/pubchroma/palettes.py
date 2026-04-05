"""Core palette loading and recommendation functions."""

from __future__ import annotations

import json
from importlib.resources import files
from typing import Optional


def _load_data() -> dict:
    """Load palette data from the bundled JSON file."""
    data_path = files("pubchroma").joinpath("data/journals.json")
    return json.loads(data_path.read_text(encoding="utf-8"))


_DATA: dict | None = None


def _get_data() -> dict:
    global _DATA
    if _DATA is None:
        _DATA = _load_data()
    return _DATA


def list_journals() -> list[str]:
    """Return all available journal keys.

    Returns
    -------
    list[str]
        Sorted list of journal keys (e.g. ['bmj', 'cell', 'jama', ...]).

    Examples
    --------
    >>> import pubchroma as pc
    >>> pc.list_journals()
    ['bmj', 'cell', 'colorblind', 'jama', 'lancet', 'nature', 'nejm', 'pnas', 'science']
    """
    return sorted(_get_data().keys())


def list_palettes(journal: str) -> list[str]:
    """Return all palette names for a given journal.

    Parameters
    ----------
    journal : str
        Journal key (case-insensitive). Use :func:`list_journals` to see options.

    Returns
    -------
    list[str]
        Sorted list of palette names for that journal.

    Raises
    ------
    ValueError
        If the journal key is not found.

    Examples
    --------
    >>> import pubchroma as pc
    >>> pc.list_palettes("nature")
    ['light', 'main']
    """
    data = _get_data()
    key = journal.lower()
    if key not in data:
        available = ", ".join(sorted(data.keys()))
        raise ValueError(f"Journal '{journal}' not found. Available: {available}")
    return sorted(data[key]["palettes"].keys())


def get_palette(journal: str, palette: str = "main") -> dict:
    """Return full palette metadata for a journal.

    Parameters
    ----------
    journal : str
        Journal key (case-insensitive).
    palette : str, optional
        Palette name within that journal, by default ``"main"``.

    Returns
    -------
    dict
        Dictionary with keys: ``colors``, ``colorblind_safe``, ``description``, ``type``.

    Raises
    ------
    ValueError
        If the journal or palette is not found.

    Examples
    --------
    >>> import pubchroma as pc
    >>> p = pc.get_palette("nature")
    >>> p["colors"][:3]
    ['#E64B35', '#4DBBD5', '#00A087']
    """
    data = _get_data()
    key = journal.lower()
    if key not in data:
        available = ", ".join(sorted(data.keys()))
        raise ValueError(f"Journal '{journal}' not found. Available: {available}")
    palettes = data[key]["palettes"]
    pal = palette.lower()
    if pal not in palettes:
        available = ", ".join(sorted(palettes.keys()))
        raise ValueError(f"Palette '{palette}' not found for '{journal}'. Available: {available}")
    return palettes[pal]


def get_colors(
    journal: str,
    palette: str = "main",
    n: Optional[int] = None,
    colorblind_only: bool = False,
) -> list[str]:
    """Return hex color codes for a journal palette.

    Parameters
    ----------
    journal : str
        Journal key (case-insensitive).
    palette : str, optional
        Palette name, by default ``"main"``.
    n : int, optional
        Number of colors to return. If None, returns all colors.
        If ``n`` exceeds the palette length, colors are cycled.
    colorblind_only : bool, optional
        If True, raise an error when the palette is not colorblind-safe.

    Returns
    -------
    list[str]
        List of hex color strings (e.g. ``['#E64B35', '#4DBBD5', ...]``).

    Raises
    ------
    ValueError
        If ``colorblind_only=True`` and the palette is not colorblind-safe,
        or if the journal/palette is not found.

    Examples
    --------
    >>> import pubchroma as pc
    >>> pc.get_colors("nature", n=3)
    ['#E64B35', '#4DBBD5', '#00A087']
    >>> pc.get_colors("colorblind", "okabe_ito", colorblind_only=True)
    ['#E69F00', '#56B4E9', '#009E73', '#F0E442', '#0072B2', '#D55E00', '#CC79A7', '#000000']
    """
    pal = get_palette(journal, palette)

    if colorblind_only and not pal["colorblind_safe"]:
        raise ValueError(
            f"Palette '{palette}' for '{journal}' is not colorblind-safe. "
            "Use colorblind_only=False or choose a colorblind-safe palette."
        )

    colors = pal["colors"]
    if n is None:
        return list(colors)

    if n <= 0:
        raise ValueError(f"n must be a positive integer, got {n}")

    if n <= len(colors):
        return colors[:n]

    # Cycle colors if n > palette length
    cycles = (n // len(colors)) + 1
    return (colors * cycles)[:n]
