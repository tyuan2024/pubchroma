"""Palette validation utilities.

Cross-references a palette (by ID or hex list) against the registry and
field rules, returning structured warnings and validation status.
"""

from __future__ import annotations

from typing import Optional

from ._data_loader import load_field_rules, load_palettes_yaml


def validate_palette(
    palette_id: Optional[str] = None,
    hex_colors: Optional[list[str]] = None,
    field: Optional[str] = None,
    figure_type: Optional[str] = None,
    n_groups: Optional[int] = None,
    colorblind_safe: bool = False,
    grayscale_safe: bool = False,
) -> dict:
    """Validate a palette against registry metadata and field conventions.

    At least one of ``palette_id`` or ``hex_colors`` must be provided.

    Parameters
    ----------
    palette_id : str, optional
        A registered palette identifier (e.g. ``"clinical_categorical_conservative_4"``).
    hex_colors : list[str], optional
        Custom hex color list to validate (bypasses registry lookup).
    field : str, optional
        Scientific domain for field-specific rule checking.
    figure_type : str, optional
        Chart type for figure-specific rule checking.
    n_groups : int, optional
        Number of categories or levels.
    colorblind_safe : bool, optional
        Whether the figure claims colorblind safety.
    grayscale_safe : bool, optional
        Whether the figure claims grayscale safety.

    Returns
    -------
    dict
        Keys: ``valid`` (bool), ``palette_id``, ``hex``, ``errors``,
        ``warnings``, ``suggestions``.
    """
    if palette_id is None and hex_colors is None:
        raise ValueError("Provide at least one of palette_id or hex_colors.")

    palettes = load_palettes_yaml()["palettes"]
    errors: list[str] = []
    warnings: list[str] = []
    suggestions: list[str] = []

    pal_meta: Optional[dict] = None
    resolved_hex: list[str] = []

    if palette_id is not None:
        if palette_id not in palettes:
            errors.append(
                f"Palette '{palette_id}' is not in the registry. "
                f"Available: {', '.join(sorted(palettes))}."
            )
        else:
            pal_meta = palettes[palette_id]
            resolved_hex = list(pal_meta["colors"])
    if hex_colors is not None:
        resolved_hex = list(hex_colors)
        _validate_hex_format(hex_colors, errors)
        _check_rainbow_heuristic(hex_colors, errors)
        _check_red_green_bicolor(hex_colors, errors)

    if pal_meta is not None:
        # Capacity check
        if n_groups is not None and n_groups > pal_meta["n_max"]:
            errors.append(
                f"n_groups={n_groups} exceeds palette capacity n_max={pal_meta['n_max']}."
            )
        elif n_groups is not None and n_groups > pal_meta["n_max"] * 0.8:
            suggestions.append(
                f"n_groups={n_groups} is near the palette capacity "
                f"({pal_meta['n_max']}). Consider grouping categories."
            )

        # Colorblind / grayscale claim consistency
        if colorblind_safe and not pal_meta.get("colorblind_safe", False):
            errors.append(
                f"Palette '{palette_id}' is not marked colorblind-safe in the registry, "
                "but colorblind_safe=True was claimed."
            )
        if grayscale_safe and not pal_meta.get("grayscale_safe", False):
            errors.append(
                f"Palette '{palette_id}' is not marked grayscale-safe in the registry, "
                "but grayscale_safe=True was claimed."
            )

        # Field match
        if field is not None:
            _check_field_match(
                palette_id=palette_id,
                pal_meta=pal_meta,
                field=field,
                warnings=warnings,
                suggestions=suggestions,
            )

    return {
        "valid": len(errors) == 0,
        "palette_id": palette_id,
        "hex": resolved_hex,
        "errors": errors,
        "warnings": warnings,
        "suggestions": suggestions,
    }


def _validate_hex_format(hex_colors: list[str], errors: list[str]) -> None:
    for color in hex_colors:
        if not (color.startswith("#") and len(color) == 7):
            try:
                int(color[1:], 16)
            except (ValueError, IndexError):
                errors.append(f"Invalid hex color: '{color}'.")


def _check_rainbow_heuristic(hex_colors: list[str], errors: list[str]) -> None:
    # Heuristic: detect high hue spread with >7 colors (typical rainbow signature)
    if len(hex_colors) > 7:
        hues = _extract_hues(hex_colors)
        if hues and (max(hues) - min(hues)) > 300:
            errors.append(
                "Color list spans a wide hue range (>300°) with many colors. "
                "This is characteristic of a rainbow gradient, which is not recommended."
            )


def _check_red_green_bicolor(hex_colors: list[str], errors: list[str]) -> None:
    has_red = any(_is_red(c) for c in hex_colors)
    has_green = any(_is_green(c) for c in hex_colors)
    if has_red and has_green and len(hex_colors) <= 3:
        errors.append(
            "Red-green colour combination detected. This is the most common "
            "accessibility failure for colour-vision deficiency."
        )


def _check_field_match(
    palette_id: Optional[str],
    pal_meta: dict,
    field: str,
    warnings: list[str],
    suggestions: list[str],
) -> None:
    field_rules = load_field_rules()["fields"]
    field_cfg = field_rules.get(field, {})
    preferred_ids: list[str] = field_cfg.get("preferred_palette_ids", [])

    if palette_id and preferred_ids and palette_id not in preferred_ids:
        warnings.append(
            f"Palette '{palette_id}' is not in the preferred list for field '{field}'. "
            f"Preferred: {', '.join(preferred_ids)}."
        )

    if not field_cfg.get("colorblind_safe_required", False):
        if field_cfg.get("colorblind_safe_recommended", False):
            if not pal_meta.get("colorblind_safe", False):
                suggestions.append(
                    f"Field '{field}' recommends colorblind-safe palettes. "
                    "Current palette is not verified colorblind-safe."
                )


def _extract_hues(hex_colors: list[str]) -> list[float]:
    import colorsys
    hues = []
    for color in hex_colors:
        try:
            r = int(color[1:3], 16) / 255
            g = int(color[3:5], 16) / 255
            b = int(color[5:7], 16) / 255
            h, s, v = colorsys.rgb_to_hsv(r, g, b)
            if s > 0.2:  # only chromatic colors
                hues.append(h * 360)
        except (ValueError, IndexError):
            pass
    return hues


def _is_red(hex_color: str) -> bool:
    try:
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        return r > 180 and g < 100 and b < 100
    except (ValueError, IndexError):
        return False


def _is_green(hex_color: str) -> bool:
    try:
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        return g > 150 and r < 120 and b < 120
    except (ValueError, IndexError):
        return False
