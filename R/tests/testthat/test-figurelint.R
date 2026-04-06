test_that("lint_figure_spec returns expected structure", {
  spec <- list(
    field = "clinical", figure_type = "box", variable_type = "categorical",
    palette_name = "clinical_categorical_conservative_4",
    font_size_pt = 8, dpi = 600, width_mm = 89
  )
  report <- lint_figure_spec(spec)
  expect_type(report, "list")
  expect_true("errors" %in% names(report))
  expect_true("warnings" %in% names(report))
  expect_true("suggestions" %in% names(report))
  expect_true("score" %in% names(report))
  expect_true("summary" %in% names(report))
})

test_that("lint_figure_spec clean spec scores 100", {
  spec <- list(
    field = "clinical", figure_type = "box", variable_type = "categorical",
    palette_name = "clinical_categorical_conservative_4",
    font_size_pt = 10, dpi = 600, width_mm = 89
  )
  report <- lint_figure_spec(spec)
  expect_equal(report$score, 100L)
  expect_equal(report$summary, "No issues found.")
})

test_that("lint_figure_spec errors on missing required fields", {
  expect_error(lint_figure_spec(list(field = "clinical")),
               "Required spec fields missing")
})

test_that("lint_figure_spec detects rainbow palette", {
  spec <- list(field = "clinical", figure_type = "bar",
               variable_type = "categorical", palette_name = "rainbow")
  report <- lint_figure_spec(spec)
  expect_true(any(vapply(report$errors, function(x) x$rule == "rainbow_palette_detected", logical(1))))
})

test_that("lint_figure_spec detects low DPI", {
  spec <- list(field = "clinical", figure_type = "box",
               variable_type = "categorical", dpi = 150)
  report <- lint_figure_spec(spec)
  expect_true(any(vapply(report$errors, function(x) x$rule == "dpi_below_minimum", logical(1))))
})

test_that("lint_figure_spec detects small font", {
  spec <- list(field = "clinical", figure_type = "box",
               variable_type = "categorical", font_size_pt = 4)
  report <- lint_figure_spec(spec)
  expect_true(any(vapply(report$errors, function(x) x$rule == "font_size_too_small", logical(1))))
})

test_that("lint_figure_spec detects narrow figure", {
  spec <- list(field = "clinical", figure_type = "box",
               variable_type = "categorical", width_mm = 50)
  report <- lint_figure_spec(spec)
  expect_true(any(vapply(report$warnings, function(x) x$rule == "figure_width_too_small", logical(1))))
})

test_that("lint_figure_spec score decreases with issues", {
  spec_ok <- list(field = "clinical", figure_type = "box",
                  variable_type = "categorical")
  spec_bad <- list(field = "clinical", figure_type = "box",
                   variable_type = "categorical", dpi = 72, font_size_pt = 3)
  expect_gt(lint_figure_spec(spec_ok)$score, lint_figure_spec(spec_bad)$score)
})
