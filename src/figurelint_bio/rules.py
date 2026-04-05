"""Individual lint rule implementations.

Each rule function accepts a figure spec dict and returns a (possibly empty)
list of issue dicts.  Each issue dict has:
  - rule:     rule identifier (snake_case)
  - severity: "error" | "warning" | "suggestion"
  - message:  human-readable description
"""

from __future__ import annotations

from typing import Any

from ._data_loader import load_field_rules, load_palettes_yaml

# Thresholds (sourced from accessibility_rules.yml to keep logic DRY)
_MIN_FONT_SIZE = 6.0
_RECOMMENDED_FONT_SIZE = 8.0
_MIN_DPI = 300
_MIN_WIDTH_MM = 80.0
_MAX_LEGEND_ITEMS = 10
_MAX_LEGEND_LABEL_CHARS = 30

_RAINBOW_NAMES = {
    "jet", "rainbow", "hsv", "gist_rainbow", "nipy_spectral", "spectral",
    "gist_ncar",
}
_RED_GREEN_NAMES = {
    "red_green", "redgreen", "rg_bicolor", "green_red",
}


# ── Palette × field / figure_type ────────────────────────────────────────────

def rule_palette_field_mismatch(spec: dict[str, Any]) -> list[dict]:
    palette_name = spec.get("palette_name")
    field = spec.get("field")
    if not palette_name or not field:
        return []

    field_rules = load_field_rules()["fields"]
    field_cfg = field_rules.get(field, {})
    preferred = field_cfg.get("preferred_palette_ids", [])

    if preferred and palette_name not in preferred:
        return [{
            "rule": "palette_field_mismatch",
            "severity": "warning",
            "message": (
                f"Palette '{palette_name}' is not recommended for field '{field}'. "
                f"Preferred palettes: {', '.join(preferred)}."
            ),
        }]
    return []


def rule_palette_figure_type_mismatch(spec: dict[str, Any]) -> list[dict]:
    palette_name = spec.get("palette_name")
    figure_type = spec.get("figure_type")
    if not palette_name or not figure_type:
        return []

    palettes = load_palettes_yaml()["palettes"]
    pal = palettes.get(palette_name)
    if pal is None:
        return []

    if figure_type not in pal.get("figure_tags", []):
        return [{
            "rule": "palette_figure_type_mismatch",
            "severity": "warning",
            "message": (
                f"Palette '{palette_name}' is not tagged for figure type "
                f"'{figure_type}'.  It is intended for: "
                f"{', '.join(pal.get('figure_tags', []))}."
            ),
        }]
    return []


# ── Disallowed palette patterns ───────────────────────────────────────────────

def rule_rainbow_palette(spec: dict[str, Any]) -> list[dict]:
    palette_name = (spec.get("palette_name") or "").lower()
    if palette_name in _RAINBOW_NAMES:
        return [{
            "rule": "rainbow_palette_detected",
            "severity": "error",
            "message": (
                "Rainbow or spectral colour gradients are not recommended. "
                "They introduce perceptual non-linearity and are not colorblind-safe."
            ),
        }]
    return []


def rule_red_green_bicolor(spec: dict[str, Any]) -> list[dict]:
    palette_name = (spec.get("palette_name") or "").lower()
    if palette_name in _RED_GREEN_NAMES:
        return [{
            "rule": "red_green_bicolor_detected",
            "severity": "error",
            "message": (
                "Red-green colour combination detected. This is the most common "
                "accessibility failure for colour-vision deficiency. "
                "Replace with a deuteranopia-safe alternative."
            ),
        }]
    return []


# ── Category count ────────────────────────────────────────────────────────────

def rule_too_many_categories(spec: dict[str, Any]) -> list[dict]:
    n_groups = spec.get("n_groups")
    palette_name = spec.get("palette_name")
    if n_groups is None or palette_name is None:
        return []

    palettes = load_palettes_yaml()["palettes"]
    pal = palettes.get(palette_name)
    if pal is None:
        return []

    n_max = pal.get("n_max", 999)
    if n_groups > n_max:
        return [{
            "rule": "too_many_categories",
            "severity": "error",
            "message": (
                f"{n_groups} categories exceed the recommended maximum ({n_max}) "
                f"for palette '{palette_name}'. "
                "Perceptual discrimination degrades above this threshold."
            ),
        }]
    if n_groups > n_max * 0.85:
        return [{
            "rule": "many_categories_suggestion",
            "severity": "suggestion",
            "message": (
                f"{n_groups} categories is near the upper limit ({n_max}) "
                f"for palette '{palette_name}'. "
                "Consider grouping less important categories."
            ),
        }]
    return []


# ── Diverging palette midpoint ─────────────────────────────────────────────────

def rule_diverging_no_midpoint(spec: dict[str, Any]) -> list[dict]:
    variable_type = spec.get("variable_type", "")
    if variable_type != "diverging":
        return []
    # A spec with explicit notes about midpoint is acceptable
    notes = (spec.get("notes") or "").lower()
    if any(kw in notes for kw in ("midpoint", "zero", "center", "centre")):
        return []
    return [{
        "rule": "diverging_no_explicit_midpoint",
        "severity": "warning",
        "message": (
            "A diverging palette is selected but no midpoint reference is "
            "declared in the spec notes. Readers may misinterpret the zero reference. "
            "Add a 'notes' field describing the midpoint (e.g. 'midpoint=0 for logFC')."
        ),
    }]


# ── Legend ─────────────────────────────────────────────────────────────────────

def rule_legend_too_many_items(spec: dict[str, Any]) -> list[dict]:
    legend_items = spec.get("legend_items")
    if legend_items is None:
        return []
    if legend_items > _MAX_LEGEND_ITEMS:
        return [{
            "rule": "legend_too_many_items",
            "severity": "warning",
            "message": (
                f"Legend has {legend_items} items. Legends with more than "
                f"{_MAX_LEGEND_ITEMS} items are difficult to read in print."
            ),
        }]
    return []


