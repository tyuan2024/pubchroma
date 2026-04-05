"""Tests for pubchroma — palette lookup, recommend, validate, and figurelint_bio."""

import os
import sys

import pytest

# Allow running tests before install
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../src"))

import pubchroma as pc


# ── Helper: minimal valid spec ─────────────────────────────────────────────

def _minimal_spec(**overrides):
    base = {
        "field": "clinical",
        "figure_type": "box",
        "variable_type": "categorical",
    }
    base.update(overrides)
    return base


# ═══════════════════════════════════════════════════════════════════════════════
# pubchroma core (palette lookup)
# ═══════════════════════════════════════════════════════════════════════════════

class TestListJournals:
    def test_returns_list(self):
        assert isinstance(pc.list_journals(), list)

    def test_contains_known_journals(self):
        result = pc.list_journals()
        for journal in ["nature", "science", "cell", "nejm", "lancet", "jama", "pnas", "bmj"]:
            assert journal in result

    def test_is_sorted(self):
        result = pc.list_journals()
        assert result == sorted(result)

    def test_returns_new_list_each_call(self):
        a, b = pc.list_journals(), pc.list_journals()
        assert a == b
        assert a is not b


class TestListPalettes:
    def test_nature_has_main(self):
        assert "main" in pc.list_palettes("nature")

    def test_case_insensitive(self):
        assert pc.list_palettes("Nature") == pc.list_palettes("nature")
        assert pc.list_palettes("NATURE") == pc.list_palettes("nature")

    def test_unknown_journal_raises(self):
        with pytest.raises(ValueError, match="not found"):
            pc.list_palettes("nonexistent_journal")

    @pytest.mark.parametrize("journal", pc.list_journals())
    def test_every_journal_has_palettes(self, journal):
        palettes = pc.list_palettes(journal)
        assert isinstance(palettes, list)
        assert len(palettes) > 0


class TestGetPalette:
    def test_nature_main_structure(self):
        p = pc.get_palette("nature")
        assert "colors" in p
        assert len(p["colors"]) > 0
        assert "colorblind_safe" in p
        assert isinstance(p["colorblind_safe"], bool)
        assert "description" in p
        assert "type" in p

    def test_colors_are_valid_hex(self):
        p = pc.get_palette("nature")
        for c in p["colors"]:
            assert c.startswith("#") and len(c) == 7
            int(c[1:], 16)  # valid hex chars

    def test_unknown_journal_raises(self):
        with pytest.raises(ValueError, match="not found"):
            pc.get_palette("nonexistent")

    def test_unknown_palette_raises(self):
        with pytest.raises(ValueError, match="not found"):
            pc.get_palette("nature", "nonexistent")

    @pytest.mark.parametrize("journal", pc.list_journals())
    def test_all_journals_valid_hex(self, journal):
        for pal_name in pc.list_palettes(journal):
            pal = pc.get_palette(journal, pal_name)
            for color in pal["colors"]:
                assert color.startswith("#") and len(color) == 7, (
                    f"{journal}/{pal_name}: {color}"
                )
                int(color[1:], 16)


class TestGetColors:
    def test_returns_list_of_strings(self):
        colors = pc.get_colors("nature")
        assert isinstance(colors, list)
        assert all(isinstance(c, str) for c in colors)

    def test_n_limits_colors(self):
        assert len(pc.get_colors("nature", n=3)) == 3

    def test_n_cycles_when_exceeds(self):
        assert len(pc.get_colors("nature", n=12)) == 12

    def test_n_one(self):
        assert len(pc.get_colors("nature", n=1)) == 1

    def test_n_zero_raises(self):
        with pytest.raises(ValueError, match="positive"):
            pc.get_colors("nature", n=0)

    def test_n_negative_raises(self):
        with pytest.raises(ValueError, match="positive"):
            pc.get_colors("nature", n=-1)

    def test_colorblind_only_safe_ok(self):
        assert len(pc.get_colors("colorblind", "okabe_ito", colorblind_only=True)) > 0

    def test_colorblind_only_unsafe_raises(self):
        with pytest.raises(ValueError, match="not colorblind-safe"):
            pc.get_colors("science", colorblind_only=True)

    def test_returns_copy(self):
        a, b = pc.get_colors("nature"), pc.get_colors("nature")
        assert a == b and a is not b


class TestColorblindCheck:
    def test_nature_main_is_safe(self):
        assert pc.is_colorblind_safe("nature") is True

    def test_science_main_is_not_safe(self):
        assert pc.is_colorblind_safe("science") is False

    def test_list_colorblind_safe_structure(self):
        result = pc.list_colorblind_safe()
        assert isinstance(result, list) and len(result) > 0
        for item in result:
            for key in ("journal", "palette", "n_colors"):
                assert key in item

    def test_list_colorblind_safe_all_verified(self):
        for item in pc.list_colorblind_safe():
            assert pc.is_colorblind_safe(item["journal"], item["palette"]) is True


