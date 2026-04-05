"""figurelint_bio — pre-submission figure QA for biomedical and engineering figures."""

from .lint import lint_figure_spec
from .report import generate_markdown_report

__version__ = "0.1.0"
__all__ = [
    "lint_figure_spec",
    "generate_markdown_report",
]
