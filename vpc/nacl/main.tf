# Create a VPC
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name        = "example-vpc"
    Environment = "example"
  }
}

# Create a Network ACL (NACL) attached to the VPC
resource "aws_network_acl" "example_nacl" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name        = var.nacl_name
    Environment = "example"
  }
}

# Inbound rule: Allow all inbound HTTP traffic (port 80)
resource "aws_network_acl_rule" "allow_http_inbound" {
  network_acl_id = aws_network_acl.example_nacl.id
  rule_number    = 100
  egress        = false
  protocol      = "6"           # TCP protocol number
  rule_action   = "allow"
  cidr_block    = "0.0.0.0/0"
  from_port     = 80
  to_port       = 80
}

# Outbound rule: Allow all outbound HTTP traffic (port 80)
resource "aws_network_acl_rule" "allow_http_outbound" {
  network_acl_id = aws_network_acl.example_nacl.id
  rule_number    = 100
  egress        = true
  protocol      = "6"           # TCP protocol number
  rule_action   = "allow"
  cidr_block    = "0.0.0.0/0"
  from_port     = 80
  to_port       = 80
}

# Deny all other inbound traffic by default (implicit deny in AWS NACLs)
# Similarly, deny other outbound traffic by default.
