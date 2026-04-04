"""
PubChroma Quick Start — Python
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../src"))

import pubchroma as pc

# 1. List all supported journals
print("Supported journals:")
print(pc.list_journals())

# 2. Get colors for Nature (default: main palette)
nature_colors = pc.get_colors("nature", n=5)
print("\nNature top-5 colors:", nature_colors)

# 3. Check colorblind safety
print("\nNature main is colorblind-safe:", pc.is_colorblind_safe("nature"))
print("Science main is colorblind-safe:", pc.is_colorblind_safe("science"))

# 4. Find all colorblind-safe palettes
print("\nAll colorblind-safe palettes:")
for item in pc.list_colorblind_safe():
    print(f"  {item['journal']}/{item['palette']} ({item['n_colors']} colors)")

# 5. Use with matplotlib (optional)
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    journals = ["nature", "science", "nejm", "lancet", "jama"]
    fig, axes = plt.subplots(len(journals), 1, figsize=(10, 6))

    for ax, journal in zip(axes, journals):
        colors = pc.get_colors(journal, n=8)
        for i, color in enumerate(colors):
            ax.add_patch(mpatches.Rectangle((i, 0), 1, 1, color=color))
        ax.set_xlim(0, 8)
        ax.set_ylim(0, 1)
        ax.set_yticks([])
        ax.set_ylabel(journal, rotation=0, ha="right", va="center")
        ax.set_xticks([])

    plt.suptitle("PubChroma — Journal Palettes", y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(os.path.dirname(__file__), "palette_preview.png"),
                dpi=150, bbox_inches="tight")
    print("\nPalette preview saved to examples/python/palette_preview.png")
except ImportError:
    print("\n(matplotlib not installed — skipping plot)")
