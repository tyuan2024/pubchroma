test_that("recommend_palette returns expected structure", {
  result <- recommend_palette("clinical", "box", n_groups = 4,
                              colorblind_safe = TRUE)
  expect_type(result, "list")
  expect_true("palette_id" %in% names(result))
  expect_true("hex" %in% names(result))
  expect_true("n_max" %in% names(result))
  expect_true("variable_type" %in% names(result))
  expect_true("colorblind_safe" %in% names(result))
  expect_true("rationale" %in% names(result))
  expect_true("warnings" %in% names(result))
})

test_that("recommend_palette returns hex colors", {
  result <- recommend_palette("clinical", "box", n_groups = 4)
  expect_type(result$hex, "character")
  expect_true(all(grepl("^#[0-9A-Fa-f]{6}$", result$hex)))
})

test_that("recommend_palette respects n_groups", {
  result <- recommend_palette("clinical", "bar", n_groups = 3)
  expect_lte(length(result$hex), 3)
})

test_that("recommend_palette colorblind_safe=TRUE returns safe palette", {
  result <- recommend_palette("clinical", "box", colorblind_safe = TRUE)
  expect_true(result$colorblind_safe)
})

test_that("recommend_palette errors on invalid field", {
  expect_error(recommend_palette("invalid_field", "box"), "field must be one of")
})

test_that("recommend_palette errors on invalid figure_type", {
  expect_error(recommend_palette("clinical", "pie"), "figure_type must be one of")
})

test_that("recommend_palette errors on invalid variable_type", {
  expect_error(recommend_palette("clinical", "box", variable_type = "nominal"),
               "variable_type must be one of")
})

test_that("recommend_palette palette_id is a string", {
  result <- recommend_palette("omics", "heatmap",
                              variable_type = "sequential")
  expect_type(result$palette_id, "character")
  expect_true(nzchar(result$palette_id))
})
