# Limitations

This document states what FigureLint-Bio v0.1 does **not** do.

## No image-level analysis

FigureLint-Bio operates on **structured figure specs** — JSON or dict descriptions
provided by the researcher. It does not:

- Parse rendered image files (PNG, TIFF, PDF)
- Analyse matplotlib Figure or ggplot2 object internals
- Detect actual colours used in a rendered plot
- Extract text from images

This is a deliberate design choice. Spec-based lint is fast, deterministic,
and integrable into any scripted workflow without image rendering dependencies.
Image-level analysis is listed in the roadmap.

## No per-pixel colorblind simulation

Colorblind-safety classification is based on palette provenance and published
colour-vision deficiency research. The toolkit does not:

- Run Brettel, Viénot, or Mollon simulation algorithms
- Compute perceptual distances in LMS or CAM02 space
- Auto-correct unsafe palettes

## No journal-specific rule sets

Lint thresholds (6 pt font, 300 DPI, 80 mm width) are derived from commonly
observed author guidelines across major journals. The toolkit does not:

- Maintain per-journal rule databases
- Auto-detect the target journal from a spec
- Guarantee compliance with any specific journal's current author guidelines

Always verify against the target journal's author instructions.

## No statistical validity checking

The toolkit checks that statistical annotations are *structurally* consistent
with the figure type (e.g., flags stars on heatmaps as a suggestion).
It does not:

- Evaluate statistical test choices
- Check sample size adequacy
- Detect p-hacking or multiplicity issues

## No layout or composition analysis

The toolkit does not check:

- Axis scale choices (linear vs. log)
- Error bar types (SD, SE, 95% CI)
- Panel alignment or whitespace
- Aspect ratio

These are planned for future releases.
