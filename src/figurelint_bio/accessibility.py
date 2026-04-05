"""Accessibility checks for figure specs."""

from __future__ import annotations

from typing import Any

from ._data_loader import load_palettes_yaml


def check_colorblind_claim(spec: dict[str, Any]) -> list[dict]:
    """Verify colorblind_safe claim against palette registry."""
    issues: list[dict] = []
    palette_name = spec.get("palette_name")
    claims_cb = spec.get("colorblind_safe", False)

    if not claims_cb or not palette_name:
        return issues

    palettes = load_palettes_yaml()["palettes"]
    pal = palettes.get(palette_name)
    if pal is not None and not pal.get("colorblind_safe", False):
        issues.append({
            "rule": "colorblind_safe_claimed_but_palette_unsafe",
            "severity": "error",
            "message": (
                f"The spec declares colorblind_safe=true but palette "
                f"'{palette_name}' is not marked as colorblind-safe in the registry."
            ),
        })
    return issues


def check_grayscale_claim(spec: dict[str, Any]) -> list[dict]:
    """Verify grayscale_safe claim against palette registry."""
    issues: list[dict] = []
    palette_name = spec.get("palette_name")
    claims_gs = spec.get("grayscale_safe", False)

    if not claims_gs or not palette_name:
        return issues

    palettes = load_palettes_yaml()["palettes"]
    pal = palettes.get(palette_name)
    if pal is not None and not pal.get("grayscale_safe", False):
        issues.append({
            "rule": "grayscale_safe_claimed_but_palette_unsafe",
            "severity": "error",
            "message": (
                f"The spec declares grayscale_safe=true but palette "
                f"'{palette_name}' is not marked as grayscale-safe in the registry."
            ),
        })
    return issues


def check_clinical_colorblind_suggestion(spec: dict[str, Any]) -> list[dict]:
    """Suggest colorblind-safe palette for clinical figures."""
    issues: list[dict] = []
    if spec.get("field") != "clinical":
        return issues
    palette_name = spec.get("palette_name")
    if palette_name is None:
        return issues
    palettes = load_palettes_yaml()["palettes"]
    pal = palettes.get(palette_name)
    if pal is not None and not pal.get("colorblind_safe", False):
        issues.append({
            "rule": "colorblind_safe_not_claimed_for_clinical",
            "severity": "suggestion",
            "message": (
                "Field 'clinical' figures are recommended to use colorblind-safe "
                "palettes. Current palette is not verified colorblind-safe."
            ),
        })
    return issues
