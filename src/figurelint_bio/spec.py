"""Figure spec schema definition and validation.

A figure spec is a JSON-serialisable dict describing the key properties
of a single figure (or multi-panel figure) as declared by the researcher.
FigureLint-Bio performs structural lint on this spec—it does not parse
image files or rendered output.
"""

from __future__ import annotations

from typing import Any

# Required field names and their expected Python types.
REQUIRED_FIELDS: dict[str, type] = {
    "field": str,
    "figure_type": str,
    "variable_type": str,
}

OPTIONAL_FIELDS: dict[str, Any] = {
    "title": str,
    "n_groups": int,
    "journal_family": str,
    "palette_name": str,
    "hex": list,
    "width_mm": (int, float),
    "height_mm": (int, float),
    "dpi": (int, float),
    "font_family": str,
    "font_size_pt": (int, float),
    "legend_items": int,
    "legend_title": str,
    "panel_count": int,
    "has_statistics_annotation": bool,
    "statistics_annotation_style": str,
    "colorblind_safe": bool,
    "grayscale_safe": bool,
    "export_format": str,
    "notes": str,
}

VALID_FIELDS = {"clinical", "omics", "singlecell", "mechanism", "engineering"}
VALID_FIGURE_TYPES = {
    "bar", "box", "violin", "line", "scatter", "heatmap", "volcano", "umap",
}
VALID_VARIABLE_TYPES = {"categorical", "sequential", "diverging"}


def validate_spec_schema(spec: dict[str, Any]) -> list[str]:
    """Check that spec has required fields with correct types.

    Returns a list of schema error strings (empty = valid schema).
    """
    errors: list[str] = []

    for field, ftype in REQUIRED_FIELDS.items():
        if field not in spec:
            errors.append(f"Required field '{field}' is missing.")
        elif not isinstance(spec[field], ftype):
            errors.append(
                f"Field '{field}' must be {ftype.__name__}, "
                f"got {type(spec[field]).__name__}."
            )

    if "field" in spec and spec["field"] not in VALID_FIELDS:
        errors.append(
            f"field='{spec['field']}' is not recognised. "
            f"Valid values: {sorted(VALID_FIELDS)}."
        )
    if "figure_type" in spec and spec["figure_type"] not in VALID_FIGURE_TYPES:
        errors.append(
            f"figure_type='{spec['figure_type']}' is not recognised. "
            f"Valid values: {sorted(VALID_FIGURE_TYPES)}."
        )
    if "variable_type" in spec and spec["variable_type"] not in VALID_VARIABLE_TYPES:
        errors.append(
            f"variable_type='{spec['variable_type']}' is not recognised. "
            f"Valid values: {sorted(VALID_VARIABLE_TYPES)}."
        )

    for field, ftype in OPTIONAL_FIELDS.items():
        if field in spec and spec[field] is not None:
            if not isinstance(spec[field], ftype):
                expected = (
                    ftype.__name__ if isinstance(ftype, type)
                    else " or ".join(t.__name__ for t in ftype)
                )
                errors.append(
                    f"Optional field '{field}' must be {expected}, "
                    f"got {type(spec[field]).__name__}."
                )

    return errors


def get_field(spec: dict[str, Any], key: str, default: Any = None) -> Any:
    """Safe accessor with default."""
    return spec.get(key, default)
