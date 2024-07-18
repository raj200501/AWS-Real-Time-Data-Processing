provider "aws" {
  region = var.aws_region
}

# S3 Bucket
resource "aws_s3_bucket" "example_bucket" {
  bucket = var.s3_bucket_name
  acl    = "private"
}

# DynamoDB Table
resource "aws_dynamodb_table" "example_table" {
  name         = var.dynamodb_table_name
  hash_key     = "sensor_id"
  range_key    = "timestamp"
  read_capacity  = 5
  write_capacity = 5

  attribute {
    name = "sensor_id"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "N"
  }
}

# Redshift Cluster
resource "aws_redshift_cluster" "example_cluster" {
  cluster_identifier = var.redshift_cluster_identifier
  database_name      = "exampledb"
  master_username    = "admin"
  master_password    = "Password123!"
  node_type          = "dc2.large"
  cluster_type       = "single-node"
}

# Athena S3 Bucket for Query Results
resource "aws_s3_bucket" "athena_results_bucket" {
  bucket = var.athena_results_bucket
  acl    = "private"
}

# Glue Service Role
resource "aws_iam_role" "glue_service_role" {
  name = "AWSGlueServiceRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "glue.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })

  inline_policy {
    name = "AWSGlueServicePolicy"
    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [{
        Effect = "Allow"
        Action = ["s3:*", "glue:*"]
        Resource = "*"
      }]
    })
  }
}

# Kinesis Stream
resource "aws_kinesis_stream" "example_stream" {
  name        = var.kinesis_stream_name
  shard_count = 1
}

# Lambda Execution Role
resource "aws_iam_role" "lambda_execution_role" {
  name = "LambdaExecutionRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })

  inline_policy {
    name = "LambdaExecutionPolicy"
    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [{
        Effect = "Allow"
        Action = ["logs:*", "s3:*", "dynamodb:*", "kinesis:*"]
        Resource = "*"
      }]
    })
  }
}

# CloudWatch Alarm
resource "aws_cloudwatch_metric_alarm" "example_alarm" {
  alarm_name                = var.cloudwatch_alarm_name
  comparison_operator       = "GreaterThanThreshold"
  evaluation_periods        = 2
  metric_name               = "CPUUtilization"
  namespace                 = "AWS/EC2"
  period                    = 120
  statistic                 = "Average"
  threshold                 = 70
  alarm_description         = "This metric monitors the CPU utilization of the EC2 instance"
  actions_enabled           = true
  alarm_actions             = [var.cloudwatch_alarm_actions]
  insufficient_data_actions = [var.cloudwatch_alarm_actions]
  ok_actions                = [var.cloudwatch_alarm_actions]
  dimensions = {
    InstanceId = var.ec2_instance_id
  }
}
