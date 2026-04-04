#' PubChroma palette function for ggplot2
#'
#' Returns a palette function compatible with ggplot2 discrete scales.
#'
#' @param journal Character. Journal key (case-insensitive). Default `"nature"`.
#' @param palette Character. Palette name. Default `"main"`.
#' @param direction Integer. `1` (default) for original order, `-1` to reverse.
#' @return A function that takes an integer `n` and returns `n` hex color codes.
#' @export
#' @examples
#' f <- pubchroma_pal("nejm")
#' f(5)
pubchroma_pal <- function(journal = "nature", palette = "main", direction = 1) {
  if (!direction %in% c(1L, -1L)) stop("`direction` must be 1 or -1")
  function(n) {
    colors <- get_colors(journal, palette, n = n)
    if (direction == -1) rev(colors) else colors
  }
}

#' Discrete color scale using a PubChroma journal palette
#'
#' Applies a journal-inspired color palette to the `colour` aesthetic in ggplot2.
#'
#' @param journal Character. Journal key (case-insensitive). Default `"nature"`.
#' @param palette Character. Palette name within that journal. Default `"main"`.
#' @param direction Integer. `1` for original order, `-1` to reverse. Default `1`.
#' @param ... Additional arguments passed to [ggplot2::discrete_scale()].
#' @return A ggplot2 scale object.
#' @export
#' @examples
#' if (requireNamespace("ggplot2", quietly = TRUE)) {
#'   library(ggplot2)
#'   ggplot(mtcars, aes(wt, mpg, colour = factor(cyl))) +
#'     geom_point() +
#'     scale_color_pubchroma("nejm")
#' }
scale_color_pubchroma <- function(journal = "nature", palette = "main",
                                  direction = 1, ...) {
  if (!requireNamespace("ggplot2", quietly = TRUE)) {
    stop("ggplot2 is required. Install it with: install.packages('ggplot2')")
  }
  ggplot2::discrete_scale(
    aesthetics = "colour",
    palette = pubchroma_pal(journal, palette, direction),
    ...
  )
}

#' @rdname scale_color_pubchroma
#' @export
scale_colour_pubchroma <- scale_color_pubchroma

#' Discrete fill scale using a PubChroma journal palette
#'
#' Applies a journal-inspired color palette to the `fill` aesthetic in ggplot2.
#'
#' @param journal Character. Journal key (case-insensitive). Default `"nature"`.
#' @param palette Character. Palette name within that journal. Default `"main"`.
#' @param direction Integer. `1` for original order, `-1` to reverse. Default `1`.
#' @param ... Additional arguments passed to [ggplot2::discrete_scale()].
#' @return A ggplot2 scale object.
#' @export
#' @examples
#' if (requireNamespace("ggplot2", quietly = TRUE)) {
#'   library(ggplot2)
#'   ggplot(mtcars, aes(factor(cyl), fill = factor(cyl))) +
#'     geom_bar() +
#'     scale_fill_pubchroma("jama")
#' }
scale_fill_pubchroma <- function(journal = "nature", palette = "main",
                                 direction = 1, ...) {
  if (!requireNamespace("ggplot2", quietly = TRUE)) {
    stop("ggplot2 is required. Install it with: install.packages('ggplot2')")
  }
  ggplot2::discrete_scale(
    aesthetics = "fill",
    palette = pubchroma_pal(journal, palette, direction),
    ...
  )
}
