"""
FigureLint-Bio counter-example: deliberately bad figure spec.

Shows how lint catches common mistakes before submission.
"""

import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../src"))

from figurelint_bio import lint_figure_spec, generate_markdown_report

spec_path = os.path.join(
    os.path.dirname(__file__), "../specs/counterexample_bad_spec.json"
)
with open(spec_path) as fh:
    spec = json.load(fh)
    # Remove the _note field (not a valid spec field)
    spec.pop("_note", None)

report = lint_figure_spec(spec)

print(generate_markdown_report(report))
print(f"\nScore: {report['score']}/100")
print(f"Errors:      {len(report['errors'])}")
print(f"Warnings:    {len(report['warnings'])}")
print(f"Suggestions: {len(report['suggestions'])}")
