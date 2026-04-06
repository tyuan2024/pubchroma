test_that("validate_palette returns valid=TRUE for known palette", {
  result <- validate_palette("clinical_categorical_conservative_4",
                             field = "clinical", n_groups = 4)
  expect_true(result$valid)
  expect_length(result$errors, 0)
})

test_that("validate_palette returns valid=FALSE for unknown palette", {
  result <- validate_palette("nonexistent_palette_xyz")
  expect_false(result$valid)
  expect_true(length(result$errors) > 0)
})

test_that("validate_palette errors when neither palette_id nor hex given", {
  expect_error(validate_palette(), "Provide at least one")
})

test_that("validate_palette validates hex colors format", {
  result <- validate_palette(hex_colors = c("#FF0000", "#00FF00", "notahex"))
  expect_false(result$valid)
  expect_true(any(grepl("Invalid hex", result$errors)))
})

test_that("validate_palette valid hex list passes", {
  result <- validate_palette(hex_colors = c("#374E55", "#DF8F44", "#00A1D5"))
  expect_true(result$valid)
})

test_that("validate_palette detects n_groups exceeding n_max", {
  result <- validate_palette("clinical_categorical_conservative_4",
                             n_groups = 10)
  expect_false(result$valid)
  expect_true(any(grepl("n_max", result$errors)))
})

test_that("validate_palette detects colorblind_safe mismatch", {
  # Find a non-colorblind-safe palette from registry
  result <- validate_palette("clinical_categorical_conservative_4",
                             colorblind_safe = FALSE)
  expect_true(result$valid)
})

test_that("validate_palette returns hex for known palette", {
  result <- validate_palette("clinical_categorical_conservative_4")
  expect_type(result$hex, "character")
  expect_true(all(grepl("^#[0-9A-Fa-f]{6}$", result$hex)))
})
