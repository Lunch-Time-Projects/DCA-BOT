resource "aws_lambda_layer_version" "lambda_layer" {
  layer_name          = "lambda_layer"
  filename            = data.archive_file.layer_zip.output_path
  source_code_hash    = data.archive_file.layer_zip.output_base64sha256
  compatible_runtimes = ["python3.8"]
}

resource "aws_lambda_function" "lambda_function" {
  function_name    = "lambda_function"
  filename         = data.archive_file.function_zip.output_path
  handler          = "lambda_function.lambda_handler"
  role             = aws_iam_role.lambda_exec.arn
  runtime          = "python3.8"
  source_code_hash = data.archive_file.function_zip.output_base64sha256
  layers           = [aws_lambda_layer_version.lambda_layer.arn]

  environment {
    variables = {
      secret = var.bitflyer_secret
      key    = var.bitflyer_key
    }
  }
}

resource "aws_iam_role" "lambda_exec" {
  name               = "lambda_role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_cloudwatch_log_group" "lambda_log_group" {
  name              = "/aws/lambda/${aws_lambda_function.lambda_function.function_name}"
  retention_in_days = 14
}

resource "aws_iam_policy" "lambda_logging" {
  name   = "lambda_logging"
  path   = "/"
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*",
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "lambda_logging_attachment" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = aws_iam_policy.lambda_logging.arn
}

resource "aws_cloudwatch_event_rule" "cloudwatch_rules" {
  for_each            = var.dca_bot_config
  name                = "${each.key}_cloudwatch_rule"
  description         = "${each.key} CloudWatch Rule"
  schedule_expression = each.value.schedule_expression
  is_enabled          = false # Manually enable in AWS Console
}

resource "aws_cloudwatch_event_target" "cloudwatch_targets" {
  for_each  = var.dca_bot_config
  rule      = "${each.key}_cloudwatch_rule"
  target_id = "lambda_function"
  arn       = aws_lambda_function.lambda_function.arn
  input     = jsonencode(each.value.input)
}

resource "aws_lambda_permission" "cloudwatch_to_lambda_permissions" {
  for_each      = var.dca_bot_config
  statement_id  = "${each.key}_cloudwatch_to_lambda_permission"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_function.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.cloudwatch_rules[each.key].arn
}
