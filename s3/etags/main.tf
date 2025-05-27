# ref https://registry.terraform.io/providers.hashicorp/aws/latest
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "6.0.0-beta2"
    }
  }
}

provider "aws" {
  # Configuration options
}

resource "aws_s3_bucket" "default" {
}

resource "aws_s3_object" "object" {
    bucket = aws_s3_bucket.default.id
    key    = "myfile.txt"
    source = "myfile.txt"
    etag   = filemd5("myfile.txt")
    # The etag is the MD5 hash of the file content, used for integrity checks.
    # Note: The etag is automatically calculated by AWS S3 when the object is uploaded.
    # Terraform can detect changes to the file and update the etag accordingly.
}