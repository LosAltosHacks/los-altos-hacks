terraform {
  required_version = "0.12.8"
  backend "s3" {
    bucket = "terraform-backend-lah"
    key    = "registration/tf_state"
    region = "us-west-2"
  }
}

variable "region" {
  default = "us-west-2"
}

variable "amis" {
  default = {
    us-west-2 = "ami-082b5a644766e0e6f"
  }
}

provider "aws" {
  version = "2.27.0"
  profile = "default"
  region  = var.region
}

# resource "aws_instance" "example" {
#   ami           = var.amis[var.region]
#   instance_type = "t2.micro"
# }
