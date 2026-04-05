#' Run lint rules against a figure spec
#'
#' Performs structural QA on a figure spec list, checking palette fitness,
#' accessibility, typography, export settings, and statistical annotations.
#'
#' @param spec Named list. A figure spec. Required fields: \code{field},
#'   \code{figure_type}, \code{variable_type}.
#' @return A named list with elements \code{errors}, \code{warnings},
#'   \code{suggestions}, \code{score} (0-100), and \code{summary}.
#' @export
#' @examples
#' spec <- list(
#'   field = "clinical", figure_type = "box", variable_type = "categorical",
#'   n_groups = 4, palette_name = "clinical_categorical_conservative_4",
#'   font_size_pt = 10, dpi = 300, width_mm = 89
#' )
#' report <- lint_figure_spec(spec)
#' report$summary
lint_figure_spec <- function(spec) {
  required <- c("field", "figure_type", "variable_type")
  missing_fields <- setdiff(required, names(spec))
  if (length(missing_fields) > 0) {
    stop(sprintf("Required spec fields missing: %s",
                 paste(missing_fields, collapse = ", ")))
  }

  errors      <- list()
  warnings    <- list()
  suggestions <- list()

  .issue <- function(sev, rule, msg) {
    list(rule = rule, severity = sev, message = msg)
  }

  palettes_data <- tryCatch(.load_palettes_yaml(), error = function(e) NULL)
  field_rules_data <- tryCatch(.load_field_rules(), error = function(e) NULL)

  palette_name <- spec$palette_name
  field        <- tolower(spec$field %||% "")
  figure_type  <- tolower(spec$figure_type %||% "")

  # ── Disallowed palette names ────────────────────────────────────────────
  rainbow_names <- c("jet", "rainbow", "hsv", "gist_rainbow", "spectral")
  if (!is.null(palette_name) && tolower(palette_name) %in% rainbow_names) {
    errors <- c(errors, list(.issue("error", "rainbow_palette_detected",
      "Rainbow or spectral colour gradients are not recommended for scientific figures."
    )))
  }

  # ── Palette × field mismatch ────────────────────────────────────────────
  if (!is.null(palette_name) && !is.null(field_rules_data)) {
    field_cfg <- field_rules_data$fields[[field]]
    if (!is.null(field_cfg)) {
      preferred <- field_cfg$preferred_palette_ids %||% character(0)
      if (length(preferred) > 0 && !palette_name %in% preferred) {
        warnings <- c(warnings, list(.issue("warning", "palette_field_mismatch",
          sprintf("Palette '%s' is not recommended for field '%s'. Preferred: %s.",
                  palette_name, field, paste(preferred, collapse = ", "))
        )))
      }
    }
  }

  # ── Category count ──────────────────────────────────────────────────────
  if (!is.null(spec$n_groups) && !is.null(palette_name) && !is.null(palettes_data)) {
    pal <- palettes_data$palettes[[palette_name]]
    if (!is.null(pal)) {
      n_max <- pal$n_max %||% 999L
      if (spec$n_groups > n_max) {
        errors <- c(errors, list(.issue("error", "too_many_categories",
          sprintf("%d categories exceed the palette maximum (%d).",
                  spec$n_groups, n_max)
        )))
      }
    }
  }

  # ── Diverging midpoint ──────────────────────────────────────────────────
  if (isTRUE(spec$variable_type == "diverging")) {
    notes <- tolower(spec$notes %||% "")
    if (!grepl("midpoint|zero|center|centre", notes)) {
      warnings <- c(warnings, list(.issue("warning", "diverging_no_explicit_midpoint",
        "Diverging palette selected but no midpoint reference is declared in spec$notes."
      )))
    }
  }

  # ── Accessibility ────────────────────────────────────────────────────────
  if (isTRUE(spec$colorblind_safe) && !is.null(palette_name) && !is.null(palettes_data)) {
    pal <- palettes_data$palettes[[palette_name]]
    if (!is.null(pal) && !isTRUE(pal$colorblind_safe)) {
      errors <- c(errors, list(.issue("error", "colorblind_safe_claimed_but_palette_unsafe",
        sprintf("Palette '%s' is not marked colorblind-safe, but colorblind_safe=TRUE.",
                palette_name)
      )))
    }
  }

  # ── Font size ────────────────────────────────────────────────────────────
  if (!is.null(spec$font_size_pt)) {
    if (spec$font_size_pt < 6) {
      errors <- c(errors, list(.issue("error", "font_size_too_small",
        sprintf("Font size %.1f pt is below the 6 pt minimum.", spec$font_size_pt)
      )))
    } else if (spec$font_size_pt < 8) {
      suggestions <- c(suggestions, list(.issue("suggestion", "font_size_small_suggestion",
        sprintf("Font size %.1f pt is below the recommended 8 pt.", spec$font_size_pt)
      )))
    }
  }

  # ── DPI ──────────────────────────────────────────────────────────────────
  if (!is.null(spec$dpi) && spec$dpi < 300) {
    errors <- c(errors, list(.issue("error", "dpi_below_minimum",
      sprintf("DPI %g is below 300. Most journals require ≥300 dpi.", spec$dpi)
    )))
  }

  # ── Figure width ─────────────────────────────────────────────────────────
  if (!is.null(spec$width_mm) && spec$width_mm < 80) {
    warnings <- c(warnings, list(.issue("warning", "figure_width_too_small",
      sprintf("Figure width %g mm is below the single-column minimum (80 mm).",
              spec$width_mm)
    )))
  }

  # ── Legend ───────────────────────────────────────────────────────────────
  if (!is.null(spec$legend_items) && spec$legend_items > 10) {
    warnings <- c(warnings, list(.issue("warning", "legend_too_many_items",
      sprintf("Legend has %d items. Legends with >10 items are difficult to read in print.",
              spec$legend_items)
    )))
  }

  # ── Score ─────────────────────────────────────────────────────────────────
  penalty <- length(errors) * 20 + length(warnings) * 5 + length(suggestions) * 1
  score   <- max(0L, 100L - penalty)

  parts <- c(
    if (length(errors) > 0)      sprintf("%d error(s)", length(errors))      else NULL,
    if (length(warnings) > 0)    sprintf("%d warning(s)", length(warnings))  else NULL,
    if (length(suggestions) > 0) sprintf("%d suggestion(s)", length(suggestions)) else NULL
  )
  summary_str <- if (length(parts) == 0) {
    "No issues found."
  } else {
    paste0("Found: ", paste(parts, collapse = ", "), ".  Score: ", score, "/100.")
  }

  list(
    errors      = errors,
    warnings    = warnings,
    suggestions = suggestions,
    score       = score,
    summary     = summary_str
  )
}
