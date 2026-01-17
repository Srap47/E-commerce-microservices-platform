output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_id" {
  description = "ID of the public subnet"
  value       = aws_subnet.public.id
}

output "ecs_cluster_name" {
  description = "Name of the ECS cluster"
  value       = aws_ecs_cluster.main.name
}

output "api_gateway_invoke_url" {
  description = "API Gateway invoke URL"
  value       = try(aws_apigatewayv2_stage.main.invoke_url, "Not deployed")
}

output "lambda_function_names" {
  description = "Names of Lambda functions"
  value = {
    product_service = aws_lambda_function.product_service.function_name
    cart_service    = aws_lambda_function.cart_service.function_name
    auth_service    = aws_lambda_function.auth_service.function_name
  }
}