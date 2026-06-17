provider "aws" { region = "us-east-1" }
resource "aws_eks_cluster" "world_sim" { name = "world-sim-cluster" }