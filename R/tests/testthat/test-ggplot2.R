test_that("pubchroma_pal returns a function", {
  f <- pubchroma_pal("nature")
  expect_type(f, "closure")
})

test_that("pubchroma_pal function returns correct number of colors", {
  f <- pubchroma_pal("nature")
  expect_length(f(3), 3)
  expect_length(f(5), 5)
})

test_that("pubchroma_pal returns hex color strings", {
  f <- pubchroma_pal("nejm")
  colors <- f(4)
  expect_true(all(grepl("^#[0-9A-Fa-f]{6}$", colors)))
})

test_that("pubchroma_pal direction=-1 reverses colors", {
  fwd <- pubchroma_pal("nature", direction =  1)(5)
  rev <- pubchroma_pal("nature", direction = -1)(5)
  expect_equal(fwd, base::rev(rev))
})

test_that("pubchroma_pal errors on invalid direction", {
  expect_error(pubchroma_pal("nature", direction = 0), "direction")
})

test_that("pubchroma_pal works with colorblind palette", {
  f <- pubchroma_pal("colorblind", "okabe_ito")
  expect_length(f(4), 4)
})

skip_if_not_installed("ggplot2")

test_that("scale_color_pubchroma returns a ggplot2 Scale object", {
  s <- scale_color_pubchroma("nature")
  expect_s3_class(s, "Scale")
})

test_that("scale_fill_pubchroma returns a ggplot2 Scale object", {
  s <- scale_fill_pubchroma("jama")
  expect_s3_class(s, "Scale")
})

test_that("scale_colour_pubchroma is alias for scale_color_pubchroma", {
  expect_identical(scale_colour_pubchroma, scale_color_pubchroma)
})

test_that("scale_color_pubchroma produces correct colors in a plot", {
  library(ggplot2)
  p <- ggplot(mtcars, aes(wt, mpg, colour = factor(cyl))) +
    geom_point() +
    scale_color_pubchroma("nejm")
  built <- ggplot_build(p)
  plot_colors <- unique(built$data[[1]]$colour)
  nejm_colors <- get_colors("nejm", n = 3)
  expect_true(all(plot_colors %in% nejm_colors))
})

test_that("scale_fill_pubchroma produces correct colors in a plot", {
  library(ggplot2)
  p <- ggplot(mtcars, aes(factor(cyl), fill = factor(cyl))) +
    geom_bar() +
    scale_fill_pubchroma("jama")
  built <- ggplot_build(p)
  plot_colors <- unique(built$data[[1]]$fill)
  jama_colors <- get_colors("jama", n = 3)
  expect_true(all(plot_colors %in% jama_colors))
})

test_that("direction=-1 reverses colors in scale", {
  library(ggplot2)
  p_fwd <- ggplot(mtcars, aes(wt, mpg, colour = factor(cyl))) +
    geom_point() + scale_color_pubchroma("nature", direction =  1)
  p_rev <- ggplot(mtcars, aes(wt, mpg, colour = factor(cyl))) +
    geom_point() + scale_color_pubchroma("nature", direction = -1)
  colors_fwd <- unique(ggplot_build(p_fwd)$data[[1]]$colour)
  colors_rev <- unique(ggplot_build(p_rev)$data[[1]]$colour)
  expect_false(identical(colors_fwd, colors_rev))
})
