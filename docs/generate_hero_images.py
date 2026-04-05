"""
Generate all README hero images for PubChroma + FigureLint-Bio.

Run from repo root:
  python docs/generate_hero_images.py
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.gridspec import GridSpec
from matplotlib.patches import FancyBboxPatch, Wedge

OUT = os.path.dirname(__file__)

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.spines.left": False,
    "axes.spines.bottom": False,
})

BG    = "#0f1117"
CARD  = "#1a1d27"
TEXT  = "#e8eaf0"
MUTED = "#8b8fa8"
ACCENT = "#4f8ef7"

FIELD_COLORS = {
    "clinical":    "#4f8ef7",
    "omics":       "#a78bfa",
    "singlecell":  "#34d399",
    "engineering": "#fb923c",
    "mechanism":   "#f472b6",
    "universal":   "#94a3b8",
}


# ═══════════════════════════════════════════════════════════════════════════════
# 1. PALETTE BANNER
# ═══════════════════════════════════════════════════════════════════════════════

def make_palette_banner():
    palettes = [
        ("Clinical Conservative 4",  ["#374E55","#DF8F44","#00A1D5","#B24745"],                                                  "clinical",    True),
        ("Clinical Conservative 6",  ["#374E55","#DF8F44","#00A1D5","#B24745","#79AF97","#6A6599"],                              "clinical",    True),
        ("Omics Diverging",           ["#3C5488","#FFFFFF","#E64B35"],                                                            "omics",       True),
        ("Omics Sequential",          ["#F7FBFF","#C6DBEF","#9ECAE1","#6BAED6","#3182BD","#08519C","#08306B"],                   "omics",       True),
        ("Single-cell 12-color",      ["#E64B35","#4DBBD5","#00A087","#3C5488","#F39B7F","#8491B4",
                                       "#91D1C2","#DC0000","#7E6148","#B09C85","#4DB8FF","#FFDB6D"],                              "singlecell",  False),
        ("Engineering Sequential",    ["#FFF7FB","#ECE2F0","#D0D1E6","#A6BDDB","#67A9CF","#1C9099","#016C59"],                   "engineering", True),
        ("Engineering Categorical",   ["#3B4992","#EE0000","#008B45","#631879","#008280","#BB0021"],                              "engineering", False),
        ("Mechanism Highlight",       ["#E64B35","#3C5488","#AAAAAA","#DDDDDD"],                                                  "mechanism",   True),
        ("Okabe-Ito Universal",       ["#E69F00","#56B4E9","#009E73","#F0E442","#0072B2","#D55E00","#CC79A7","#000000"],          "universal",   True),
    ]

    # Layout constants (all in data-space = inches since figsize drives it)
    FIG_W   = 15.0
    ROW_H   = 0.72   # vertical space per row
    PAD_TOP = 1.0    # space above first row (title block)
    PAD_BOT = 0.55   # space below last row (footer)
    n_rows  = len(palettes)
    FIG_H   = n_rows * ROW_H + PAD_TOP + PAD_BOT

    # Column positions
    TAG_X    = 0.18   # left edge of field tag box
    TAG_W    = 0.78   # tag box width (wide enough for "engineering")
    TAG_MID  = TAG_X + TAG_W / 2
    NAME_X   = TAG_X + TAG_W + 0.18   # left edge of palette name text
    SWATCH_X = 4.0    # left edge of first swatch
    SWATCH_W = 0.50
    SWATCH_H = 0.38
    SWATCH_G = 0.08   # gap between swatches
    MAX_SWATCHES = 12  # single-cell has 12
    BADGE_X  = SWATCH_X + MAX_SWATCHES * (SWATCH_W + SWATCH_G) + 0.20

    fig = plt.figure(figsize=(FIG_W, FIG_H), facecolor=BG)
    ax  = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(BG)
    ax.set_xlim(0, FIG_W)
    ax.set_ylim(0, FIG_H)
    ax.axis("off")

    # ── Title block ───────────────────────────────────────────────────────────
    title_y = FIG_H - 0.38
    sub_y   = FIG_H - 0.72
    ax.text(FIG_W / 2, title_y,
            "PubChroma  ·  Journal-Inspired Colour Palettes",
            ha="center", va="center", fontsize=17, fontweight="bold", color=TEXT)
    ax.text(FIG_W / 2, sub_y,
            "field-aware  ·  figure-aware  ·  accessibility-aware",
            ha="center", va="center", fontsize=9.5, color=MUTED)

    # ── Rows ─────────────────────────────────────────────────────────────────
    for i, (name, colors, field, cb) in enumerate(palettes):
        # vertical centre of this row
        cy = FIG_H - PAD_TOP - (i + 0.55) * ROW_H

        fc = FIELD_COLORS.get(field, MUTED)

        # Field tag pill
        tag_h = 0.28
        tag = FancyBboxPatch((TAG_X, cy - tag_h / 2), TAG_W, tag_h,
                             boxstyle="round,pad=0.05",
                             facecolor=fc + "2a", edgecolor=fc, linewidth=0.9)
        ax.add_patch(tag)
        ax.text(TAG_MID, cy, field,
                ha="center", va="center", fontsize=6.0, color=fc, fontweight="bold")

        # Palette name (single-line, no \n)
        ax.text(NAME_X, cy, name,
                ha="left", va="center", fontsize=8.5, color=TEXT)

        # Swatches
        light = {"#FFFFFF","#F7FBFF","#FFF7FB","#F0E442","#DDDDDD","#ECE2F0"}
        for j, color in enumerate(colors):
            sx = SWATCH_X + j * (SWATCH_W + SWATCH_G)
            edge = "#666677" if color.upper() in light else "none"
            rect = FancyBboxPatch((sx, cy - SWATCH_H / 2), SWATCH_W, SWATCH_H,
                                  boxstyle="round,pad=0.03",
                                  facecolor=color, edgecolor=edge, linewidth=0.5)
            ax.add_patch(rect)

        # CB-safe badge
        if cb:
            ax.text(BADGE_X, cy, "✓ CB-safe",
                    ha="left", va="center", fontsize=7.5,
                    color="#34d399", fontweight="bold")

    # ── Separator line ────────────────────────────────────────────────────────
    sep_y = PAD_BOT - 0.05
    ax.axhline(sep_y, xmin=0.02, xmax=0.98, color="#2a2d3e", linewidth=0.6)

    # ── Footer ────────────────────────────────────────────────────────────────
    ax.text(FIG_W / 2, PAD_BOT / 2,
            "pip install pubchroma[recommend]   ·   github.com/tyuan2024/pubchroma",
            ha="center", va="center", fontsize=8.5, color=MUTED, family="monospace")

    fig.savefig(os.path.join(OUT, "banner_palettes.png"),
                dpi=180, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("✓ banner_palettes.png")


# ═══════════════════════════════════════════════════════════════════════════════
# 2. SCIENTIFIC FIGURE EXAMPLES
# ═══════════════════════════════════════════════════════════════════════════════

def make_science_examples():
    rng = np.random.default_rng(42)

    fig = plt.figure(figsize=(18, 11), facecolor=BG)
    fig.patch.set_facecolor(BG)

    gs = GridSpec(2, 4, figure=fig,
                  hspace=0.52, wspace=0.40,
                  left=0.05, right=0.97, top=0.87, bottom=0.07)

    def style_ax(ax, title, subtitle=""):
        ax.set_facecolor(CARD)
        for sp in ax.spines.values():
            sp.set_color("#2a2d3e")
            sp.set_linewidth(0.8)
        ax.tick_params(colors=MUTED, labelsize=7)
        ax.xaxis.label.set_color(MUTED)
        ax.yaxis.label.set_color(MUTED)
        # Title slightly above the axes
        ax.set_title(title, color=TEXT, fontsize=9.5, fontweight="bold", pad=4)
        if subtitle:
            # Place subtitle *above* the title using figure-space annotation
            ax.text(0.5, 1.075, subtitle,
                    transform=ax.transAxes,
                    ha="center", va="bottom", fontsize=6.5, color=MUTED)

    # ── Panel A: Clinical boxplot ─────────────────────────────────────────────
    ax_a = fig.add_subplot(gs[0, 0])
    palette_clin = ["#374E55", "#DF8F44", "#00A1D5", "#B24745"]
    arms = ["Placebo", "Low", "Mid", "High"]
    data_clin = [rng.normal(loc, 0.7, 28) for loc in [0, 0.6, 1.1, 1.7]]
    bp = ax_a.boxplot(data_clin, patch_artist=True,
                      widths=0.52,
                      medianprops=dict(color="white", linewidth=1.5),
                      whiskerprops=dict(color=MUTED),
                      capprops=dict(color=MUTED),
                      flierprops=dict(marker="o", markerfacecolor=MUTED,
                                     markersize=2.5, alpha=0.5, linestyle="none"))
    for patch, c in zip(bp["boxes"], palette_clin):
        patch.set_facecolor(c)
        patch.set_alpha(0.88)
    ax_a.set_xticklabels(arms, fontsize=7)
    ax_a.set_ylabel("Biomarker (AU)", fontsize=7.5)
    ax_a.axhline(0, color=MUTED, linewidth=0.4, linestyle="--", alpha=0.4)
    style_ax(ax_a, "A  Clinical Boxplot", "clinical · medical_conservative")

    # Significance bracket — positioned safely above data
    y_max = max(max(d) for d in data_clin) + 0.25
    y_br  = y_max + 0.15
    ax_a.annotate("", xy=(4, y_br), xytext=(1, y_br),
                  arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
    ax_a.text(2.5, y_br + 0.10, "p = 0.003",
              ha="center", fontsize=6.5, color=TEXT, va="bottom")

    # ── Panel B: Omics heatmap ────────────────────────────────────────────────
    ax_b = fig.add_subplot(gs[0, 1])
    cmap_div = LinearSegmentedColormap.from_list(
        "div", ["#3C5488", "#FFFFFF", "#E64B35"])
    heat_data = rng.normal(0, 1.5, (18, 12))
    im = ax_b.imshow(heat_data, cmap=cmap_div, vmin=-3, vmax=3, aspect="auto")
    ax_b.set_xticks([])
    ax_b.set_yticks([])
    cb = fig.colorbar(im, ax=ax_b, fraction=0.046, pad=0.04)
    cb.ax.tick_params(labelsize=6, colors=MUTED)
    cb.ax.set_ylabel("z-score", fontsize=6, color=MUTED)
    cb.outline.set_edgecolor("#2a2d3e")
    style_ax(ax_b, "B  Omics Heatmap", "omics · diverging · cns_inspired")

    # ── Panel C: Single-cell UMAP ─────────────────────────────────────────────
    ax_c = fig.add_subplot(gs[0, 2:4])
    palette_sc = [
        "#E64B35","#4DBBD5","#00A087","#3C5488","#F39B7F",
        "#8491B4","#91D1C2","#DC0000","#7E6148","#B09C85",
        "#4DB8FF","#FFDB6D",
    ]
    n_cells, n_types = 1800, 12
    angles = np.linspace(0, 2 * np.pi, n_types, endpoint=False)
    radii  = [2.8, 2.2, 3.1, 2.5, 3.4, 2.0, 2.9, 3.2, 1.8, 2.6, 3.0, 2.4]
    x_all, y_all, c_all = [], [], []
    per_type = n_cells // n_types
    for k in range(n_types):
        cx   = radii[k] * np.cos(angles[k]) + rng.normal(0, 0.2)
        cy_k = radii[k] * np.sin(angles[k]) + rng.normal(0, 0.2)
        sp   = rng.uniform(0.35, 0.75)
        x_all.extend(rng.normal(cx,   sp, per_type))
        y_all.extend(rng.normal(cy_k, sp, per_type))
        c_all.extend([palette_sc[k]] * per_type)
    idx   = rng.permutation(len(x_all))
    x_all = np.array(x_all)[idx]
    y_all = np.array(y_all)[idx]
    c_all = np.array(c_all)[idx]

    ax_c.scatter(x_all, y_all, c=c_all, s=3.5, alpha=0.72, linewidths=0)

    cell_types = [f"Type {i+1}" for i in range(n_types)]
    handles = [mpatches.Patch(color=c, label=l)
               for c, l in zip(palette_sc, cell_types)]
    ax_c.legend(handles=handles, ncol=6, fontsize=6.5,
                frameon=True, framealpha=0.30,
                facecolor=CARD, edgecolor="#2a2d3e",
                labelcolor=TEXT, loc="lower center",
                bbox_to_anchor=(0.5, -0.02),
                markerscale=1.4, handlelength=1.0,
                columnspacing=0.6, handletextpad=0.4)
    ax_c.set_xticks([])
    ax_c.set_yticks([])
    ax_c.set_xlabel("UMAP 1", fontsize=7.5)
    ax_c.set_ylabel("UMAP 2", fontsize=7.5)
    style_ax(ax_c, "C  Single-Cell UMAP", "singlecell · categorical · 12 cell types")

    # ── Panel D: Volcano plot ──────────────────────────────────────────────────
    ax_d = fig.add_subplot(gs[1, 0:2])
    n_genes  = 600
    log2fc   = rng.normal(0, 1.2, n_genes)
    pvals    = np.abs(rng.normal(0, 1, n_genes))
    nlp      = pvals * rng.uniform(0.5, 4, n_genes)

    sig_up  = (log2fc >  1) & (nlp > 1.3)
    sig_dn  = (log2fc < -1) & (nlp > 1.3)
    nonsig  = ~(sig_up | sig_dn)

    ax_d.scatter(log2fc[nonsig], nlp[nonsig],
                 s=5, c="#6b7280", alpha=0.40, linewidths=0, label="NS")
    ax_d.scatter(log2fc[sig_up], nlp[sig_up],
                 s=9, c="#E64B35", alpha=0.82, linewidths=0, label=f"Up ({sig_up.sum()})")
    ax_d.scatter(log2fc[sig_dn], nlp[sig_dn],
                 s=9, c="#3C5488", alpha=0.82, linewidths=0, label=f"Down ({sig_dn.sum()})")

    ax_d.axhline(1.3, color=MUTED, linewidth=0.7, linestyle="--", alpha=0.5)
    ax_d.axvline(-1,  color=MUTED, linewidth=0.7, linestyle="--", alpha=0.5)
    ax_d.axvline( 1,  color=MUTED, linewidth=0.7, linestyle="--", alpha=0.5)
    ax_d.set_xlabel("log₂ fold change", fontsize=8)
    ax_d.set_ylabel("−log₁₀ p-value",   fontsize=8)

    # Annotate top 5 genes with controlled offsets to avoid overlap
    top_idx = np.argsort(nlp)[-5:]
    offsets = [(-0.9, 0.5), (0.9, 0.5), (-0.9, -0.5), (0.9, -0.5), (0.0, 0.7)]
    for ii, gi in enumerate(top_idx):
        dx, dy = offsets[ii]
        ax_d.annotate(f"Gene{gi:03d}",
                      xy=(log2fc[gi], nlp[gi]),
                      xytext=(log2fc[gi] + dx, nlp[gi] + dy),
                      fontsize=5.5, color=TEXT, alpha=0.85,
                      arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.5))

    ax_d.legend(fontsize=7, frameon=True, framealpha=0.25,
                facecolor=CARD, edgecolor="#2a2d3e",
                labelcolor=TEXT, loc="upper left")
    style_ax(ax_d, "D  Volcano Plot", "omics · mechanism_highlight_neutral")

    # ── Panel E: FigureLint-Bio score card ────────────────────────────────────
    ax_e = fig.add_subplot(gs[1, 2:4])
    ax_e.set_facecolor(CARD)
    ax_e.set_xlim(0, 10)
    ax_e.set_ylim(0, 10)
    ax_e.axis("off")
    style_ax(ax_e, "E  FigureLint-Bio Report", "pre-submission figure QA")

    # Score ring
    score   = 85
    ring_bg = Wedge((1.8, 5.8), 1.55, 0, 360, width=0.42,
                    facecolor="#2a2d3e", edgecolor="none")
    ring_fg = Wedge((1.8, 5.8), 1.55, 90, 90 - 360 * score / 100, width=0.42,
                    facecolor="#34d399", edgecolor="none")
    ax_e.add_patch(ring_bg)
    ax_e.add_patch(ring_fg)
    ax_e.text(1.8, 5.9,  f"{score}", ha="center", va="center",
              fontsize=20, color="#34d399", fontweight="bold")
    ax_e.text(1.8, 4.75, "/ 100",    ha="center", va="center",
              fontsize=8,  color=MUTED)
    ax_e.text(1.8, 4.25, "SCORE",    ha="center", va="center",
              fontsize=7,  color=MUTED, fontweight="bold")

    # Issues list — two columns: tag + message
    issues = [
        ("ERROR",      "#ef4444", "DPI 150 below minimum 300"),
        ("WARNING",    "#f59e0b", "legend has 14 items (>10)"),
        ("SUGGESTION", ACCENT,    "use PDF for line art figures"),
        ("SUGGESTION", ACCENT,    "prefer CB-safe palette (clinical)"),
        ("PASSED",     "#34d399", "palette fits field 'clinical'"),
        ("PASSED",     "#34d399", "font size 8 pt ≥ threshold"),
        ("PASSED",     "#34d399", "figure width 89 mm ≥ 80 mm"),
    ]
    TAG_COL_X = 3.5   # left edge of tag column
    MSG_COL_X = 5.4   # left edge of message column
    ROW_SPC   = 1.0   # vertical spacing per issue row
    TOP_Y     = 9.0   # y of first row

    for row, (tag, col, msg) in enumerate(issues):
        y_pos = TOP_Y - row * ROW_SPC
        bullet = "●" if tag in ("ERROR","WARNING","SUGGESTION") else "✓"
        ax_e.text(TAG_COL_X, y_pos, f"{bullet} {tag}",
                  ha="left", va="center", fontsize=6.8, color=col, fontweight="bold")
        ax_e.text(MSG_COL_X, y_pos, msg,
                  ha="left", va="center", fontsize=6.8, color=TEXT, alpha=0.88)

    # Supra-title
    fig.text(0.5, 0.935,
             "PubChroma + FigureLint-Bio  ·  Figure examples across scientific domains",
             ha="center", fontsize=13.5, fontweight="bold", color=TEXT)

    fig.savefig(os.path.join(OUT, "banner_examples.png"),
                dpi=180, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("✓ banner_examples.png")


# ═══════════════════════════════════════════════════════════════════════════════
# 3. WORKFLOW DIAGRAM
# ═══════════════════════════════════════════════════════════════════════════════

def make_workflow():
    FIG_W, FIG_H = 16, 5.5

    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), facecolor=BG)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, FIG_W)
    ax.set_ylim(0, FIG_H)
    ax.axis("off")

    # Supra-title
    fig.text(0.5, 0.95,
             "Workflow: From figure intent to submission-ready QA",
             ha="center", va="top", fontsize=13, fontweight="bold", color=TEXT)

    steps = [
        (1.6,   "1. Describe\nyour figure",    "field, figure_type\nvariable_type, n_groups",      "#4f8ef7", "●"),
        (4.8,   "2. Recommend\npalette",        "recommend_palette()\nreturns palette_id + hex",    "#a78bfa", "◆"),
        (8.0,   "3. Validate\npalette",         "validate_palette()\nchecks registry + field rules","#fb923c", "▲"),
        (11.2,  "4. Lint\nfigure spec",         "lint_figure_spec()\n15 rules, 3 severities",       "#34d399", "■"),
        (14.4,  "5. Review\nreport",            "generate_markdown_report()\nerrors / score",        "#f472b6", "★"),
    ]

    BOX_W = 2.6
    BOX_H = 2.1
    CY    = 3.1   # vertical centre of cards

    for x, title, subtitle, color, icon in steps:
        card = FancyBboxPatch((x - BOX_W / 2, CY - BOX_H / 2), BOX_W, BOX_H,
                              boxstyle="round,pad=0.14",
                              facecolor=CARD, edgecolor=color, linewidth=1.6)
        ax.add_patch(card)

        # Icon at top of card
        ax.text(x, CY + BOX_H / 2 - 0.30, icon,
                ha="center", va="center", fontsize=14, color=color)

        # Title centred in card (two lines)
        ax.text(x, CY + 0.22, title,
                ha="center", va="center", fontsize=9, color=TEXT,
                fontweight="bold", linespacing=1.35)

        # Subtitle below title — clear vertical gap
        ax.text(x, CY - 0.70, subtitle,
                ha="center", va="center", fontsize=7, color=MUTED,
                linespacing=1.35)

    # Arrows between cards
    for i in range(len(steps) - 1):
        x1 = steps[i][0]   + BOX_W / 2
        x2 = steps[i+1][0] - BOX_W / 2
        ax.annotate("",
                    xy=(x2, CY), xytext=(x1, CY),
                    arrowprops=dict(arrowstyle="-|>", color=MUTED,
                                   lw=1.3, mutation_scale=16))

    # Code banner at bottom — split into two lines so it doesn't overflow
    banner_y0 = 0.10
    banner_h  = 0.90
    code_bg = FancyBboxPatch((0.25, banner_y0), FIG_W - 0.50, banner_h,
                             boxstyle="round,pad=0.06",
                             facecolor="#0d1117", edgecolor="#2a2d3e", linewidth=0.8)
    ax.add_patch(code_bg)

    line1 = "result = recommend_palette('clinical', 'box', n_groups=4, colorblind_safe=True)"
    line2 = "report = lint_figure_spec({...})   →   print(generate_markdown_report(report))"
    mid_y = banner_y0 + banner_h / 2
    ax.text(FIG_W / 2, mid_y + 0.20, line1,
            ha="center", va="center", fontsize=7.8, color="#a78bfa", family="monospace")
    ax.text(FIG_W / 2, mid_y - 0.20, line2,
            ha="center", va="center", fontsize=7.8, color="#4DBBD5", family="monospace")

    fig.savefig(os.path.join(OUT, "banner_workflow.png"),
                dpi=180, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("✓ banner_workflow.png")


if __name__ == "__main__":
    make_palette_banner()
    make_science_examples()
    make_workflow()
    print("\nAll images saved to docs/")
