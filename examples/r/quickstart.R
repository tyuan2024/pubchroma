# PubChroma Quick Start — R

# If installed:
# library(pubchroma)

# For development, source directly:
source_dir <- file.path(dirname(rstudioapi::getSourceEditorContext()$path), "../../R/R")
for (f in list.files(source_dir, pattern = "\\.R$", full.names = TRUE)) source(f)

# You also need jsonlite:
# install.packages("jsonlite")

# 1. List all supported journals
cat("Supported journals:\n")
print(list_journals())

# 2. Get colors for Nature
nature_colors <- get_colors("nature", n = 5)
cat("\nNature top-5 colors:\n")
print(nature_colors)

# 3. Check colorblind safety
cat("\nNature main is colorblind-safe:", is_colorblind_safe("nature"), "\n")
cat("Science main is colorblind-safe:", is_colorblind_safe("science"), "\n")

# 4. Find all colorblind-safe palettes
cat("\nAll colorblind-safe palettes:\n")
print(list_colorblind_safe())

# 5. Use with ggplot2 (optional)
if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)

  journals <- c("nature", "science", "nejm", "lancet", "jama")
  plot_data <- do.call(rbind, lapply(journals, function(j) {
    cols <- get_colors(j, n = 8)
    data.frame(
      journal = j,
      x = seq_along(cols),
      color = cols,
      stringsAsFactors = FALSE
    )
  }))

  p <- ggplot(plot_data, aes(x = x, y = journal, fill = I(color))) +
    geom_tile(width = 0.9, height = 0.9) +
    scale_x_continuous(breaks = NULL) +
    labs(title = "PubChroma — Journal Palettes", x = NULL, y = NULL) +
    theme_minimal()

  ggsave("examples/r/palette_preview.png", p, width = 8, height = 4, dpi = 150)
  cat("\nPalette preview saved to examples/r/palette_preview.png\n")
} else {
  cat("\n(ggplot2 not installed — skipping plot)\n")
}
