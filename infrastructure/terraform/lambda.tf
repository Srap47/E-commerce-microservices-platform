# Lambda resources for microservices

# Product Service Lambda
resource "aws_lambda_function" "product_service" {
  filename      = "product_service.zip"
  function_name = "ecommerce-product-service"
  role          = aws_iam_role.lambda_role.arn
  handler       = "app.main.handler"
  runtime       = "python3.11"
  timeout       = 60

  environment {
    variables = {
      ENVIRONMENT = "production"
    }
  }
}

# Cart Service Lambda
resource "aws_lambda_function" "cart_service" {
  filename      = "cart_service.zip"
  function_name = "ecommerce-cart-service"
  role          = aws_iam_role.lambda_role.arn
  handler       = "app.main.handler"
  runtime       = "python3.11"
  timeout       = 60

  environment {
    variables = {
      ENVIRONMENT = "production"
    }
  }
}

# Auth Service Lambda
resource "aws_lambda_function" "auth_service" {
  filename      = "auth_service.zip"
  function_name = "ecommerce-auth-service"
  role          = aws_iam_role.lambda_role.arn
  handler       = "app.main.handler"
  runtime       = "python3.11"
  timeout       = 60

  environment {
    variables = {
      ENVIRONMENT = "production"
      SECRET_KEY  = var.jwt_secret_key
    }
  }
}

output "product_service_arn" {
  value = aws_lambda_function.product_service.arn
}

output "cart_service_arn" {
  value = aws_lambda_function.cart_service.arn
}

output "auth_service_arn" {
  value = aws_lambda_function.auth_service.arn
}
