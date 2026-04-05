#' Field-aware palette recommendation
#'
#' Returns the best-matching palette for the given figure context by
#' cross-referencing the shared \code{data/palettes.yml} and
#' \code{data/field_rules.yml} rule files.
#'
#' @param field Character. Scientific domain: \code{"clinical"},
#'   \code{"omics"}, \code{"singlecell"}, \code{"mechanism"},
#'   or \code{"engineering"}.
#' @param figure_type Character. Chart type: \code{"bar"}, \code{"box"},
#'   \code{"violin"}, \code{"line"}, \code{"scatter"}, \code{"heatmap"},
#'   \code{"volcano"}, or \code{"umap"}.
#' @param variable_type Character. Data encoding: \code{"categorical"},
#'   \code{"sequential"}, or \code{"diverging"}. Default \code{"categorical"}.
#' @param n_groups Integer or NULL. Number of categories or levels.
#' @param colorblind_safe Logical. Restrict to colorblind-safe palettes.
#'   Default \code{FALSE}.
#' @param grayscale_safe Logical. Restrict to grayscale-safe palettes.
#'   Default \code{FALSE}.
#' @return A named list with elements \code{palette_id}, \code{hex},
#'   \code{n_max}, \code{variable_type}, \code{journal_family},
#'   \code{colorblind_safe}, \code{grayscale_safe}, \code{rationale},
#'   \code{warnings}.
#' @export
#' @examples
#' result <- recommend_palette("clinical", "box", n_groups = 4,
#'                             colorblind_safe = TRUE)
#' result$palette_id
#' result$hex
recommend_palette <- function(
    field,
    figure_type,
    variable_type = "categorical",
    n_groups = NULL,
    colorblind_safe = FALSE,
    grayscale_safe = FALSE
) {
  valid_fields <- c("clinical", "omics", "singlecell", "mechanism", "engineering")
  valid_figure_types <- c("bar", "box", "violin", "line", "scatter",
                          "heatmap", "volcano", "umap")
  valid_var_types <- c("categorical", "sequential", "diverging")

  field <- tolower(field)
  figure_type <- tolower(figure_type)
  variable_type <- tolower(variable_type)

  if (!field %in% valid_fields) {
    stop(sprintf("field must be one of: %s", paste(valid_fields, collapse = ", ")))
  }
  if (!figure_type %in% valid_figure_types) {
    stop(sprintf("figure_type must be one of: %s", paste(valid_figure_types, collapse = ", ")))
  }
  if (!variable_type %in% valid_var_types) {
    stop(sprintf("variable_type must be one of: %s", paste(valid_var_types, collapse = ", ")))
  }

  palettes_data <- .load_palettes_yaml()
  field_rules   <- .load_field_rules()

  field_cfg    <- field_rules$fields[[field]]
  preferred_ids <- field_cfg$preferred_palette_ids %||% character(0)

  candidates <- .filter_palette_candidates(
    palettes      = palettes_data$palettes,
    field         = field,
    figure_type   = figure_type,
    variable_type = variable_type,
    n_groups      = n_groups,
    colorblind_safe = colorblind_safe,
    grayscale_safe  = grayscale_safe,
    preferred_ids   = preferred_ids
  )

  if (length(candidates) == 0) {
    stop(sprintf(
      "No palette found for field='%s', figure_type='%s', variable_type='%s'. ",
      field, figure_type, variable_type
    ))
  }

  palette_id <- candidates[[1]]$id
  pal        <- candidates[[1]]$data
  hex        <- unlist(pal$colors)

  if (!is.null(n_groups) && n_groups <= length(hex)) {
    hex <- hex[seq_len(n_groups)]
  }

  list(
    palette_id      = palette_id,
    hex             = hex,
    n_max           = pal$n_max,
    variable_type   = pal$variable_type,
    journal_family  = pal$journal_family,
    colorblind_safe = isTRUE(pal$colorblind_safe),
    grayscale_safe  = isTRUE(pal$grayscale_safe),
    rationale       = trimws(pal$rationale %||% ""),
    warnings        = pal$warnings %||% list()
  )
}


.filter_palette_candidates <- function(palettes, field, figure_type, variable_type,
                                       n_groups, colorblind_safe, grayscale_safe,
                                       preferred_ids) {
  scored <- list()
  for (pid in names(palettes)) {
    pal <- palettes[[pid]]

    if (!is.null(variable_type) && pal$variable_type != variable_type) next
    if (colorblind_safe && !isTRUE(pal$colorblind_safe)) next
    if (grayscale_safe && !isTRUE(pal$grayscale_safe)) next
    if (!is.null(n_groups) && n_groups > (pal$n_max %||% 999L)) next

    score <- 0L
    if (field %in% (pal$field_tags %||% character(0)))       score <- score + 10L
    if (figure_type %in% (pal$figure_tags %||% character(0))) score <- score + 5L
    if (pid %in% preferred_ids)                               score <- score + 8L

    scored <- c(scored, list(list(id = pid, data = pal, score = score)))
  }

  if (length(scored) == 0) return(list())

  scores <- vapply(scored, `[[`, 0L, "score")
  scored[order(-scores)]
}


.load_palettes_yaml <- function() {
  yaml_path <- .find_data_file("palettes.yml")
  yaml::read_yaml(yaml_path)
}

.load_field_rules <- function() {
  yaml_path <- .find_data_file("field_rules.yml")
  yaml::read_yaml(yaml_path)
}

.find_data_file <- function(filename) {
  # When installed as R package
  pkg_path <- system.file("extdata", filename, package = "pubchroma")
  if (nzchar(pkg_path)) return(pkg_path)

  # Development fallback: locate data/ relative to this file
  here <- tryCatch(
    dirname(sys.frame(1)$ofile),
    error = function(e) dirname(normalizePath("R/R/recommend.R", mustWork = FALSE))
  )
  repo_root <- dirname(dirname(here))
  file.path(repo_root, "data", filename)
}

# Null-coalescing helper (avoid purrr dependency)
`%||%` <- function(a, b) if (!is.null(a)) a else b
