# Terraform Variables
variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "my_profile" {
  description = "AWS CLI profile to use"
  type        = string
  default     = "alice"
}

variable "acm_certificate_arn" {
  description = "ARN of the ACM certificate for moderation.juanca.online"
  type        = string
}
