#' Validate a palette against the registry and field conventions
#'
#' Cross-references a palette (by ID or hex list) against the shared
#' \code{data/palettes.yml} registry.  Returns structured errors, warnings,
#' and suggestions.
#'
#' @param palette_id Character or NULL. A registered palette identifier.
#' @param hex_colors Character vector or NULL. Custom hex list to validate.
#' @param field Character or NULL. Scientific domain for field-specific checks.
#' @param n_groups Integer or NULL. Number of categories.
#' @param colorblind_safe Logical. Whether the figure claims colorblind safety.
#' @param grayscale_safe Logical. Whether the figure claims grayscale safety.
#' @return A named list with elements \code{valid} (logical), \code{palette_id},
#'   \code{hex}, \code{errors}, \code{warnings}, \code{suggestions}.
#' @export
#' @examples
#' result <- validate_palette("clinical_categorical_conservative_4",
#'                            field = "clinical", n_groups = 4)
#' result$valid
#' result$warnings
validate_palette <- function(
    palette_id = NULL,
    hex_colors = NULL,
    field = NULL,
    n_groups = NULL,
    colorblind_safe = FALSE,
    grayscale_safe = FALSE
) {
  if (is.null(palette_id) && is.null(hex_colors)) {
    stop("Provide at least one of palette_id or hex_colors.")
  }

  palettes_data <- .load_palettes_yaml()
  palettes <- palettes_data$palettes

  errors      <- character(0)
  warnings    <- character(0)
  suggestions <- character(0)
  pal_meta    <- NULL
  resolved_hex <- character(0)

  if (!is.null(palette_id)) {
    if (!palette_id %in% names(palettes)) {
      errors <- c(errors, sprintf(
        "Palette '%s' is not in the registry. Available: %s.",
        palette_id, paste(sort(names(palettes)), collapse = ", ")
      ))
    } else {
      pal_meta     <- palettes[[palette_id]]
      resolved_hex <- unlist(pal_meta$colors)
    }
  }

  if (!is.null(hex_colors)) {
    resolved_hex <- hex_colors
    invalid <- hex_colors[!grepl("^#[0-9A-Fa-f]{6}$", hex_colors)]
    if (length(invalid) > 0) {
      errors <- c(errors, sprintf("Invalid hex colors: %s",
                                  paste(invalid, collapse = ", ")))
    }
  }

  if (!is.null(pal_meta)) {
    n_max <- pal_meta$n_max %||% 999L

    if (!is.null(n_groups) && n_groups > n_max) {
      errors <- c(errors, sprintf(
        "n_groups=%d exceeds palette capacity n_max=%d.", n_groups, n_max
      ))
    }

    if (colorblind_safe && !isTRUE(pal_meta$colorblind_safe)) {
      errors <- c(errors, sprintf(
        "Palette '%s' is not marked colorblind-safe, but colorblind_safe=TRUE was claimed.",
        palette_id
      ))
    }
    if (grayscale_safe && !isTRUE(pal_meta$grayscale_safe)) {
      errors <- c(errors, sprintf(
        "Palette '%s' is not marked grayscale-safe, but grayscale_safe=TRUE was claimed.",
        palette_id
      ))
    }

    if (!is.null(field)) {
      field_rules <- .load_field_rules()
      field_cfg   <- field_rules$fields[[tolower(field)]]
      if (!is.null(field_cfg)) {
        preferred <- field_cfg$preferred_palette_ids %||% character(0)
        if (length(preferred) > 0 && !is.null(palette_id) && !palette_id %in% preferred) {
          warnings <- c(warnings, sprintf(
            "Palette '%s' is not in the preferred list for field '%s'. Preferred: %s.",
            palette_id, field, paste(preferred, collapse = ", ")
          ))
        }
        if (isTRUE(field_cfg$colorblind_safe_recommended) &&
            !isTRUE(pal_meta$colorblind_safe)) {
          suggestions <- c(suggestions, sprintf(
            "Field '%s' recommends colorblind-safe palettes. Current palette is not verified safe.",
            field
          ))
        }
      }
    }
  }

  list(
    valid       = length(errors) == 0,
    palette_id  = palette_id,
    hex         = resolved_hex,
    errors      = as.list(errors),
    warnings    = as.list(warnings),
    suggestions = as.list(suggestions)
  )
}
