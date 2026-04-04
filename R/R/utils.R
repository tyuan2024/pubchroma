#' @keywords internal
"_PACKAGE"

# Internal: load palette data once
.pc_data <- NULL

.get_data <- function() {
  if (is.null(.pc_data)) {
    json_path <- system.file("extdata", "journals.json", package = "pubchroma")
    if (!nzchar(json_path)) {
      # Fallback for development (running from R/ directory)
      json_path <- file.path(
        dirname(dirname(dirname(sys.frame(1)$ofile))),
        "data", "palettes", "journals.json"
      )
    }
    .pc_data <<- jsonlite::read_json(json_path)
  }
  .pc_data
}
