"""Main lint entrypoint for FigureLint-Bio."""

from __future__ import annotations

from typing import Any

from .accessibility import (
    check_clinical_colorblind_suggestion,
    check_colorblind_claim,
    check_grayscale_claim,
)
from .rules import ALL_RULES
from .spec import validate_spec_schema


def lint_figure_spec(spec: dict[str, Any]) -> dict:
    """Run all lint rules against a figure spec dict.

    Parameters
    ----------
    spec : dict
        A figure spec mapping.  See :mod:`figurelint_bio.spec` for the
        full field reference.  Required fields: ``field``, ``figure_type``,
        ``variable_type``.

    Returns
    -------
    dict
        Keys:
        ``errors`` (list[dict]),
        ``warnings`` (list[dict]),
        ``suggestions`` (list[dict]),
        ``score`` (int, 0-100),
        ``summary`` (str),
        ``spec`` (the input spec, unchanged).

    Raises
    ------
    ValueError
        If required spec fields are missing or have wrong types.
    """
    # 1. Schema validation
    schema_errors = validate_spec_schema(spec)
    if schema_errors:
        raise ValueError(
            "Figure spec failed schema validation:\n"
            + "\n".join(f"  - {e}" for e in schema_errors)
        )

    errors: list[dict] = []
    warnings: list[dict] = []
    suggestions: list[dict] = []

    # 2. Structural lint rules
    for rule_fn in ALL_RULES:
        for issue in rule_fn(spec):
            sev = issue["severity"]
            if sev == "error":
                errors.append(issue)
            elif sev == "warning":
                warnings.append(issue)
            else:
                suggestions.append(issue)

    # 3. Accessibility checks
    for check_fn in (
        check_colorblind_claim,
        check_grayscale_claim,
        check_clinical_colorblind_suggestion,
    ):
        for issue in check_fn(spec):
            sev = issue["severity"]
            if sev == "error":
                errors.append(issue)
            elif sev == "warning":
                warnings.append(issue)
            else:
                suggestions.append(issue)

    # 4. Score (simple rule-based, 0-100)
    penalty = len(errors) * 20 + len(warnings) * 5 + len(suggestions) * 1
    score = max(0, 100 - penalty)

    # 5. Summary
    parts = []
    if errors:
        parts.append(f"{len(errors)} error{'s' if len(errors) != 1 else ''}")
    if warnings:
        parts.append(f"{len(warnings)} warning{'s' if len(warnings) != 1 else ''}")
    if suggestions:
        parts.append(f"{len(suggestions)} suggestion{'s' if len(suggestions) != 1 else ''}")
    summary = (
        "No issues found."
        if not parts
        else "Found: " + ", ".join(parts) + f".  Score: {score}/100."
    )

    return {
        "errors": errors,
        "warnings": warnings,
        "suggestions": suggestions,
        "score": score,
        "summary": summary,
        "spec": spec,
    }
