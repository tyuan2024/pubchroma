test_that("list_journals returns sorted character vector", {
  result <- list_journals()
  expect_type(result, "character")
  expect_true("nature" %in% result)
  expect_true("science" %in% result)
  expect_true("cell" %in% result)
  expect_equal(result, sort(result))
})

test_that("list_palettes returns palettes for known journal", {
  result <- list_palettes("nature")
  expect_true("main" %in% result)
})

test_that("list_palettes is case insensitive", {
  expect_equal(list_palettes("Nature"), list_palettes("nature"))
})

test_that("list_palettes errors on unknown journal", {
  expect_error(list_palettes("nonexistent"), "not found")
})

test_that("get_palette returns list with required fields", {
  p <- get_palette("nature")
  expect_type(p, "list")
  expect_true("colors" %in% names(p))
  expect_true("colorblind_safe" %in% names(p))
  expect_true("description" %in% names(p))
})

test_that("get_palette colors are hex strings", {
  p <- get_palette("nature")
  colors <- unlist(p$colors)
  expect_true(all(grepl("^#[0-9A-Fa-f]{6}$", colors)))
})

test_that("get_palette errors on unknown journal", {
  expect_error(get_palette("nonexistent"), "not found")
})

test_that("get_palette errors on unknown palette", {
  expect_error(get_palette("nature", "nonexistent"), "not found")
})

test_that("get_colors returns character vector", {
  colors <- get_colors("nature")
  expect_type(colors, "character")
  expect_true(length(colors) > 0)
})

test_that("get_colors n parameter limits output", {
  colors <- get_colors("nature", n = 3)
  expect_length(colors, 3)
})

test_that("get_colors cycles when n exceeds palette", {
  colors <- get_colors("nature", n = 12)
  expect_length(colors, 12)
})

test_that("get_colors colorblind_only=TRUE works on safe palette", {
  colors <- get_colors("colorblind", "okabe_ito", colorblind_only = TRUE)
  expect_true(length(colors) > 0)
})

test_that("get_colors colorblind_only=TRUE errors on unsafe palette", {
  expect_error(get_colors("science", colorblind_only = TRUE), "not colorblind-safe")
})

test_that("is_colorblind_safe returns TRUE for nature main", {
  expect_true(is_colorblind_safe("nature"))
})

test_that("is_colorblind_safe returns FALSE for science main", {
  expect_false(is_colorblind_safe("science"))
})

test_that("list_colorblind_safe returns data frame with required columns", {
  result <- list_colorblind_safe()
  expect_s3_class(result, "data.frame")
  expect_true("journal" %in% names(result))
  expect_true("palette" %in% names(result))
  expect_true("n_colors" %in% names(result))
  expect_true(nrow(result) > 0)
})
