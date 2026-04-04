#' List all available journal keys
#'
#' @return A character vector of journal keys, sorted alphabetically.
#' @export
#' @examples
#' list_journals()
list_journals <- function() {
  sort(names(.get_data()))
}

#' List all palette names for a journal
#'
#' @param journal Character. Journal key (case-insensitive).
#'   Use [list_journals()] to see available options.
#' @return A character vector of palette names, sorted alphabetically.
#' @export
#' @examples
#' list_palettes("nature")
list_palettes <- function(journal) {
  data <- .get_data()
  key <- tolower(journal)
  if (!key %in% names(data)) {
    stop(sprintf(
      "Journal '%s' not found. Available: %s",
      journal, paste(sort(names(data)), collapse = ", ")
    ))
  }
  sort(names(data[[key]][["palettes"]]))
}

#' Get full palette metadata for a journal
#'
#' @param journal Character. Journal key (case-insensitive).
#' @param palette Character. Palette name within that journal. Default `"main"`.
#' @return A list with elements `colors`, `colorblind_safe`, `description`, `type`.
#' @export
#' @examples
#' p <- get_palette("nature")
#' p$colors[1:3]
get_palette <- function(journal, palette = "main") {
  data <- .get_data()
  key <- tolower(journal)
  if (!key %in% names(data)) {
    stop(sprintf(
      "Journal '%s' not found. Available: %s",
      journal, paste(sort(names(data)), collapse = ", ")
    ))
  }
  palettes <- data[[key]][["palettes"]]
  pal <- tolower(palette)
  if (!pal %in% names(palettes)) {
    stop(sprintf(
      "Palette '%s' not found for '%s'. Available: %s",
      palette, journal, paste(sort(names(palettes)), collapse = ", ")
    ))
  }
  palettes[[pal]]
}

#' Get hex color codes for a journal palette
#'
#' @param journal Character. Journal key (case-insensitive).
#' @param palette Character. Palette name. Default `"main"`.
#' @param n Integer or NULL. Number of colors to return. If NULL, returns all.
#'   If `n` exceeds the palette length, colors are cycled.
#' @param colorblind_only Logical. If TRUE, error when palette is not colorblind-safe.
#' @return A character vector of hex color codes.
#' @export
#' @examples
#' get_colors("nature", n = 3)
#' get_colors("colorblind", "okabe_ito", colorblind_only = TRUE)
get_colors <- function(journal, palette = "main", n = NULL, colorblind_only = FALSE) {
  pal <- get_palette(journal, palette)

  if (colorblind_only && !isTRUE(pal[["colorblind_safe"]])) {
    stop(sprintf(
      "Palette '%s' for '%s' is not colorblind-safe. ",
      palette, journal
    ))
  }

  colors <- unlist(pal[["colors"]])

  if (is.null(n)) {
    return(colors)
  }

  n <- as.integer(n)
  if (n <= length(colors)) {
    return(colors[seq_len(n)])
  }

  # Cycle colors if n > palette length
  rep_colors <- rep(colors, times = ceiling(n / length(colors)))
  rep_colors[seq_len(n)]
}
