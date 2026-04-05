"""Field-aware palette recommendation engine.

Usage::

    from pubchroma.recommend import recommend_palette

    result = recommend_palette(
        field="clinical",
        figure_type="box",
        variable_type="categorical",
        n_groups=4,
        colorblind_safe=True,
    )
    print(result["palette_id"])
    print(result["hex"])
    print(result["rationale"])
"""

from __future__ import annotations

from typing import Optional

from ._data_loader import load_field_rules, load_palettes_yaml

# Valid input values
_VALID_FIELDS = {"clinical", "omics", "singlecell", "mechanism", "engineering"}
_VALID_FIGURE_TYPES = {
    "bar", "box", "violin", "line", "scatter", "heatmap", "volcano", "umap",
}
_VALID_VAR_TYPES = {"categorical", "sequential", "diverging"}
_VALID_JOURNAL_FAMILIES = {
    "cns_inspired", "medical_conservative", "engineering_high_contrast", "universal",
}


def recommend_palette(
    field: str,
    figure_type: str,
    variable_type: str = "categorical",
    n_groups: Optional[int] = None,
    journal_family: Optional[str] = None,
    colorblind_safe: bool = False,
    grayscale_safe: bool = False,
) -> dict:
    """Return the best-matching palette for the given figure context.

    Parameters
    ----------
    field : str
        Scientific domain.  One of: ``clinical``, ``omics``, ``singlecell``,
        ``mechanism``, ``engineering``.
    figure_type : str
        Chart type.  One of: ``bar``, ``box``, ``violin``, ``line``,
        ``scatter``, ``heatmap``, ``volcano``, ``umap``.
    variable_type : str, optional
        Data encoding type: ``categorical``, ``sequential``, or ``diverging``.
        Default ``"categorical"``.
    n_groups : int, optional
        Number of categories or levels.  Used to check palette capacity.
    journal_family : str, optional
        Preferred style family.  One of: ``cns_inspired``,
        ``medical_conservative``, ``engineering_high_contrast``, ``universal``.
        If ``None``, the field default is used.
    colorblind_safe : bool, optional
        Restrict to colorblind-safe palettes only.
    grayscale_safe : bool, optional
        Restrict to grayscale-safe palettes only.

    Returns
    -------
    dict
        Keys:
        ``palette_id``, ``hex``, ``n_max``, ``variable_type``,
        ``journal_family``, ``colorblind_safe``, ``grayscale_safe``,
        ``rationale``, ``warnings``,
        ``code_snippet_python``, ``code_snippet_r``.

    Raises
    ------
    ValueError
        If required inputs are invalid or no palette matches the constraints.
    """
    field = field.lower()
    figure_type = figure_type.lower()
    variable_type = variable_type.lower()

    if field not in _VALID_FIELDS:
        raise ValueError(f"field must be one of {sorted(_VALID_FIELDS)}, got '{field}'")
    if figure_type not in _VALID_FIGURE_TYPES:
        raise ValueError(
            f"figure_type must be one of {sorted(_VALID_FIGURE_TYPES)}, got '{figure_type}'"
        )
    if variable_type not in _VALID_VAR_TYPES:
        raise ValueError(
            f"variable_type must be one of {sorted(_VALID_VAR_TYPES)}, got '{variable_type}'"
        )
    if journal_family is not None and journal_family not in _VALID_JOURNAL_FAMILIES:
        raise ValueError(
            f"journal_family must be one of {sorted(_VALID_JOURNAL_FAMILIES)}, "
            f"got '{journal_family}'"
        )

    palettes = load_palettes_yaml()["palettes"]
    field_rules = load_field_rules()["fields"]
    field_cfg = field_rules.get(field, {})

    preferred_ids: list[str] = field_cfg.get("preferred_palette_ids", [])
    preferred_families: list[str] = field_cfg.get("preferred_journal_families", [])

    candidates = _filter_candidates(
        palettes=palettes,
        field=field,
        figure_type=figure_type,
        variable_type=variable_type,
        n_groups=n_groups,
        journal_family=journal_family or (preferred_families[0] if preferred_families else None),
        colorblind_safe=colorblind_safe,
        grayscale_safe=grayscale_safe,
        preferred_ids=preferred_ids,
    )

    if not candidates:
        # Relax constraints progressively
        candidates = _filter_candidates(
            palettes=palettes,
            field=field,
            figure_type=figure_type,
            variable_type=variable_type,
            n_groups=n_groups,
            journal_family=None,
            colorblind_safe=colorblind_safe,
            grayscale_safe=grayscale_safe,
            preferred_ids=preferred_ids,
        )

    if not candidates:
        raise ValueError(
            f"No palette found for field='{field}', figure_type='{figure_type}', "
            f"variable_type='{variable_type}', colorblind_safe={colorblind_safe}, "
            f"grayscale_safe={grayscale_safe}.  "
            "Try relaxing colorblind_safe or grayscale_safe constraints."
        )

    palette_id, pal = candidates[0]
    return _build_result(palette_id, pal, n_groups)


def _filter_candidates(
    palettes: dict,
    field: str,
    figure_type: str,
    variable_type: str,
    n_groups: Optional[int],
    journal_family: Optional[str],
    colorblind_safe: bool,
    grayscale_safe: bool,
    preferred_ids: list[str],
) -> list[tuple[str, dict]]:
    scored: list[tuple[int, str, dict]] = []

    for pid, pal in palettes.items():
        # Hard filters
        if variable_type and pal.get("variable_type") != variable_type:
            continue
        if colorblind_safe and not pal.get("colorblind_safe", False):
            continue
        if grayscale_safe and not pal.get("grayscale_safe", False):
            continue
        if n_groups is not None and n_groups > pal.get("n_max", 999):
            continue

        # Soft scoring (higher = better)
        score = 0
        if field in pal.get("field_tags", []):
            score += 10
        if figure_type in pal.get("figure_tags", []):
            score += 5
        if journal_family and pal.get("journal_family") == journal_family:
            score += 3
        if pid in preferred_ids:
            score += 8

        scored.append((score, pid, pal))

    scored.sort(key=lambda x: -x[0])
    return [(pid, pal) for _, pid, pal in scored]


def _build_result(palette_id: str, pal: dict, n_groups: Optional[int]) -> dict:
    hex_colors = pal["colors"]
    if n_groups is not None:
        hex_colors = hex_colors[:n_groups] if n_groups <= len(hex_colors) else hex_colors

    colors_r = ", ".join(f'"{c}"' for c in hex_colors)

    code_python = (
        f"from pubchroma.recommend import recommend_palette\n"
        f"result = recommend_palette(...)\n"
        f"colors = {list(hex_colors)}\n\n"
        f"# With matplotlib:\n"
        f"import matplotlib.pyplot as plt\n"
        f"from cycler import cycler\n"
        f"plt.rcParams['axes.prop_cycle'] = cycler(color=colors)"
    )

    code_r = (
        f"library(pubchroma)\n"
        f"colors <- c({colors_r})\n\n"
        f"# With ggplot2:\n"
        f"library(ggplot2)\n"
        f"scale_color_manual(values = colors)"
    )

    return {
        "palette_id": palette_id,
        "hex": list(hex_colors),
        "n_max": pal["n_max"],
        "variable_type": pal["variable_type"],
        "journal_family": pal.get("journal_family"),
        "colorblind_safe": pal.get("colorblind_safe", False),
        "grayscale_safe": pal.get("grayscale_safe", False),
        "rationale": pal.get("rationale", "").strip(),
        "warnings": pal.get("warnings", []),
        "code_snippet_python": code_python,
        "code_snippet_r": code_r,
    }
