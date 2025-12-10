# DNS: Point moderation.juanca.online → API Gateway

# Get Route 53 Hosted Zone
data "aws_route53_zone" "main_zone" {
  name         = "juanca.online." # Add your domain name here. Make sure to include the trailing dot
  private_zone = false
}

# Create A Record for moderation.juanca.online
resource "aws_route53_record" "moderation_record" {
  zone_id = data.aws_route53_zone.main_zone.zone_id
  name    = "moderation"
  type    = "A" # Alias record

  alias {
    name                   = aws_api_gateway_domain_name.moderation_domain.regional_domain_name
    zone_id                = aws_api_gateway_domain_name.moderation_domain.regional_zone_id
    evaluate_target_health = false
  }
}