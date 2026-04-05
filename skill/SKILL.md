# SKILL: pubchroma-figurelint

**Purpose**: Field-aware colour palette recommendation and pre-submission figure QA
for biomedical and engineering visualizations.

---

## Supported tasks

### 1. `recommend_palette`

Returns the best-matching palette for a given figure context.

**Input schema**

| Field | Type | Required | Description |
|---|---|---|---|
| `field` | str | yes | `clinical` \| `omics` \| `singlecell` \| `mechanism` \| `engineering` |
| `figure_type` | str | yes | `bar` \| `box` \| `violin` \| `line` \| `scatter` \| `heatmap` \| `volcano` \| `umap` |
| `variable_type` | str | no | `categorical` \| `sequential` \| `diverging` (default: `categorical`) |
| `n_groups` | int | no | Number of categories |
| `journal_family` | str | no | `cns_inspired` \| `medical_conservative` \| `engineering_high_contrast` \| `universal` |
| `colorblind_safe` | bool | no | Restrict to colorblind-safe palettes |
| `grayscale_safe` | bool | no | Restrict to grayscale-safe palettes |

**Output schema**

| Field | Type | Description |
|---|---|---|
| `palette_id` | str | Unique palette identifier |
| `hex` | list[str] | Hex color codes |
| `n_max` | int | Maximum recommended categories |
| `variable_type` | str | Palette encoding type |
| `journal_family` | str | Style family |
| `colorblind_safe` | bool | Registry flag |
| `grayscale_safe` | bool | Registry flag |
| `rationale` | str | One-line design rationale |
| `warnings` | list[str] | Any palette-level warnings |
| `code_snippet_python` | str | Ready-to-use Python code |
| `code_snippet_r` | str | Ready-to-use R code |

---

### 2. `validate_palette`

Cross-references a palette against registry metadata and field conventions.

**Input schema**

| Field | Type | Required | Description |
|---|---|---|---|
| `palette_id` | str | one of | Registered palette ID |
| `hex_colors` | list[str] | one of | Custom hex list |
| `field` | str | no | For field-specific checks |
| `n_groups` | int | no | For capacity checks |
| `colorblind_safe` | bool | no | Claimed safety flag |
| `grayscale_safe` | bool | no | Claimed safety flag |

**Output schema**

| Field | Type | Description |
|---|---|---|
| `valid` | bool | True if no errors |
| `palette_id` | str | Input palette ID |
| `hex` | list[str] | Resolved colors |
| `errors` | list[str] | Hard failures |
| `warnings` | list[str] | Advisory issues |
| `suggestions` | list[str] | Optional improvements |

---

### 3. `lint_figure_spec`

Runs 15 lint rules against a structured figure spec.

**Input schema** (required fields marked *)

| Field | Type | Description |
|---|---|---|
| `field` * | str | Scientific domain |
| `figure_type` * | str | Chart type |
| `variable_type` * | str | Data encoding |
| `title` | str | Figure title |
| `n_groups` | int | Number of categories |
| `palette_name` | str | Palette ID from registry |
| `hex` | list[str] | Custom hex list |
| `width_mm` | float | Figure width in millimetres |
| `height_mm` | float | Figure height in millimetres |
| `dpi` | int | Export resolution |
| `font_family` | str | Font name |
| `font_size_pt` | float | Axis label font size in points |
| `legend_items` | int | Number of legend entries |
| `legend_title` | str | Legend title text |
| `panel_count` | int | Number of figure panels |
| `has_statistics_annotation` | bool | Whether statistical annotations are present |
| `statistics_annotation_style` | str | `p_value` \| `stars` \| `none` |
| `colorblind_safe` | bool | Claimed colorblind safety |
| `grayscale_safe` | bool | Claimed grayscale safety |
| `export_format` | str | `pdf` \| `svg` \| `eps` \| `png` \| `tiff` |
| `notes` | str | Free-text notes (used for midpoint detection) |

**Output schema**

| Field | Type | Description |
|---|---|---|
| `errors` | list[dict] | Hard failures (rule, severity, message) |
| `warnings` | list[dict] | Advisory issues |
| `suggestions` | list[dict] | Optional improvements |
| `score` | int | 0–100 rule-based quality score |
| `summary` | str | One-line summary |
| `spec` | dict | Input spec (unmodified) |

---

## Decision logic

1. Schema validation — required fields checked first; raises `ValueError` on failure.
2. Structural rules — palette/field mismatch, rainbow detection, category count, diverging midpoint, legend, font, DPI, width, export, multipanel, statistics.
3. Accessibility checks — colorblind/grayscale claim consistency, clinical-field suggestion.
4. Score = 100 − (20 × errors) − (5 × warnings) − (1 × suggestions), floor 0.

---

## Constraints

- Does not parse rendered image files.
- Colorblind-safety is based on palette provenance, not per-pixel simulation.
- Rule thresholds (6 pt font, 300 DPI, 80 mm width) are derived from common journal guidelines and may not match the target journal exactly.
- R functions require `yaml` package; Python functions require `pyyaml`.

---

## Examples

### Python

```python
from pubchroma.recommend import recommend_palette
from figurelint_bio import lint_figure_spec, generate_markdown_report

result = recommend_palette("omics", "heatmap", variable_type="diverging")
spec = {
    "field": "omics",
    "figure_type": "heatmap",
    "variable_type": "diverging",
    "palette_name": result["palette_id"],
    "dpi": 600,
    "font_size_pt": 7,
    "width_mm": 174,
    "notes": "midpoint=0 for z-score",
}
report = lint_figure_spec(spec)
print(generate_markdown_report(report))
```

### R

```r
result <- recommend_palette("clinical", "box", n_groups = 4)
spec <- list(
  field = "clinical", figure_type = "box", variable_type = "categorical",
  palette_name = result$palette_id, dpi = 600, font_size_pt = 8, width_mm = 89
)
report <- lint_figure_spec(spec)
cat(report$summary)
```

---

## Extension points

- Add palettes: `data/palettes.yml` (no code changes required for basic lookup)
- Add lint rules: `data/lint_rules.yml` + `src/figurelint_bio/rules.py` + `ALL_RULES` registry
- Add fields: `data/field_rules.yml`
- R: add new rule functions in `R/R/figurelint.R`
- CLI: planned as a thin wrapper over `lint_figure_spec`
