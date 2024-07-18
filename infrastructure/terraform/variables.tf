variable "aws_region" {
  description = "The AWS region to deploy resources"
  default     = "us-west-1"
}

variable "s3_bucket_name" {
  description = "The name of the S3 bucket"
  default     = "your-s3-bucket"
}

variable "dynamodb_table_name" {
  description = "The name of the DynamoDB table"
  default     = "YourDynamoDBTable"
}

variable "redshift_cluster_identifier" {
  description = "The identifier for the Redshift cluster"
  default     = "example-cluster"
}

variable "athena_results_bucket" {
  description = "The name of the S3 bucket for Athena query results"
  default     = "your-query-results-bucket"
}

variable "kinesis_stream_name" {
  description = "The name of the Kinesis stream"
  default     = "example-stream"
}

variable "cloudwatch_alarm_name" {
  description = "The name of the CloudWatch alarm"
  default     = "example-alarm"
}

variable "cloudwatch_alarm_actions" {
  description = "The ARN of the CloudWatch alarm actions"
  default     = "arn:aws:sns:us-west-1:123456789012:ExampleTopic"
}

variable "ec2_instance_id" {
  description = "The ID of the EC2 instance to monitor"
  default     = "i-1234567890abcdef0"
}
