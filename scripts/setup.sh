#!/bin/bash

set -e

echo "Setting up AWS Real-Time Data Processing and Analytics Platform..."

# Install dependencies
pip install -r lambda/deployment_package/requirements.txt

# Create necessary S3 buckets
python s3/setup_s3.py

# Create DynamoDB tables
python dynamodb/setup_dynamodb.py

# Create and start Glue crawlers and jobs
python glue/setup_glue.py

echo "Setup complete!"
