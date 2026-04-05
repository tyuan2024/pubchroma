"""Matplotlib integration for PubChroma palettes."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from .palettes import get_colors, get_palette

if TYPE_CHECKING:
    from matplotlib.colors import ListedColormap
    from matplotlib.figure import Figure


def get_cmap(
    journal: str,
    palette: str = "main",
    n: Optional[int] = None,
) -> ListedColormap:
    """Return a matplotlib ListedColormap for a journal palette.

    Parameters
    ----------
    journal : str
        Journal key (case-insensitive).
    palette : str, optional
        Palette name, by default ``"main"``.
    n : int, optional
        Number of colors. If None, uses all palette colors.

    Returns
    -------
    matplotlib.colors.ListedColormap
        A colormap suitable for ``plt.set_cmap()`` or ``ax.imshow()``.

    Raises
    ------
    ImportError
        If matplotlib is not installed.

    Examples
    --------
    >>> from pubchroma.matplotlib import get_cmap
    >>> cmap = get_cmap("nature")
    >>> cmap(0)  # RGBA tuple for first color
    (0.9019607843137255, 0.29411764705882354, 0.20784313725490197, 1.0)
    """
    try:
        from matplotlib.colors import ListedColormap as _ListedColormap
    except ImportError:
        raise ImportError(
            "matplotlib is required for this function. "
            "Install it with: pip install pubchroma[plot]"
        ) from None

    colors = get_colors(journal, palette, n=n)
    name = f"pubchroma_{journal}_{palette}"
    return _ListedColormap(colors, name=name)


def get_cycle(
    journal: str,
    palette: str = "main",
    n: Optional[int] = None,
) -> Any:
    """Return a matplotlib color cycler for a journal palette.

    Useful for setting the default color cycle on axes:
    ``ax.set_prop_cycle(get_cycle("nature"))``

    Parameters
    ----------
    journal : str
        Journal key (case-insensitive).
    palette : str, optional
        Palette name, by default ``"main"``.
    n : int, optional
        Number of colors. If None, uses all palette colors.

    Returns
    -------
    cycler.Cycler
        A color cycler for matplotlib.

    Examples
    --------
    >>> from pubchroma.matplotlib import get_cycle
    >>> import matplotlib.pyplot as plt
    >>> plt.rc("axes", prop_cycle=get_cycle("nature"))
    """
    try:
        from cycler import cycler
    except ImportError:
        raise ImportError(
            "matplotlib is required for this function. "
            "Install it with: pip install pubchroma[plot]"
        ) from None

    colors = get_colors(journal, palette, n=n)
    return cycler(color=colors)


def show_palette(
    journal: str,
    palette: str = "main",
    *,
    figsize: tuple[float, float] = (8, 1),
) -> Figure:
    """Display a visual swatch of a journal palette.

    Parameters
    ----------
    journal : str
        Journal key (case-insensitive).
    palette : str, optional
        Palette name, by default ``"main"``.
    figsize : tuple[float, float], optional
        Figure size in inches, by default ``(8, 1)``.

    Returns
    -------
    matplotlib.figure.Figure
        The figure containing the palette swatch.

    Examples
    --------
    >>> from pubchroma.matplotlib import show_palette
    >>> fig = show_palette("nature")
    """
    try:
        import matplotlib.patches as mpatches
        import matplotlib.pyplot as plt
    except ImportError:
        raise ImportError(
            "matplotlib is required for this function. "
            "Install it with: pip install pubchroma[plot]"
        ) from None

    pal = get_palette(journal, palette)
    colors = pal["colors"]
    nc = len(colors)
    label = f"{journal}/{palette}"

    fig, ax = plt.subplots(figsize=figsize)
    for i, color in enumerate(colors):
        rect = mpatches.Rectangle((i, 0), 1, 1, facecolor=color, edgecolor="white", linewidth=1)
        ax.add_patch(rect)

    ax.set_xlim(0, nc)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(
        f"{label}  ({nc} colors"
        f"{', colorblind-safe' if pal['colorblind_safe'] else ''})",
        fontsize=10,
        loc="left",
    )

    for spine in ax.spines.values():
        spine.set_visible(False)

    fig.tight_layout()
    return fig


def show_all(
    *,
    figsize: tuple[float, float] = (10, 8),
) -> Figure:
    """Display all available palettes in a single figure.

    Parameters
    ----------
    figsize : tuple[float, float], optional
        Figure size in inches, by default ``(10, 8)``.

    Returns
    -------
    matplotlib.figure.Figure
        The figure containing all palette swatches.
    """
    try:
        import matplotlib.patches as mpatches
        import matplotlib.pyplot as plt
    except ImportError:
        raise ImportError(
            "matplotlib is required for this function. "
            "Install it with: pip install pubchroma[plot]"
        ) from None

    from .palettes import list_journals, list_palettes

    entries: list[tuple[str, list[str], bool]] = []
    for j in list_journals():
        for p in list_palettes(j):
            pal = get_palette(j, p)
            entries.append((f"{j}/{p}", pal["colors"], pal["colorblind_safe"]))

    n_rows = len(entries)
    max_colors = max(len(e[1]) for e in entries)

    fig, axes = plt.subplots(n_rows, 1, figsize=figsize)
    if n_rows == 1:
        axes = [axes]

    for ax, (label, colors, cb_safe) in zip(axes, entries):
        for i, color in enumerate(colors):
            rect = mpatches.Rectangle(
                (i, 0), 1, 1, facecolor=color, edgecolor="white", linewidth=1,
            )
            ax.add_patch(rect)
        ax.set_xlim(0, max_colors)
        ax.set_ylim(0, 1)
        ax.set_xticks([])
        ax.set_yticks([])
        suffix = " (CB)" if cb_safe else ""
        ax.set_ylabel(f"{label}{suffix}", rotation=0, ha="right", va="center", fontsize=8)
        for spine in ax.spines.values():
            spine.set_visible(False)

    fig.suptitle("PubChroma — All Palettes", fontsize=12, fontweight="bold")
    fig.tight_layout()
    return fig
