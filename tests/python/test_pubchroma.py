"""Tests for pubchroma Python package."""

import pytest
import sys
import os

# Allow running tests before install
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../src"))

import pubchroma as pc


# ---------------------------------------------------------------------------
# list_journals
# ---------------------------------------------------------------------------
class TestListJournals:
    def test_returns_list(self):
        result = pc.list_journals()
        assert isinstance(result, list)

    def test_contains_known_journals(self):
        result = pc.list_journals()
        for journal in ["nature", "science", "cell", "nejm", "lancet", "jama", "pnas", "bmj"]:
            assert journal in result

    def test_is_sorted(self):
        result = pc.list_journals()
        assert result == sorted(result)

    def test_returns_new_list_each_call(self):
        a = pc.list_journals()
        b = pc.list_journals()
        assert a == b
        assert a is not b


# ---------------------------------------------------------------------------
# list_palettes
# ---------------------------------------------------------------------------
class TestListPalettes:
    def test_nature_has_main(self):
        result = pc.list_palettes("nature")
        assert "main" in result

    def test_case_insensitive(self):
        assert pc.list_palettes("Nature") == pc.list_palettes("nature")
        assert pc.list_palettes("NATURE") == pc.list_palettes("nature")

    def test_unknown_journal_raises(self):
        with pytest.raises(ValueError, match="not found"):
            pc.list_palettes("nonexistent_journal")

    @pytest.mark.parametrize("journal", pc.list_journals())
    def test_every_journal_has_main(self, journal):
        palettes = pc.list_palettes(journal)
        assert isinstance(palettes, list)
        assert len(palettes) > 0


# ---------------------------------------------------------------------------
# get_palette
# ---------------------------------------------------------------------------
class TestGetPalette:
    def test_nature_main_has_colors(self):
        p = pc.get_palette("nature")
        assert "colors" in p
        assert len(p["colors"]) > 0

    def test_colors_are_hex(self):
        p = pc.get_palette("nature")
        for c in p["colors"]:
            assert c.startswith("#")
            assert len(c) == 7

    def test_has_colorblind_safe_field(self):
        p = pc.get_palette("nature")
        assert "colorblind_safe" in p
        assert isinstance(p["colorblind_safe"], bool)

    def test_has_description(self):
        p = pc.get_palette("nature")
        assert "description" in p
        assert isinstance(p["description"], str)
        assert len(p["description"]) > 0

    def test_has_type(self):
        p = pc.get_palette("nature")
        assert "type" in p

    def test_unknown_palette_raises(self):
        with pytest.raises(ValueError, match="not found"):
            pc.get_palette("nature", "nonexistent")

    def test_unknown_journal_raises(self):
        with pytest.raises(ValueError, match="not found"):
            pc.get_palette("nonexistent")

    @pytest.mark.parametrize("journal", pc.list_journals())
    def test_all_journals_valid_hex(self, journal):
        """Every color in every palette must be a valid 7-char hex string."""
        for pal_name in pc.list_palettes(journal):
            pal = pc.get_palette(journal, pal_name)
            for color in pal["colors"]:
                assert color.startswith("#"), f"{journal}/{pal_name}: {color}"
                assert len(color) == 7, f"{journal}/{pal_name}: {color}"
                # Validate hex chars
                int(color[1:], 16)


# ---------------------------------------------------------------------------
# get_colors
# ---------------------------------------------------------------------------
class TestGetColors:
    def test_returns_list_of_strings(self):
        colors = pc.get_colors("nature")
        assert isinstance(colors, list)
        assert all(isinstance(c, str) for c in colors)

    def test_n_limits_colors(self):
        colors = pc.get_colors("nature", n=3)
        assert len(colors) == 3

    def test_n_cycles_when_exceeds(self):
        # nature/main has 10 colors; request 12
        colors = pc.get_colors("nature", n=12)
        assert len(colors) == 12

    def test_n_equals_palette_length(self):
        all_colors = pc.get_colors("nature")
        colors = pc.get_colors("nature", n=len(all_colors))
        assert colors == all_colors

    def test_n_one(self):
        colors = pc.get_colors("nature", n=1)
        assert len(colors) == 1

    def test_n_zero_raises(self):
        with pytest.raises(ValueError, match="positive"):
            pc.get_colors("nature", n=0)

    def test_n_negative_raises(self):
        with pytest.raises(ValueError, match="positive"):
            pc.get_colors("nature", n=-1)

    def test_colorblind_only_safe_palette_ok(self):
        colors = pc.get_colors("colorblind", "okabe_ito", colorblind_only=True)
        assert len(colors) > 0

    def test_colorblind_only_unsafe_palette_raises(self):
        with pytest.raises(ValueError, match="not colorblind-safe"):
            pc.get_colors("science", colorblind_only=True)

    def test_returns_copy_not_reference(self):
        """Ensure returned list is a new copy (immutability)."""
        a = pc.get_colors("nature")
        b = pc.get_colors("nature")
        assert a == b
        assert a is not b


# ---------------------------------------------------------------------------
# Colorblind checks
# ---------------------------------------------------------------------------
class TestColorblindCheck:
    def test_nature_main_is_safe(self):
        assert pc.is_colorblind_safe("nature") is True

    def test_science_main_is_not_safe(self):
        assert pc.is_colorblind_safe("science") is False

    def test_list_colorblind_safe_returns_list(self):
        result = pc.list_colorblind_safe()
        assert isinstance(result, list)
        assert len(result) > 0
        for item in result:
            assert "journal" in item
            assert "palette" in item
            assert "n_colors" in item

    def test_list_colorblind_safe_all_are_safe(self):
        """Every entry returned should actually be colorblind-safe."""
        for item in pc.list_colorblind_safe():
            assert pc.is_colorblind_safe(item["journal"], item["palette"]) is True


# ---------------------------------------------------------------------------
# Matplotlib integration
# ---------------------------------------------------------------------------
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

        cmap = get_cmap("nature", n=5)
        assert cmap.N == 5

    def test_get_cycle_returns_cycler(self):
        from pubchroma.matplotlib import get_cycle

        cycle = get_cycle("nature")
        colors = [d["color"] for d in cycle]
        assert len(colors) == 10

    def test_show_palette_returns_figure(self):
        import matplotlib
        matplotlib.use("Agg")
        from pubchroma.matplotlib import show_palette
        import matplotlib.pyplot as plt

        fig = show_palette("nature")
        assert fig is not None
        plt.close(fig)

    def test_show_all_returns_figure(self):
        import matplotlib
        matplotlib.use("Agg")
        from pubchroma.matplotlib import show_all
        import matplotlib.pyplot as plt

        fig = show_all()
        assert fig is not None
        plt.close(fig)


# ---------------------------------------------------------------------------
# Version
# ---------------------------------------------------------------------------
class TestVersion:
    def test_version_string(self):
        assert isinstance(pc.__version__, str)
        parts = pc.__version__.split(".")
        assert len(parts) == 3
