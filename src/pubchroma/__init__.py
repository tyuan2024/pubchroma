"""PubChroma — journal-inspired color palettes for scientific figures."""

from .check import is_colorblind_safe, list_colorblind_safe
from .palettes import get_colors, get_palette, list_journals, list_palettes

__version__ = "0.2.0"
__all__ = [
    "get_colors",
    "get_palette",
    "is_colorblind_safe",
    "list_colorblind_safe",
    "list_journals",
    "list_palettes",
]
