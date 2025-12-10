# AWS Lambda Function for Image Moderation using Amazon Rekognition
provider "aws" {
  region = var.aws_region
  profile = var.my_profile
}

# IAM Role for Lambda Function
resource "aws_iam_role" "lambda_role" {
    name               = "Detection_Lambda_Function_Role"
    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Action = "sts:AssumeRole"
                Principal = {
                    Service = "lambda.amazonaws.com"
                }
                Effect = "Allow"
            }
        ]
    })
}

# IAM Policy for Lambda Role
resource "aws_iam_policy" "iam_policy_for_lambda" {
    name        = "aws_iam_policy_for_terraform_aws_lambda_role"
    path        = "/"
    description = "AWS IAM Policy for lambda role"
    policy      = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Action = [
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents"
                ]
                Resource = "arn:aws:logs:*:*:*"
                Effect   = "Allow"
            }
        ]
    })
}

# Attach IAM Policy to IAM Role
resource "aws_iam_role_policy_attachment" "attach_iam_policy_to_iam_role" {
    role        = aws_iam_role.lambda_role.name
    policy_arn  = aws_iam_policy.iam_policy_for_lambda.arn
}

# Attach Amazon Rekognition ReadOnly Access Policy to IAM Role
data "aws_iam_policy" "rekognition_policy" {
  arn = "arn:aws:iam::aws:policy/AmazonRekognitionReadOnlyAccess"
}

# Attach the Rekognition policy to the Lambda role
resource "aws_iam_role_policy_attachment" "rekognition_policy_attach" {
   role        = aws_iam_role.lambda_role.name
   policy_arn = data.aws_iam_policy.rekognition_policy.arn
}

# Package Lambda Function
data "archive_file" "zip_the_python_code" {
    type        = "zip"
    source_file  = "${path.module}/../python/moderation.py"
    output_path = "${path.module}/../python/moderation.zip"
}

# Create Lambda Function
resource "aws_lambda_function" "terraform_lambda_func" {
    filename            = data.archive_file.zip_the_python_code.output_path
    function_name       = "Detection_Lambda_Function"
    role                = aws_iam_role.lambda_role.arn
    handler             = "moderation.lambda_handler"
    runtime             = "python3.12"
    timeout             = 30
    memory_size         = 256
}
