# Contributing to PubChroma + FigureLint-Bio

Contributions are welcome. This document describes the process and standards.

## What we are looking for

- **Bug reports** with a minimal reproducible example
- **New palettes** — well-sourced, clearly described, with field and figure-type tags
- **New lint rules** — rule ID, severity, applies_to, rationale; must be testable
- **R parity fixes** — keeping R and Python interfaces aligned
- **Documentation improvements** — clearer rationale, better examples

We are not looking for:

- Major API redesigns without prior discussion
- New dependencies beyond pyyaml and matplotlib
- Palettes that cannot be attributed or are aesthetically-motivated without a field rationale

## Development setup

```bash
git clone https://github.com/tyuan2024/pubchroma.git
cd pubchroma
pip install -e ".[dev,plot,recommend]"
pytest tests/python/
```

For R:

```r
install.packages(c("yaml", "jsonlite", "testthat", "ggplot2"))
cd R && Rscript -e 'testthat::test_local()'
```

## Adding a palette

1. Add an entry to `data/palettes.yml` following the existing schema.
2. Assign `field_tags`, `figure_tags`, `colorblind_safe`, `grayscale_safe`, `n_max`, and `rationale`.
3. If the palette copies colors from a published work, note the source in `rationale`.
4. Add a test in `tests/python/test_pubchroma.py` verifying the palette is returned by `recommend_palette`.

## Adding a lint rule

1. Add the rule definition to `data/lint_rules.yml`.
2. Implement the rule function in `src/figurelint_bio/rules.py` and register it in `ALL_RULES`.
3. Add at least one test that triggers the rule and one that does not.

## Commit style

```
type: short description

Optional body.
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`.

## Pull requests

- One logical change per PR.
- Tests must pass (`pytest --cov-fail-under=80`).
- Ruff lint must pass (`ruff check src/`).
- Update `CHANGELOG.md`.

## Code of conduct

See [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).
