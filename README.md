# AWS Real-Time Data Processing and Analytics Platform

## Project Overview

**AWS Real-Time Data Processing and Analytics Platform** demonstrates how to build a robust and scalable real-time data processing and analytics platform using various AWS services. The platform collects, processes, analyzes, and visualizes streaming data from different sources, providing real-time insights and automated actions.

### Key Components

1. **Amazon Kinesis**: For collecting and processing real-time streaming data.
2. **AWS Lambda**: For serverless data processing.
3. **Amazon S3**: For storing processed data.
4. **Amazon DynamoDB**: For fast, scalable NoSQL database solutions.
5. **Amazon Redshift**: For data warehousing and complex queries.
6. **Amazon Athena**: For querying data in S3 using SQL.
7. **AWS Glue**: For ETL (Extract, Transform, Load) operations.
8. **Amazon CloudWatch**: For monitoring and logging.
9. **AWS IAM**: For managing access and security.

## Setup and Usage

### Prerequisites

- AWS CLI configured with appropriate permissions
- Python 3.x installed
- AWS SDK for Python (Boto3)
- Terraform installed (for infrastructure setup)

### Installation

1. **Clone the Repository**
    ```sh
    git clone https://github.com/your-username/AWS-Real-Time-Data-Processing.git
    cd AWS-Real-Time-Data-Processing
    ```

2. **Setup Environment**
    ```sh
    ./scripts/setup.sh
    ```

3. **Deploy Infrastructure**
    ```sh
    ./scripts/deploy.sh
    ```

### Configuration

Update the `config/config.yaml` file with your parameters and settings.

### Running the Project

1. **Start Data Producer**
    ```sh
    python kinesis/producer.py
    ```

2. **Monitor Data Processing**
    Use Amazon CloudWatch to monitor the logs and metrics.

## Project Components

### Amazon Kinesis

- **create_stream.py**: Script to create a Kinesis stream.
- **producer.py**: Script to simulate data production and send data to Kinesis.
- **consumer.py**: Script to consume data from Kinesis and process it using Lambda.

### AWS Lambda

- **processor.py**: Lambda function to process data from Kinesis.
- **deployment_package**: Contains requirements.txt and a deployment script for the Lambda function.

### Amazon S3

- **setup_s3.py**: Script to set up S3 buckets.
- **s3_operations.py**: Script to perform operations on S3 buckets (upload, download, etc.).

### Amazon DynamoDB

- **setup_dynamodb.py**: Script to set up DynamoDB tables.
- **dynamodb_operations.py**: Script to perform CRUD operations on DynamoDB tables.

### Amazon Redshift

- **setup_redshift.py**: Script to set up Redshift clusters.
- **redshift_operations.py**: Script to perform operations on Redshift (loading data, querying, etc.).

### Amazon Athena

- **setup_athena.py**: Script to set up Athena databases and tables.
- **athena_queries.py**: Script to perform queries on data stored in S3 using Athena.

### AWS Glue

- **setup_glue.py**: Script to set up Glue jobs and crawlers.
- **glue_jobs.py**: Script to define and run ETL jobs using Glue.

### Amazon CloudWatch

- **setup_cloudwatch.py**: Script to set up CloudWatch alarms and dashboards.
- **cloudwatch_alarms.py**: Script to define alarms for monitoring purposes.

## Infrastructure

### CloudFormation

- **cloudformation.yml**: CloudFormation template to provision AWS resources.

### Terraform

- **main.tf**: Terraform configuration to provision AWS resources.
- **variables.tf**: Variables for the Terraform configuration.

## Scripts

- **deploy.sh**: Script to deploy the entire infrastructure.
- **setup.sh**: Script to set up the environment.

## Testing

### Tests

- **test_kinesis.py**: Unit tests for Kinesis components.
- **test_lambda.py**: Unit tests for Lambda functions.
- **test_s3.py**: Unit tests for S3 operations.
- **test_dynamodb.py**: Unit tests for DynamoDB operations.
- **test_redshift.py**: Unit tests for Redshift operations.
- **test_athena.py**: Unit tests for Athena queries.
- **test_glue.py**: Unit tests for Glue jobs.
- **test_cloudwatch.py**: Unit tests for CloudWatch alarms.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions, reach out to [rajskashikar@vt.edu](mailto:rajskashikar@vt.edu).

---

This project demonstrates a comprehensive understanding of AWS services, showcasing the ability to design, deploy, and manage a real-time data processing and analytics platform. It highlights skills in data ingestion, processing, storage, analysis, monitoring, and security, proving expertise in AWS to any recruiter or potential employer.
