"""PubChroma — journal-inspired color palettes for scientific figures."""

from .palettes import get_palette, list_journals, list_palettes, get_colors
from .check import is_colorblind_safe, list_colorblind_safe

__version__ = "0.1.0"
__all__ = ["get_palette", "list_journals", "list_palettes", "get_colors", "is_colorblind_safe", "list_colorblind_safe"]