# ═══════════════════════════════════════════════════════════════════════════════
# pubchroma.recommend
# ═══════════════════════════════════════════════════════════════════════════════

class TestRecommendPalette:
    @pytest.fixture(autouse=True)
    def _skip_if_no_yaml(self):
        pytest.importorskip("yaml")

    def test_returns_expected_keys(self):
        from pubchroma.recommend import recommend_palette
        result = recommend_palette("clinical", "box")
        for key in ("palette_id", "hex", "n_max", "variable_type",
                    "journal_family", "colorblind_safe", "rationale"):
            assert key in result

    def test_hex_are_valid(self):
        from pubchroma.recommend import recommend_palette
        result = recommend_palette("clinical", "box")
        for c in result["hex"]:
            assert c.startswith("#") and len(c) == 7

    def test_colorblind_safe_filter(self):
        from pubchroma.recommend import recommend_palette
        result = recommend_palette("clinical", "box", colorblind_safe=True)
        assert result["colorblind_safe"] is True

    def test_n_groups_respected(self):
        from pubchroma.recommend import recommend_palette
        result = recommend_palette("clinical", "box", n_groups=3)
        assert len(result["hex"]) <= result["n_max"]

    def test_invalid_field_raises(self):
        from pubchroma.recommend import recommend_palette
        with pytest.raises(ValueError, match="field must be"):
            recommend_palette("astrology", "bar")

    def test_invalid_figure_type_raises(self):
        from pubchroma.recommend import recommend_palette
        with pytest.raises(ValueError, match="figure_type must be"):
            recommend_palette("clinical", "pie_chart")

    @pytest.mark.parametrize("field,figure_type", [
        ("clinical", "box"),
        ("omics", "heatmap"),
        ("singlecell", "umap"),
        ("engineering", "line"),
    ])
    def test_common_combinations(self, field, figure_type):
        from pubchroma.recommend import recommend_palette
        result = recommend_palette(field, figure_type)
        assert result["palette_id"]
        assert len(result["hex"]) > 0


# ═══════════════════════════════════════════════════════════════════════════════
# pubchroma.validate
# ═══════════════════════════════════════════════════════════════════════════════

class TestValidatePalette:
    @pytest.fixture(autouse=True)
    def _skip_if_no_yaml(self):
        pytest.importorskip("yaml")

    def test_known_palette_valid(self):
        from pubchroma.validate import validate_palette
        result = validate_palette("clinical_categorical_conservative_4")
        assert result["valid"] is True
        assert result["errors"] == []

    def test_unknown_palette_invalid(self):
        from pubchroma.validate import validate_palette
        result = validate_palette("nonexistent_palette_xyz")
        assert result["valid"] is False
        assert any("not in the registry" in e for e in result["errors"])

    def test_colorblind_claim_mismatch_raises_error(self):
        from pubchroma.validate import validate_palette
        # singlecell_categorical_balanced_12 is NOT colorblind-safe
        result = validate_palette(
            "singlecell_categorical_balanced_12",
            colorblind_safe=True,
        )
        assert result["valid"] is False
        assert any("colorblind" in e.lower() for e in result["errors"])

    def test_n_groups_over_capacity(self):
        from pubchroma.validate import validate_palette
        result = validate_palette(
            "clinical_categorical_conservative_4",
            n_groups=10,
        )
        assert result["valid"] is False

    def test_field_mismatch_warning(self):
        from pubchroma.validate import validate_palette
        result = validate_palette(
            "engineering_categorical_contrast_6",
            field="clinical",
        )
        assert len(result["warnings"]) > 0

    def test_no_args_raises(self):
        from pubchroma.validate import validate_palette
        with pytest.raises(ValueError):
            validate_palette()


# ═══════════════════════════════════════════════════════════════════════════════
# figurelint_bio
# ═══════════════════════════════════════════════════════════════════════════════

