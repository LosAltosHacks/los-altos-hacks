variable "ecs_cluster" {
  description = "ECS cluster name"
  default     = "stage-registration"
}

# variable "ecs_key_pair_name" {
#   description = "EC2 instance key pair name"
# }

variable "region" {
  description = "AWS region"
  default     = "us-west-2"
}

variable "availability_zone" {
  description = "availability zone used for the demo, based on region"
  default = {
    us-west-2 = "us-west-2a"
  }
}
