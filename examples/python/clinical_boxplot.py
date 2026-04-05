"""
Clinical boxplot — PubChroma + FigureLint-Bio example.

Demonstrates:
  1. Recommending a palette for a clinical subgroup comparison.
  2. Validating the palette against field conventions.
  3. Running FigureLint-Bio on the figure spec.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../src"))

from pubchroma.recommend import recommend_palette
from pubchroma.validate import validate_palette
from figurelint_bio import lint_figure_spec, generate_markdown_report

# ── 1. Recommend a palette ─────────────────────────────────────────────────
result = recommend_palette(
    field="clinical",
    figure_type="box",
    variable_type="categorical",
    n_groups=4,
    colorblind_safe=True,
)

print("Recommended palette:", result["palette_id"])
print("Colors:", result["hex"])
print("Rationale:", result["rationale"])
if result["warnings"]:
    print("Warnings:", result["warnings"])

# ── 2. Validate the palette ────────────────────────────────────────────────
validation = validate_palette(
    palette_id=result["palette_id"],
    field="clinical",
    n_groups=4,
    colorblind_safe=True,
)
print("\nValidation passed:", validation["valid"])

# ── 3. Lint the figure spec ────────────────────────────────────────────────
spec = {
    "title": "Treatment-group comparison: biomarker levels by arm",
    "field": "clinical",
    "figure_type": "box",
    "variable_type": "categorical",
    "n_groups": 4,
    "palette_name": result["palette_id"],
    "font_size_pt": 8,
    "dpi": 600,
    "width_mm": 89,
    "legend_items": 4,
    "colorblind_safe": True,
    "export_format": "pdf",
}

report = lint_figure_spec(spec)
print("\n" + generate_markdown_report(report))

# ── 4. Optional matplotlib plot ────────────────────────────────────────────
try:
    import matplotlib.pyplot as plt
    import numpy as np

    rng = np.random.default_rng(42)
    arms = ["Placebo", "Low dose", "Mid dose", "High dose"]
    data = [rng.normal(loc, 0.8, 30) for loc in [0, 0.5, 1.0, 1.5]]

    fig, ax = plt.subplots(figsize=(89 / 25.4, 89 / 25.4))
    bp = ax.boxplot(data, patch_artist=True, notch=False)

    colors = result["hex"]
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.85)

    ax.set_xticklabels(arms, fontsize=8)
    ax.set_ylabel("Biomarker level (AU)", fontsize=8)
    ax.set_title("Clinical subgroup comparison", fontsize=9)
    plt.tight_layout()
    plt.savefig(
        os.path.join(os.path.dirname(__file__), "clinical_boxplot_output.pdf"),
        dpi=600,
        bbox_inches="tight",
    )
    print("Plot saved to clinical_boxplot_output.pdf")
except ImportError:
    print("(matplotlib not installed — skipping plot)")
