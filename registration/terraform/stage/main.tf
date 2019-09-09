terraform {
  required_version = "0.12.8"
  backend "s3" {
    bucket = "terraform-backend-lah"
    key    = "registration/stage/tf_state"
    region = "us-west-2"
  }
}

provider "aws" {
  version = "2.27.0"
  profile = "default"
  region  = var.region
}

# The IAM role required for EC2 instances to communicate with ECS
# https://docs.aws.amazon.com/AmazonECS/latest/developerguide/instance_IAM_role.html
resource "aws_iam_role" "ecs_instance_role" {
  name = "ecs-instance-role"
  path = "/ecs/"
  # Specifies who may assume the role, in this case all ec2 instances
  assume_role_policy = <<EOF
  {
    "Version": "2008-10-17",
    "Statement": [
      {
        "Sid": "",
        "Effect": "Allow",
        "Principal": {
          "Service": "ec2.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
      }
    ]
  }
  EOF
}

# Attach the EC2-permission-granting policy to the role
resource "aws_iam_role_policy_attachment" "ecs_ec2_attachment" {
  role       = aws_iam_role.ecs_instance_role.id
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role"
}

# Grant Cloudwatch permissions to the role
resource "aws_iam_role_policy_attachment" "ecs_ec2_cloudwatch_attachment" {
  role       = aws_iam_role.ecs_instance_role.id
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess"
}

# Create an instance profile, a container for the role that allows EC2 instances to assume it
resource "aws_iam_instance_profile" "ecs_instance_profile" {
  name = "ecs-instance-profile"
  path = "/ecs/"
  role = aws_iam_role.ecs_instance_role.name
}

# Grab the latest ECS optimized AMZN Linux 2 AMI
data "aws_ami" "amzn_linux2_ecs" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-ecs-hvm-2.*-x86_64-ebs"]
  }

  filter {
    name   = "owner-alias"
    values = ["amazon"]
  }
}

locals {
  ecs_ec2_user_data = <<EOF
                      #!/bin/bash
                      echo ECS_CLUSTER=${var.ecs_cluster} >> /etc/ecs/ecs.config
                      EOF
}

# Template specifies how to create new EC2 instances in an auto scaling group
# Prefer launch_template over launch_configuration
# https://docs.aws.amazon.com/autoscaling/ec2/userguide/LaunchTemplates.html
resource "aws_launch_template" "ecs_launch_template" {
  name          = "ecs-launch-template"
  image_id      = data.aws_ami.amzn_linux2_ecs.id
  instance_type = "t3.micro"
  iam_instance_profile {
    arn = aws_iam_instance_profile.ecs_instance_profile.arn
  }


  block_device_mappings {
    device_name = "/dev/sda1"

    ebs {
      volume_type           = "standard"
      volume_size           = 10 # GB
      delete_on_termination = true
    }
  }

  ebs_optimized = true

  # Terminates (read: deletes) on OS-initiated shutdown
  # instance_initiated_shutdown_behavior = "terminate"

  network_interfaces {
    associate_public_ip_address = true
  }

  # TODO add ssh key
  # key_name                    = "${var.ecs_key_pair_name}"

  user_data = base64encode(local.ecs_ec2_user_data)
}

# Now make the ASG the provisions instances for the cluster
resource "aws_autoscaling_group" "ecs_autoscaling_group" {
  name             = "ecs-autoscaling-group"
  max_size         = 1
  min_size         = 1
  desired_capacity = 1
  launch_template {
    id      = aws_launch_template.ecs_launch_template.id
    version = "$Latest"
  }
  health_check_type = "EC2"
  # vpc_zone_identifier = ["${aws_subnet.test_public_sn_01.id}", "${aws_subnet.test_public_sn_02.id}"]
}

# Finally, register the ECS Cluster
resource "aws_ecs_cluster" "ecs_cluster" {
  name = var.ecs_cluster
}

# now for more fun: ECR, Task Definition, Service
