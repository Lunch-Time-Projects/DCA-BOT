data "archive_file" "layer_zip" {
  type        = "zip"
  source_dir  = "../build/layer"
  output_path = "lambda/layer.zip"
}

data "archive_file" "function_zip" {
  type        = "zip"
  source_dir  = "../build/function"
  output_path = "lambda/function.zip"
}
