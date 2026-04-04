"""Tests for pubchroma Python package."""

import pytest
import sys
import os

# Allow running tests before install
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../src"))

import pubchroma as pc


class TestListJournals:
    def test_returns_list(self):
        result = pc.list_journals()
        assert isinstance(result, list)

    def test_contains_known_journals(self):
        result = pc.list_journals()
        for journal in ["nature", "science", "cell", "nejm", "lancet"]:
            assert journal in result

    def test_is_sorted(self):
        result = pc.list_journals()
        assert result == sorted(result)


class TestListPalettes:
    def test_nature_has_main(self):
        result = pc.list_palettes("nature")
        assert "main" in result

    def test_case_insensitive(self):
        assert pc.list_palettes("Nature") == pc.list_palettes("nature")

    def test_unknown_journal_raises(self):
        with pytest.raises(ValueError, match="not found"):
            pc.list_palettes("nonexistent_journal")


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

    def test_unknown_palette_raises(self):
        with pytest.raises(ValueError, match="not found"):
            pc.get_palette("nature", "nonexistent")

    def test_unknown_journal_raises(self):
        with pytest.raises(ValueError, match="not found"):
            pc.get_palette("nonexistent")


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

    def test_colorblind_only_safe_palette_ok(self):
        colors = pc.get_colors("colorblind", "okabe_ito", colorblind_only=True)
        assert len(colors) > 0

    def test_colorblind_only_unsafe_palette_raises(self):
        with pytest.raises(ValueError, match="not colorblind-safe"):
            pc.get_colors("science", colorblind_only=True)


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
