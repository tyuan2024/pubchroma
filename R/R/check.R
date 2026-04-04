#' Check whether a palette is colorblind-safe
#'
#' @param journal Character. Journal key (case-insensitive).
#' @param palette Character. Palette name. Default `"main"`.
#' @return Logical. TRUE if the palette is colorblind-safe.
#' @export
#' @examples
#' is_colorblind_safe("nature")
#' is_colorblind_safe("science")
is_colorblind_safe <- function(journal, palette = "main") {
  isTRUE(get_palette(journal, palette)[["colorblind_safe"]])
}

#' List all colorblind-safe palettes
#'
#' @return A data frame with columns `journal`, `palette`, `n_colors`.
#' @export
#' @examples
#' list_colorblind_safe()
list_colorblind_safe <- function() {
  results <- list()
  for (journal in list_journals()) {
    for (palette in list_palettes(journal)) {
      pal <- get_palette(journal, palette)
      if (isTRUE(pal[["colorblind_safe"]])) {
        results <- c(results, list(data.frame(
          journal = journal,
          palette = palette,
          n_colors = length(unlist(pal[["colors"]])),
          stringsAsFactors = FALSE
        )))
      }
    }
  }
  do.call(rbind, results)
}
