#' @keywords internal
#' @importFrom jsonlite read_json
"_PACKAGE"

# Internal: cache environment to avoid locked-binding issues under R CMD check
.pc_cache <- new.env(parent = emptyenv())

# Null-coalescing helper (avoid purrr dependency)
`%||%` <- function(a, b) if (!is.null(a)) a else b

.get_data <- function() {
  if (is.null(.pc_cache$data)) {
    json_path <- system.file("extdata", "journals.json", package = "pubchroma")
    if (!nzchar(json_path)) {
      json_path <- file.path(
        dirname(dirname(dirname(sys.frame(1)$ofile))),
        "data", "palettes", "journals.json"
      )
    }
    .pc_cache$data <- jsonlite::read_json(json_path)
  }
  .pc_cache$data
}
