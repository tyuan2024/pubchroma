# Changelog

All notable changes to PubChroma are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.2.0] - 2025-04-05

### Added
- **Matplotlib integration** (`pubchroma.matplotlib`): `get_cmap()`, `get_cycle()`,
  `show_palette()`, `show_all()` for seamless matplotlib usage
- `py.typed` marker for PEP 561 type-checking support
- Input validation: `get_colors(n=0)` and `n<0` now raise `ValueError` (Python & R)
- Parametrized tests covering all journals and edge cases (52 tests, 93% coverage)
- PyPI-ready metadata: classifiers, Changelog URL, `Typing :: Typed` classifier
- Contributing section in README
- `pip install pubchroma[plot]` optional dependency for matplotlib

### Changed
- Bumped version to 0.2.0
- Development status upgraded from Alpha to Beta
- README expanded with matplotlib integration examples and PyPI badges

## [0.1.0] - 2025-04-04

### Added
- Python package (`pubchroma`) with `get_colors`, `get_palette`, `list_journals`,
  `list_palettes`, `is_colorblind_safe`, `list_colorblind_safe`
- R package (`pubchroma`) with identical API
- ggplot2 integration: `scale_color_pubchroma`, `scale_fill_pubchroma`, `pubchroma_pal`
- Palette data for: Nature, Science, Cell, NEJM, Lancet, JAMA, PNAS, BMJ
- Colorblind-safe palettes: Okabe-Ito, Wong
- GitHub Actions CI for both Python and R
- Examples for Python (matplotlib) and R (ggplot2)
