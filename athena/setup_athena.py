import boto3
from botocore.exceptions import ClientError
import logging

logging.basicConfig(level=logging.INFO)

def create_database(database_name):
    client = boto3.client('athena')
    query = f"CREATE DATABASE IF NOT EXISTS {database_name}"
    try:
        response = client.start_query_execution(
            QueryString=query,
            ResultConfiguration={
                'OutputLocation': 's3://your-query-results-bucket/'
            }
        )
        logging.info(f"Database {database_name} created successfully.")
    except ClientError as e:
        logging.error(f"Error creating database: {e}")

def create_table(database_name, table_name, s3_location):
    client = boto3.client('athena')
    query = f"""
    CREATE EXTERNAL TABLE IF NOT EXISTS {database_name}.{table_name} (
        sensor_id STRING,
        temperature DOUBLE,
        humidity DOUBLE,
        timestamp BIGINT
    )
    ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
    WITH SERDEPROPERTIES (
        'serialization.format' = '1'
    )
    LOCATION 's3://{s3_location}/';
    """
    try:
        response = client.start_query_execution(
            QueryString=query,
            ResultConfiguration={
                'OutputLocation': 's3://your-query-results-bucket/'
            }
        )
        logging.info(f"Table {table_name} created in database {database_name} successfully.")
    except ClientError as e:
        logging.error(f"Error creating table: {e}")

if __name__ == "__main__":
    database_name = 'example_database'
    table_name = 'example_table'
    s3_location = 'your-s3-bucket/path/to/data'
    
    create_database(database_name)
    create_table(database_name, table_name, s3_location)
