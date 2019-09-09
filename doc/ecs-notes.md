# The Mystery of adding compute to an ECS cluster, finally solved

To launch something on ECS, create a service
A service references a task definition and also specifies the cluster to run on
Add EC2 to a cluster via an ASG, where each compute instane is setup with the proper AMI and ECS container agent configuration
