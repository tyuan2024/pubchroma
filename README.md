# PubChroma + FigureLint-Bio

**A journal-inspired colour recommendation and figure QA toolkit for biomedical and engineering visualizations.**

[![PyPI version](https://img.shields.io/pypi/v/pubchroma.svg)](https://pypi.org/project/pubchroma/)
[![Python](https://img.shields.io/pypi/pyversions/pubchroma.svg)](https://pypi.org/project/pubchroma/)
[![Python CI](https://github.com/tyuan2024/pubchroma/actions/workflows/python.yml/badge.svg)](https://github.com/tyuan2024/pubchroma/actions/workflows/python.yml)
[![R CI](https://github.com/tyuan2024/pubchroma/actions/workflows/r.yml/badge.svg)](https://github.com/tyuan2024/pubchroma/actions/workflows/r.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Scope note**: This toolkit provides journal-*inspired* colour guidance and pre-submission figure QA.
> It does not represent official editorial standards of any journal or publisher.
> All palette selections and lint rule thresholds are derived from published
> accessibility research and common author guidelines.

---

## Why this project

Most colour palette libraries solve the *selection* problem in isolation. They do not account for:

- **Field conventions** — palettes appropriate for a clinical trial figure differ from those for a single-cell atlas.
- **Figure type** — a diverging heatmap has different requirements than a categorical boxplot.
- **Pre-submission audit** — there is no standard tool for checking that a figure's font size, DPI, legend count, and accessibility claims are internally consistent before journal submission.

PubChroma and FigureLint-Bio address these gaps as a single, minimal, rule-driven toolkit.

---

## Modules

### PubChroma

A rule-based colour recommendation and validation library.

- `get_colors(journal, palette, n)` — look up colours from the legacy journal-keyed registry
- `recommend_palette(field, figure_type, ...)` — field-aware and figure-aware palette selection
- `validate_palette(palette_id, ...)` — cross-reference a palette against registry metadata and field rules
- `pubchroma.matplotlib` — matplotlib colormap and cycler integration
- R: `recommend_palette()`, `validate_palette()`, `scale_color_pubchroma()`

### FigureLint-Bio

A spec-based pre-submission figure QA tool.

- `lint_figure_spec(spec)` — run 15 lint rules across palette, accessibility, typography, export, and annotation categories
- `generate_markdown_report(report)` — render results as a Markdown report
- Three severity levels: **error**, **warning**, **suggestion**
- Outputs a 0–100 score and a machine-readable report dict

All rule data lives in `data/*.yml` — consumed by both Python and R without duplication.

---

## Quick start

```bash
pip install pubchroma[recommend,plot]
```

```python
from pubchroma.recommend import recommend_palette
from figurelint_bio import lint_figure_spec, generate_markdown_report

# 1. Get a field-aware palette recommendation
result = recommend_palette(
    field="clinical",
    figure_type="box",
    variable_type="categorical",
    n_groups=4,
    colorblind_safe=True,
)
print(result["palette_id"])   # clinical_categorical_conservative_4
print(result["hex"])          # ['#374E55', '#DF8F44', '#00A1D5', '#B24745']

# 2. Lint the figure spec before submission
spec = {
    "field": "clinical",
    "figure_type": "box",
    "variable_type": "categorical",
    "palette_name": result["palette_id"],
    "n_groups": 4,
    "font_size_pt": 8,
    "dpi": 600,
    "width_mm": 89,
    "colorblind_safe": True,
    "export_format": "pdf",
}
report = lint_figure_spec(spec)
print(report["summary"])   # No issues found.
print(generate_markdown_report(report))
```

### R quick start

```r
# Install from GitHub
remotes::install_github("tyuan2024/pubchroma", subdir = "R")

library(pubchroma)

# Recommend a palette
result <- recommend_palette("clinical", "box", n_groups = 4, colorblind_safe = TRUE)
result$palette_id
result$hex

# Lint a figure spec
spec <- list(
  field = "clinical", figure_type = "box", variable_type = "categorical",
  palette_name = "clinical_categorical_conservative_4",
  font_size_pt = 8, dpi = 600, width_mm = 89
)
report <- lint_figure_spec(spec)
cat(report$summary)
```

---

## Supported fields and figure types

| Field | Typical figure types |
|---|---|
| `clinical` | bar, box, violin, line (survival) |
| `omics` | heatmap, volcano, scatter |
| `singlecell` | umap, scatter |
| `mechanism` | scatter, line, bar |
| `engineering` | bar, line, scatter, heatmap |

---

## FigureLint-Bio rules (v0.1)

| Category | Rules |
|---|---|
| Palette | field mismatch, figure-type mismatch, rainbow gradient, red-green bicolor |
| Accessibility | colorblind_safe / grayscale_safe claim verification, clinical field suggestion |
| Category count | capacity exceeded, near-limit suggestion |
| Diverging scale | undeclared midpoint |
| Typography | font below 6 pt (error), below 8 pt (suggestion) |
| Export | DPI below 300, figure width below 80 mm, raster for line art |
| Legend | more than 10 items, long label |
| Multi-panel | shared legend suggestion |
| Statistics | annotation on heatmap, stars without method note |

---

## Directory structure

```
pubchroma/
├── src/
│   ├── pubchroma/          # Palette lookup, recommend, validate, matplotlib integration
│   └── figurelint_bio/     # Figure spec lint and reporting
├── data/
│   ├── palettes/journals.json      # Legacy palette registry (journal-keyed)
│   ├── palettes.yml                # Field-aware palette definitions
│   ├── field_rules.yml             # Per-field conventions
│   ├── lint_rules.yml              # Lint rule definitions
│   └── accessibility_rules.yml    # Accessibility thresholds and criteria
├── R/                      # R package (palettes, recommend, validate, figurelint, ggplot2)
├── examples/
│   ├── python/             # Runnable Python examples
│   ├── specs/              # Example figure spec JSON files
│   └── r/                  # R examples
├── tests/python/           # Python test suite (78 tests, ≥80% coverage)
├── docs/                   # Architecture and design notes
└── skill/SKILL.md          # Machine-readable skill specification
```

---

## Palette registry

The `data/palettes.yml` file defines field-aware palettes with metadata:
- `colorblind_safe`, `grayscale_safe` flags
- `n_max` (recommended category limit)
- `field_tags`, `figure_tags`
- `rationale` (one-line design note)
- `journal_family`: `cns_inspired` | `medical_conservative` | `engineering_high_contrast` | `universal`

All palette data is the single source of truth for both Python and R.

---

## Installation

```bash
# Core palette lookup (no dependencies)
pip install pubchroma

# With matplotlib integration
pip install pubchroma[plot]

# With field-aware recommendation and FigureLint-Bio
pip install pubchroma[recommend]

# Everything
pip install pubchroma[all]
```

```r
# R package (development version)
remotes::install_github("tyuan2024/pubchroma", subdir = "R")
```

---

## Limitations

- Lint is **spec-based**: FigureLint-Bio reads a structured JSON/dict description of a figure.
  It does not parse rendered images or matplotlib/ggplot2 objects.
- Colorblind-safety classification is based on palette provenance and published guidelines,
  not per-pixel simulation.
- Palette coverage is intentionally narrow. The focus is correctness and extensibility,
  not breadth.

See [`docs/limitations.md`](docs/limitations.md) for a complete list.

---

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Citation

See [`CITATION.cff`](CITATION.cff).

## License

MIT — see [`LICENSE`](LICENSE).