class TestFigureLintSpec:
    @pytest.fixture(autouse=True)
    def _skip_if_no_yaml(self):
        pytest.importorskip("yaml")

    def test_clean_spec_passes(self):
        from figurelint_bio import lint_figure_spec
        spec = _minimal_spec(
            palette_name="clinical_categorical_conservative_4",
            font_size_pt=8,
            dpi=600,
            width_mm=89,
            colorblind_safe=True,
        )
        report = lint_figure_spec(spec)
        assert report["errors"] == []
        assert report["score"] == 100

    def test_missing_required_field_raises(self):
        from figurelint_bio import lint_figure_spec
        with pytest.raises(ValueError, match="schema validation"):
            lint_figure_spec({"field": "clinical", "figure_type": "box"})

    def test_rainbow_palette_triggers_error(self):
        from figurelint_bio import lint_figure_spec
        spec = _minimal_spec(palette_name="jet")
        report = lint_figure_spec(spec)
        assert any(i["rule"] == "rainbow_palette_detected" for i in report["errors"])

    def test_low_dpi_triggers_error(self):
        from figurelint_bio import lint_figure_spec
        spec = _minimal_spec(dpi=72)
        report = lint_figure_spec(spec)
        assert any(i["rule"] == "dpi_below_minimum" for i in report["errors"])

    def test_small_font_triggers_error(self):
        from figurelint_bio import lint_figure_spec
        spec = _minimal_spec(font_size_pt=4)
        report = lint_figure_spec(spec)
        assert any(i["rule"] == "font_size_too_small" for i in report["errors"])

    def test_diverging_no_midpoint_triggers_warning(self):
        from figurelint_bio import lint_figure_spec
        spec = _minimal_spec(variable_type="diverging")
        report = lint_figure_spec(spec)
        assert any(i["rule"] == "diverging_no_explicit_midpoint" for i in report["warnings"])

    def test_diverging_with_midpoint_no_warning(self):
        from figurelint_bio import lint_figure_spec
        spec = _minimal_spec(variable_type="diverging", notes="midpoint=0 for logFC")
        report = lint_figure_spec(spec)
        assert not any(
            i["rule"] == "diverging_no_explicit_midpoint" for i in report["warnings"]
        )

    def test_too_many_legend_items_warning(self):
        from figurelint_bio import lint_figure_spec
        spec = _minimal_spec(legend_items=15)
        report = lint_figure_spec(spec)
        assert any(i["rule"] == "legend_too_many_items" for i in report["warnings"])

    def test_score_decreases_with_issues(self):
        from figurelint_bio import lint_figure_spec
        clean = lint_figure_spec(_minimal_spec())
        bad = lint_figure_spec(_minimal_spec(palette_name="jet", dpi=72, font_size_pt=3))
        assert bad["score"] < clean["score"]

    def test_colorblind_safe_claim_mismatch(self):
        from figurelint_bio import lint_figure_spec
        spec = _minimal_spec(
            palette_name="singlecell_categorical_balanced_12",
            colorblind_safe=True,
        )
        report = lint_figure_spec(spec)
        assert any(
            i["rule"] == "colorblind_safe_claimed_but_palette_unsafe"
            for i in report["errors"]
        )

    def test_report_summary_present(self):
        from figurelint_bio import lint_figure_spec
        report = lint_figure_spec(_minimal_spec())
        assert isinstance(report["summary"], str)
        assert len(report["summary"]) > 0


class TestGenerateMarkdownReport:
    @pytest.fixture(autouse=True)
    def _skip_if_no_yaml(self):
        pytest.importorskip("yaml")

    def test_clean_report_markdown(self):
        from figurelint_bio import lint_figure_spec, generate_markdown_report
        report = lint_figure_spec(_minimal_spec())
        md = generate_markdown_report(report)
        assert "# FigureLint-Bio Report" in md
        assert "Score" in md

    def test_error_report_markdown(self):
        from figurelint_bio import lint_figure_spec, generate_markdown_report
        report = lint_figure_spec(_minimal_spec(palette_name="jet"))
        md = generate_markdown_report(report)
        assert "ERROR" in md
        assert "rainbow" in md.lower()


# ═══════════════════════════════════════════════════════════════════════════════
# Matplotlib integration
# ═══════════════════════════════════════════════════════════════════════════════

class TestMatplotlib:
    @pytest.fixture(autouse=True)
    def _check_matplotlib(self):
        pytest.importorskip("matplotlib")

    def test_get_cmap_returns_colormap(self):
        from pubchroma.matplotlib import get_cmap
        cmap = get_cmap("nature")
        assert cmap.name == "pubchroma_nature_main"
        assert cmap.N == 10

    def test_get_cmap_with_n(self):
        from pubchroma.matplotlib import get_cmap
        assert get_cmap("nature", n=5).N == 5

    def test_get_cycle_returns_cycler(self):
        from pubchroma.matplotlib import get_cycle
        cycle = get_cycle("nature")
        assert len([d["color"] for d in cycle]) == 10

    def test_show_palette_returns_figure(self):
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from pubchroma.matplotlib import show_palette
        fig = show_palette("nature")
        assert fig is not None
        plt.close(fig)

    def test_show_all_returns_figure(self):
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from pubchroma.matplotlib import show_all
        fig = show_all()
        assert fig is not None
        plt.close(fig)


# ═══════════════════════════════════════════════════════════════════════════════
# Version
# ═══════════════════════════════════════════════════════════════════════════════

class TestVersion:
    def test_pubchroma_version(self):
        assert isinstance(pc.__version__, str)
        assert len(pc.__version__.split(".")) == 3

    def test_figurelint_bio_version(self):
        pytest.importorskip("yaml")
        import figurelint_bio
        assert isinstance(figurelint_bio.__version__, str)