def rule_legend_label_too_long(spec: dict[str, Any]) -> list[dict]:
    legend_title = spec.get("legend_title") or ""
    width_mm = spec.get("width_mm")
    if len(legend_title) > _MAX_LEGEND_LABEL_CHARS and width_mm is not None:
        return [{
            "rule": "legend_item_label_too_long",
            "severity": "suggestion",
            "message": (
                f"Legend title '{legend_title[:40]}...' may be too long "
                f"for the declared figure width ({width_mm} mm). "
                f"Keep legend labels under {_MAX_LEGEND_LABEL_CHARS} characters."
            ),
        }]
    return []


# ── Typography ─────────────────────────────────────────────────────────────────

def rule_font_size(spec: dict[str, Any]) -> list[dict]:
    font_size = spec.get("font_size_pt")
    if font_size is None:
        return []
    if font_size < _MIN_FONT_SIZE:
        return [{
            "rule": "font_size_too_small",
            "severity": "error",
            "message": (
                f"Font size {font_size} pt is below the {_MIN_FONT_SIZE} pt minimum. "
                "Most journals require at least 6–7 pt for axis labels in final figures."
            ),
        }]
    if font_size < _RECOMMENDED_FONT_SIZE:
        return [{
            "rule": "font_size_small_suggestion",
            "severity": "suggestion",
            "message": (
                f"Font size {font_size} pt is below the commonly recommended "
                f"{_RECOMMENDED_FONT_SIZE} pt for axis labels. "
                "Consider 8–10 pt for final submission."
            ),
        }]
    return []


# ── Export / resolution ────────────────────────────────────────────────────────

def rule_dpi(spec: dict[str, Any]) -> list[dict]:
    dpi = spec.get("dpi")
    if dpi is None:
        return []
    if dpi < _MIN_DPI:
        return [{
            "rule": "dpi_below_minimum",
            "severity": "error",
            "message": (
                f"DPI {dpi} is below {_MIN_DPI}. Most journals require ≥300 dpi "
                "for raster figures (≥600 dpi for line art)."
            ),
        }]
    return []


def rule_figure_width(spec: dict[str, Any]) -> list[dict]:
    width_mm = spec.get("width_mm")
    if width_mm is None:
        return []
    if width_mm < _MIN_WIDTH_MM:
        return [{
            "rule": "figure_width_too_small",
            "severity": "warning",
            "message": (
                f"Figure width {width_mm} mm is below the single-column minimum "
                f"({_MIN_WIDTH_MM} mm) for most journals. "
                "Verify the target journal's figure size specifications."
            ),
        }]
    return []


def rule_vector_export_suggestion(spec: dict[str, Any]) -> list[dict]:
    export_format = (spec.get("export_format") or "").lower()
    figure_type = spec.get("figure_type", "")
    raster_formats = {"png", "jpg", "jpeg", "tiff", "tif", "bmp"}
    line_types = {"bar", "box", "violin", "line", "scatter", "volcano"}
    if export_format in raster_formats and figure_type in line_types:
        return [{
            "rule": "export_format_raster_for_lineart",
            "severity": "suggestion",
            "message": (
                f"Figure type '{figure_type}' contains line art. "
                f"Consider exporting as PDF, SVG, or EPS alongside '{export_format}' "
                "to preserve sharpness at any print resolution."
            ),
        }]
    return []


# ── Panel complexity ───────────────────────────────────────────────────────────

def rule_multipanel_shared_legend(spec: dict[str, Any]) -> list[dict]:
    panel_count = spec.get("panel_count") or 1
    n_groups = spec.get("n_groups")
    if panel_count >= 3 and n_groups is not None:
        return [{
            "rule": "multipanel_shared_legend_suggested",
            "severity": "suggestion",
            "message": (
                f"Figure has {panel_count} panels. Multi-panel figures with "
                "identical colour mappings should use a shared legend to reduce redundancy."
            ),
        }]
    return []


# ── Statistical annotation ─────────────────────────────────────────────────────

def rule_stats_on_heatmap(spec: dict[str, Any]) -> list[dict]:
    if spec.get("has_statistics_annotation") and spec.get("figure_type") == "heatmap":
        return [{
            "rule": "stats_annotation_on_continuous_heatmap",
            "severity": "suggestion",
            "message": (
                "Statistical annotations are declared on a heatmap. "
                "Verify that annotations refer to specific comparisons, "
                "not the entire matrix."
            ),
        }]
    return []


def rule_stats_stars(spec: dict[str, Any]) -> list[dict]:
    if (
        spec.get("has_statistics_annotation")
        and spec.get("statistics_annotation_style") == "stars"
    ):
        return [{
            "rule": "stats_stars_without_method_note",
            "severity": "suggestion",
            "message": (
                "Statistics annotation style is 'stars'. Consider adding a "
                "methods note specifying the test used and multiple-comparison "
                "correction method."
            ),
        }]
    return []


# ── Registry of all rules ─────────────────────────────────────────────────────

ALL_RULES = [
    rule_palette_field_mismatch,
    rule_palette_figure_type_mismatch,
    rule_rainbow_palette,
    rule_red_green_bicolor,
    rule_too_many_categories,
    rule_diverging_no_midpoint,
    rule_legend_too_many_items,
    rule_legend_label_too_long,
    rule_font_size,
    rule_dpi,
    rule_figure_width,
    rule_vector_export_suggestion,
    rule_multipanel_shared_legend,
    rule_stats_on_heatmap,
    rule_stats_stars,
]
