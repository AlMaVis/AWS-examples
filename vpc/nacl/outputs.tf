output "vpc_id" {
  description = "ID of the created VPC"
  value       = aws_vpc.main.id
}

output "nacl_id" {
  description = "ID of the created Network ACL"
  value       = aws_network_acl.example_nacl.id
}
