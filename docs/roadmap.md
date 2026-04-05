# Roadmap

This document lists planned development directions.
All items are tentative; priorities may shift based on user feedback.

## v0.3 (current)

- Monorepo structure with `pubchroma` and `figurelint_bio` as sibling packages
- Field-aware palette recommendation engine (`recommend_palette`)
- Palette validation against registry and field conventions (`validate_palette`)
- Figure spec lint with 15 rules and 3 severity levels (`lint_figure_spec`)
- R parity: `recommend_palette`, `validate_palette`, `lint_figure_spec`
- Shared YAML rule files (`data/palettes.yml`, `data/field_rules.yml`, etc.)

## Near-term (v0.4–v0.5)

- **CLI entrypoint**: `pubchroma recommend` and `figurelint spec.json`
- **Quarto / R Markdown integration**: inline lint badges and report blocks
- **Additional palettes**: sequential scales for continuous clinical outcomes,
  more omics diverging options
- **Additional lint rules**: axis scale type, error bar declaration, aspect ratio
- **R `yaml` dependency reduction**: bundle pre-parsed rule data as an RData file
  to avoid requiring yaml on the R side

## Medium-term (v0.6–v1.0)

- **matplotlib / ggplot2 object introspection**: read colours directly from
  rendered Figure or ggplot objects without requiring a spec
- **Per-pixel colorblind simulation**: Brettel–Viénot–Mollon simulation for
  palette validation
- **Expanded field coverage**: microscopy, structural biology, computational
  chemistry, geoscience

## Long-term (post-v1.0)

- **Image-level lint**: extract and analyse rasterised figure images
- **Interactive report**: HTML report with annotated figure mockups
- **Journal profile library**: opt-in per-journal rule overrides based on
  publicly available author guidelines
- **Integration with submission systems**: Overleaf plugin concept,
  pre-commit hook for figure directories
