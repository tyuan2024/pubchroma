"""Generate palette preview image for README."""

import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

DATA = Path(__file__).parent.parent / "data" / "palettes" / "journals.json"
OUT = Path(__file__).parent.parent / "docs" / "palette_preview.png"
OUT.parent.mkdir(exist_ok=True)

with open(DATA) as f:
    journals = json.load(f)

# Collect all palettes in display order
entries = []
ORDER = ["nature", "science", "cell", "nejm", "lancet", "jama", "pnas", "bmj", "colorblind"]
for jkey in ORDER:
    jdata = journals[jkey]
    for pname, pdata in jdata["palettes"].items():
        label = jdata["name"] if pname == "main" else f"{jdata['name']} ({pname})"
        entries.append((label, pdata["colors"], pdata["colorblind_safe"]))

N = len(entries)
SWATCH = 1.0   # swatch width
GAP = 0.15     # gap between swatches
ROW_H = 0.55   # row height
LABEL_W = 3.6  # label column width
CB_W = 0.5     # colorblind badge column

max_colors = max(len(e[1]) for e in entries)
fig_w = LABEL_W + max_colors * (SWATCH + GAP) + CB_W + 0.6
fig_h = N * ROW_H + 1.0

fig, ax = plt.subplots(figsize=(fig_w, fig_h))
ax.set_xlim(0, fig_w)
ax.set_ylim(0, fig_h)
ax.axis("off")

# Title
fig.text(0.5, 1 - 0.3 / fig_h, "PubChroma — Journal Color Palettes",
         ha="center", va="top", fontsize=13, fontweight="bold", color="#222")

y_top = fig_h - 0.7

for i, (label, colors, cb_safe) in enumerate(entries):
    y = y_top - i * ROW_H
    cy = y - ROW_H * 0.45

    # Label
    ax.text(LABEL_W - 0.15, cy, label, ha="right", va="center",
            fontsize=8.5, color="#333")

    # Color swatches
    for j, color in enumerate(colors):
        x = LABEL_W + j * (SWATCH + GAP)
        rect = mpatches.FancyBboxPatch(
            (x, cy - 0.18), SWATCH, 0.36,
            boxstyle="round,pad=0.02",
            facecolor=color, edgecolor="white", linewidth=0.8
        )
        ax.add_patch(rect)

    # Colorblind badge
    x_badge = LABEL_W + max_colors * (SWATCH + GAP) + 0.15
    if cb_safe:
        ax.text(x_badge, cy, "✓ CB", ha="left", va="center",
                fontsize=7, color="#2a9d5c", fontweight="bold")

plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig(OUT, dpi=150, bbox_inches="tight", facecolor="white")
print(f"Saved: {OUT}")
