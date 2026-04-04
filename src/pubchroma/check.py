"""Colorblind-safety checking utilities."""

from __future__ import annotations

from .palettes import get_palette, list_journals, list_palettes


def is_colorblind_safe(journal: str, palette: str = "main") -> bool:
    """Check whether a palette is colorblind-safe.

    Parameters
    ----------
    journal : str
        Journal key (case-insensitive).
    palette : str, optional
        Palette name, by default ``"main"``.

    Returns
    -------
    bool
        True if the palette is marked as colorblind-safe.

    Examples
    --------
    >>> import pubchroma as pc
    >>> pc.is_colorblind_safe("nature")
    True
    >>> pc.is_colorblind_safe("science")
    False
    """
    return get_palette(journal, palette)["colorblind_safe"]


def list_colorblind_safe() -> list[dict]:
    """Return all colorblind-safe palettes across all journals.

    Returns
    -------
    list[dict]
        Each item has keys ``journal``, ``palette``, ``n_colors``.

    Examples
    --------
    >>> import pubchroma as pc
    >>> pc.list_colorblind_safe()  # doctest: +NORMALIZE_WHITESPACE
    [{'journal': 'colorblind', 'palette': 'okabe_ito', 'n_colors': 8}, ...]
    """
    results = []
    for journal in list_journals():
        for palette in list_palettes(journal):
            pal = get_palette(journal, palette)
            if pal["colorblind_safe"]:
                results.append({
                    "journal": journal,
                    "palette": palette,
                    "n_colors": len(pal["colors"]),
                })
    return results
