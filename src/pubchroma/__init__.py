"""PubChroma + FigureLint-Bio — journal-inspired color palettes and figure QA."""

from .check import is_colorblind_safe, list_colorblind_safe
from .palettes import get_colors, get_palette, list_journals, list_palettes

__version__ = "0.3.0"
__all__ = [
    "get_colors",
    "get_palette",
    "is_colorblind_safe",
    "list_colorblind_safe",
    "list_journals",
    "list_palettes",
]
