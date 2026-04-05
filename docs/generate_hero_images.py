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
from matplotlib.gridspec import GridSpec
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe

OUT = os.path.join(os.path.dirname(__file__))

# ── Typography ────────────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.spines.left": False,
    "axes.spines.bottom": False,
})

BG = "#0f1117"
CARD = "#1a1d27"
TEXT = "#e8eaf0"
MUTED = "#8b8fa8"
ACCENT = "#4f8ef7"

# ═══════════════════════════════════════════════════════════════════════════════
# 1. PALETTE BANNER
# ═══════════════════════════════════════════════════════════════════════════════

def make_palette_banner():
    palettes = {
        "Clinical\nConservative 4":
            (["#374E55","#DF8F44","#00A1D5","#B24745"], "clinical", True),
        "Clinical\nConservative 6":
            (["#374E55","#DF8F44","#00A1D5","#B24745","#79AF97","#6A6599"], "clinical", True),
        "Omics\nDiverging":
            (["#3C5488","#FFFFFF","#E64B35"], "omics", True),
        "Omics\nSequential":
            (["#F7FBFF","#C6DBEF","#9ECAE1","#6BAED6","#3182BD","#08519C","#08306B"], "omics", True),
        "Single-cell\n12-color":
            (["#E64B35","#4DBBD5","#00A087","#3C5488","#F39B7F","#8491B4",
              "#91D1C2","#DC0000","#7E6148","#B09C85","#4DB8FF","#FFDB6D"], "singlecell", False),
        "Engineering\nSequential":
            (["#FFF7FB","#ECE2F0","#D0D1E6","#A6BDDB","#67A9CF","#1C9099","#016C59"], "engineering", True),
        "Engineering\nCategorical":
            (["#3B4992","#EE0000","#008B45","#631879","#008280","#BB0021"], "engineering", False),
        "Mechanism\nHighlight":
            (["#E64B35","#3C5488","#AAAAAA","#DDDDDD"], "mechanism", True),
        "Okabe-Ito\nUniversal":
            (["#E69F00","#56B4E9","#009E73","#F0E442","#0072B2","#D55E00","#CC79A7","#000000"],
             "universal", True),
    }

    FIELD_COLORS = {
        "clinical":    "#4f8ef7",
        "omics":       "#a78bfa",
        "singlecell":  "#34d399",
        "engineering": "#fb923c",
        "mechanism":   "#f472b6",
        "universal":   "#94a3b8",
    }

    n_rows = len(palettes)
    fig_h = n_rows * 0.72 + 1.8
    fig_w = 14

    fig = plt.figure(figsize=(fig_w, fig_h), facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(BG)
    ax.set_xlim(0, fig_w)
    ax.set_ylim(0, fig_h)
    ax.axis("off")

    # Title
    ax.text(fig_w / 2, fig_h - 0.35, "PubChroma  ·  Journal-Inspired Colour Palettes",
            ha="center", va="center", fontsize=16, fontweight="bold",
            color=TEXT, family="DejaVu Sans")
    ax.text(fig_w / 2, fig_h - 0.75,
            "field-aware  ·  figure-aware  ·  accessibility-aware",
            ha="center", va="center", fontsize=9, color=MUTED)

    LABEL_W = 2.6
    SWATCH = 0.52
    GAP = 0.06
    ROW_H = 0.60
    BADGE_X = LABEL_W + 20 * (SWATCH + GAP) + 0.1

    for i, (name, (colors, field, cb)) in enumerate(palettes.items()):
        y = fig_h - 1.2 - i * ROW_H
        cy = y - ROW_H * 0.35

        # Field tag
        fc = FIELD_COLORS.get(field, MUTED)
        tag = FancyBboxPatch((0.08, cy - 0.12), 0.55, 0.26,
                             boxstyle="round,pad=0.04",
                             facecolor=fc + "33", edgecolor=fc, linewidth=0.8)
        ax.add_patch(tag)
        ax.text(0.355, cy + 0.01, field, ha="center", va="center",
                fontsize=5.5, color=fc, fontweight="bold")

        # Palette name
        ax.text(LABEL_W - 0.15, cy + 0.01, name,
                ha="right", va="center", fontsize=8, color=TEXT)

        # Swatches
        for j, color in enumerate(colors):
            x = LABEL_W + j * (SWATCH + GAP)
            # Outline for very light colors
            edge = "#555566" if color.upper() in ("#FFFFFF", "#F7FBFF", "#FFF7FB",
                                                   "#F0E442", "#DDDDDD") else "none"
            rect = FancyBboxPatch((x, cy - 0.20), SWATCH, 0.40,
                                  boxstyle="round,pad=0.03",
                                  facecolor=color, edgecolor=edge, linewidth=0.5)
            ax.add_patch(rect)

        # CB badge
        if cb:
            ax.text(BADGE_X, cy + 0.01, "✓ CB-safe",
                    ha="left", va="center", fontsize=7,
                    color="#34d399", fontweight="bold")

    # Footer
    ax.text(fig_w / 2, 0.22,
            "pip install pubchroma[recommend]   ·   github.com/tyuan2024/pubchroma",
            ha="center", va="center", fontsize=8, color=MUTED,
            family="monospace")

    fig.savefig(os.path.join(OUT, "banner_palettes.png"),
                dpi=180, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("✓ banner_palettes.png")


# ═══════════════════════════════════════════════════════════════════════════════
# 2. FOUR SCIENTIFIC FIGURE EXAMPLES
# ═══════════════════════════════════════════════════════════════════════════════

def make_science_examples():
    rng = np.random.default_rng(42)

    fig = plt.figure(figsize=(16, 10), facecolor=BG)
    fig.patch.set_facecolor(BG)

    gs = GridSpec(2, 4, figure=fig, hspace=0.45, wspace=0.38,
                  left=0.05, right=0.97, top=0.88, bottom=0.08)

    # Shared style
    def style_ax(ax, title, subtitle=""):
        ax.set_facecolor(CARD)
        for sp in ax.spines.values():
            sp.set_color("#2a2d3e")
            sp.set_linewidth(0.8)
        ax.tick_params(colors=MUTED, labelsize=7)
        ax.xaxis.label.set_color(MUTED)
        ax.yaxis.label.set_color(MUTED)
        ax.set_title(title, color=TEXT, fontsize=9.5, fontweight="bold", pad=6)
        if subtitle:
            ax.annotate(subtitle, xy=(0.5, 1.02), xycoords="axes fraction",
                        ha="center", fontsize=7, color=MUTED)

    # ── Panel A: Clinical boxplot ──────────────────────────────────────────
    ax_a = fig.add_subplot(gs[0, 0])
    palette_clin = ["#374E55", "#DF8F44", "#00A1D5", "#B24745"]
    arms = ["Placebo", "Low", "Mid", "High"]
    data_clin = [rng.normal(loc, 0.7, 28) for loc in [0, 0.6, 1.1, 1.7]]
    bp = ax_a.boxplot(data_clin, patch_artist=True, notch=False,
                      widths=0.55, medianprops=dict(color="white", linewidth=1.5),
                      whiskerprops=dict(color=MUTED), capprops=dict(color=MUTED),
                      flierprops=dict(marker="o", markerfacecolor=MUTED,
                                     markersize=2.5, alpha=0.5, linestyle="none"))
    for patch, c in zip(bp["boxes"], palette_clin):
        patch.set_facecolor(c)
        patch.set_alpha(0.88)
    ax_a.set_xticklabels(arms, fontsize=7)
    ax_a.set_ylabel("Biomarker (AU)", fontsize=7.5)
    ax_a.axhline(0, color=MUTED, linewidth=0.4, linestyle="--", alpha=0.4)
    style_ax(ax_a, "A  Clinical Boxplot", "clinical  ·  medical_conservative")

    # Significance bracket
    y_max = max(max(d) for d in data_clin) + 0.3
    ax_a.annotate("", xy=(4, y_max), xytext=(1, y_max),
                  arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
    ax_a.text(2.5, y_max + 0.08, "p = 0.003", ha="center",
              fontsize=6.5, color=TEXT)

    # ── Panel B: Omics heatmap ─────────────────────────────────────────────
    ax_b = fig.add_subplot(gs[0, 1])
    from matplotlib.colors import LinearSegmentedColormap  # noqa: PLC0415
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
    style_ax(ax_b, "B  Omics Heatmap", "omics  ·  diverging  ·  cns_inspired")

    # ── Panel C: Single-cell UMAP ──────────────────────────────────────────
    ax_c = fig.add_subplot(gs[0, 2:4])
    palette_sc = [
        "#E64B35","#4DBBD5","#00A087","#3C5488","#F39B7F",
        "#8491B4","#91D1C2","#DC0000","#7E6148","#B09C85",
        "#4DB8FF","#FFDB6D",
    ]
    n_cells = 1800
    n_types = 12

    # Simulate cluster structure
    angles = np.linspace(0, 2 * np.pi, n_types, endpoint=False)
    radii = [2.8, 2.2, 3.1, 2.5, 3.4, 2.0, 2.9, 3.2, 1.8, 2.6, 3.0, 2.4]
    x_all, y_all, c_all = [], [], []
    per_type = n_cells // n_types
    for k in range(n_types):
        cx = radii[k] * np.cos(angles[k]) + rng.normal(0, 0.2)
        cy_k = radii[k] * np.sin(angles[k]) + rng.normal(0, 0.2)
        spread = rng.uniform(0.35, 0.75)
        x_all.extend(rng.normal(cx, spread, per_type))
        y_all.extend(rng.normal(cy_k, spread, per_type))
        c_all.extend([palette_sc[k]] * per_type)

    # Shuffle
    idx = rng.permutation(len(x_all))
    x_all = np.array(x_all)[idx]
    y_all = np.array(y_all)[idx]
    c_all = np.array(c_all)[idx]

    ax_c.scatter(x_all, y_all, c=c_all, s=3.5, alpha=0.72, linewidths=0)

    # Legend (compact, 2 cols)
    cell_types = [f"Type {i+1}" for i in range(n_types)]
    handles = [mpatches.Patch(color=c, label=l)
               for c, l in zip(palette_sc, cell_types)]
    leg = ax_c.legend(handles=handles, ncol=4, fontsize=6.5,
                      frameon=True, framealpha=0.25,
                      facecolor=CARD, edgecolor="#2a2d3e",
                      labelcolor=TEXT, loc="lower right",
                      markerscale=1.5, handlelength=1.2,
                      columnspacing=0.8, handletextpad=0.5)
    ax_c.set_xticks([])
    ax_c.set_yticks([])
    ax_c.set_xlabel("UMAP 1", fontsize=7.5)
    ax_c.set_ylabel("UMAP 2", fontsize=7.5)
    style_ax(ax_c, "C  Single-Cell UMAP", "singlecell  ·  categorical  ·  12 cell types")

    # ── Panel D: Volcano plot ──────────────────────────────────────────────
    ax_d = fig.add_subplot(gs[1, 0:2])
    n_genes = 600
    log2fc = rng.normal(0, 1.2, n_genes)
    pvals = np.abs(rng.normal(0, 1, n_genes))
    neg_log10p = pvals * rng.uniform(0.5, 4, n_genes)

    # Color by significance
    sig_up = (log2fc > 1) & (neg_log10p > 1.3)
    sig_dn = (log2fc < -1) & (neg_log10p > 1.3)
    nonsig = ~(sig_up | sig_dn)

    ax_d.scatter(log2fc[nonsig], neg_log10p[nonsig],
                 s=5, c="#6b7280", alpha=0.45, linewidths=0, label="NS")
    ax_d.scatter(log2fc[sig_up], neg_log10p[sig_up],
                 s=9, c="#E64B35", alpha=0.82, linewidths=0, label=f"Up ({sig_up.sum()})")
    ax_d.scatter(log2fc[sig_dn], neg_log10p[sig_dn],
                 s=9, c="#3C5488", alpha=0.82, linewidths=0, label=f"Down ({sig_dn.sum()})")

    ax_d.axhline(1.3, color=MUTED, linewidth=0.7, linestyle="--", alpha=0.5)
    ax_d.axvline(-1, color=MUTED, linewidth=0.7, linestyle="--", alpha=0.5)
    ax_d.axvline(1, color=MUTED, linewidth=0.7, linestyle="--", alpha=0.5)
    ax_d.set_xlabel("log₂ fold change", fontsize=8)
    ax_d.set_ylabel("−log₁₀ p-value", fontsize=8)

    # Annotate top genes
    top_idx = np.argsort(neg_log10p)[-5:]
    for idx in top_idx:
        ax_d.annotate(f"Gene{idx:03d}",
                      xy=(log2fc[idx], neg_log10p[idx]),
                      xytext=(log2fc[idx] + rng.choice([-0.6, 0.6]),
                              neg_log10p[idx] + 0.3),
                      fontsize=5.5, color=TEXT, alpha=0.85,
                      arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.5))

    leg_d = ax_d.legend(fontsize=7, frameon=True, framealpha=0.25,
                        facecolor=CARD, edgecolor="#2a2d3e",
                        labelcolor=TEXT, loc="upper left")
    style_ax(ax_d, "D  Volcano Plot", "omics  ·  mechanism_highlight_neutral")

    # ── Panel E: FigureLint score card ────────────────────────────────────
    ax_e = fig.add_subplot(gs[1, 2:4])
    ax_e.set_facecolor(CARD)
    ax_e.set_xlim(0, 10)
    ax_e.set_ylim(0, 10)
    ax_e.axis("off")
    for sp in ax_e.spines.values():
        sp.set_color("#2a2d3e")

    ax_e.set_title("E  FigureLint-Bio Report", color=TEXT,
                   fontsize=9.5, fontweight="bold", pad=6)
    ax_e.annotate("pre-submission figure QA", xy=(0.5, 1.02),
                  xycoords="axes fraction", ha="center", fontsize=7, color=MUTED)

    # Score ring (simple arc)
    from matplotlib.patches import Wedge
    score = 85
    ring_bg = Wedge((2.2, 6.5), 1.6, 0, 360, width=0.45,
                    facecolor="#2a2d3e", edgecolor="none")
    ring_fg = Wedge((2.2, 6.5), 1.6, 90, 90 - 360 * score / 100, width=0.45,
                    facecolor="#34d399", edgecolor="none")
    ax_e.add_patch(ring_bg)
    ax_e.add_patch(ring_fg)
    ax_e.text(2.2, 6.5, f"{score}", ha="center", va="center",
              fontsize=18, color="#34d399", fontweight="bold")
    ax_e.text(2.2, 5.35, "/ 100", ha="center", va="center",
              fontsize=8, color=MUTED)
    ax_e.text(2.2, 4.85, "SCORE", ha="center", va="center",
              fontsize=7, color=MUTED, fontweight="bold")

    # Issues list
    issues = [
        ("● ERROR",      "#ef4444", "DPI 150 is below minimum 300"),
        ("● WARNING",    "#f59e0b", "legend has 14 items (>10 recommended)"),
        ("● SUGGESTION", ACCENT,    "use PDF for line art figures"),
        ("● SUGGESTION", ACCENT,    "clinical figures: prefer CB-safe palette"),
        ("✓ PASSED",     "#34d399", "palette fits field 'clinical'"),
        ("✓ PASSED",     "#34d399", "font size 8 pt meets threshold"),
        ("✓ PASSED",     "#34d399", "figure width 89 mm ≥ 80 mm"),
    ]

    x0 = 4.0
    for row, (tag, col, msg) in enumerate(issues):
        y_pos = 9.2 - row * 1.18
        ax_e.text(x0, y_pos, tag, ha="left", va="center",
                  fontsize=7, color=col, fontweight="bold")
        ax_e.text(x0 + 1.7, y_pos, msg, ha="left", va="center",
                  fontsize=7, color=TEXT, alpha=0.85)

    # Supra-title
    fig.text(0.5, 0.94,
             "PubChroma + FigureLint-Bio  ·  Figure examples across scientific domains",
             ha="center", fontsize=13, fontweight="bold", color=TEXT)

    fig.savefig(os.path.join(OUT, "banner_examples.png"),
                dpi=180, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("✓ banner_examples.png")


# ═══════════════════════════════════════════════════════════════════════════════
# 3. WORKFLOW DIAGRAM
# ═══════════════════════════════════════════════════════════════════════════════

def make_workflow():
    fig, ax = plt.subplots(figsize=(14, 4.5), facecolor=BG)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 4.5)
    ax.axis("off")

    fig.text(0.5, 0.93, "Workflow: From figure intent to submission-ready QA",
             ha="center", va="center", fontsize=13, fontweight="bold", color=TEXT)

    # Step definitions
    steps = [
        (1.4,  "1. Describe\nyour figure",
         "field, figure_type,\nvariable_type, n_groups",
         "#4f8ef7", "●"),
        (4.2,  "2. Recommend\npalette",
         "recommend_palette()\nreturns palette_id + hex",
         "#a78bfa", "◆"),
        (7.0,  "3. Validate\npalette",
         "validate_palette()\nchecks registry + field rules",
         "#fb923c", "▲"),
        (9.8,  "4. Lint\nfigure spec",
         "lint_figure_spec()\n15 rules, 3 severities",
         "#34d399", "■"),
        (12.6, "5. Review\nreport",
         "generate_markdown_report()\nerrors / warnings / score",
         "#f472b6", "★"),
    ]

    BOX_W, BOX_H = 2.0, 1.9
    CY = 2.1

    for x, title, subtitle, color, icon in steps:
        # Card
        card = FancyBboxPatch((x - BOX_W / 2, CY - BOX_H / 2), BOX_W, BOX_H,
                              boxstyle="round,pad=0.12",
                              facecolor=CARD, edgecolor=color, linewidth=1.5)
        ax.add_patch(card)

        # Icon
        ax.text(x, CY + BOX_H / 2 - 0.28, icon,
                ha="center", va="center", fontsize=13, color=color)
        # Title
        ax.text(x, CY + 0.18, title, ha="center", va="center",
                fontsize=8.5, color=TEXT, fontweight="bold", linespacing=1.4)
        # Subtitle
        ax.text(x, CY - 0.58, subtitle, ha="center", va="center",
                fontsize=6.8, color=MUTED, linespacing=1.35)

    # Arrows between cards
    for i in range(len(steps) - 1):
        x1 = steps[i][0] + BOX_W / 2
        x2 = steps[i+1][0] - BOX_W / 2
        ax.annotate("",
                    xy=(x2, CY), xytext=(x1, CY),
                    arrowprops=dict(arrowstyle="-|>", color=MUTED,
                                   lw=1.2, mutation_scale=14))

    # Code snippet banner at bottom
    code_bg = FancyBboxPatch((0.3, 0.12), 13.4, 0.72,
                             boxstyle="round,pad=0.05",
                             facecolor="#0d1117", edgecolor="#2a2d3e", linewidth=0.8)
    ax.add_patch(code_bg)
    snippet = (
        "result = recommend_palette('clinical', 'box', n_groups=4, colorblind_safe=True)   "
        "report = lint_figure_spec({...})   "
        "print(generate_markdown_report(report))"
    )
    ax.text(7.0, 0.48, snippet, ha="center", va="center",
            fontsize=7.5, color="#a78bfa", family="monospace")

    fig.savefig(os.path.join(OUT, "banner_workflow.png"),
                dpi=180, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("✓ banner_workflow.png")


if __name__ == "__main__":
    make_palette_banner()
    make_science_examples()
    make_workflow()
    print("\nAll images saved to docs/")
