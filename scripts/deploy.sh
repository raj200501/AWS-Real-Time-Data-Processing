#!/bin/bash

set -e

echo "Deploying AWS Real-Time Data Processing and Analytics Platform..."

# Initialize Terraform
cd infrastructure/terraform
terraform init

# Apply Terraform configuration
terraform apply -auto-approve

# Deploy Lambda function
cd ../../lambda/deployment_package
zip -r processor.zip .
aws lambda update-function-code --function-name example-processor --zip-file fileb://processor.zip

echo "Deployment complete!"
