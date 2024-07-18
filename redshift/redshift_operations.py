import boto3
from botocore.exceptions import ClientError
import logging

logging.basicConfig(level=logging.INFO)

def load_data_from_s3(cluster_id, db_name, table_name, s3_bucket, s3_key, iam_role):
    client = boto3.client('redshift-data')
    query = f"""
    COPY {table_name}
    FROM 's3://{s3_bucket}/{s3_key}'
    IAM_ROLE '{iam_role}'
    FORMAT AS JSON 'auto';
    """
    try:
        response = client.execute_statement(
            ClusterIdentifier=cluster_id,
            Database=db_name,
            DbUser='awsuser',
            Sql=query
        )
        logging.info(f"Data loaded into {table_name} from s3://{s3_bucket}/{s3_key}.")
    except ClientError as e:
        logging.error(f"Error loading data from S3: {e}")

def query_data(cluster_id, db_name, query):
    client = boto3.client('redshift-data')
    try:
        response = client.execute_statement(
            ClusterIdentifier=cluster_id,
            Database=db_name,
            DbUser='awsuser',
            Sql=query
        )
        result_id = response['Id']
        while True:
            result_response = client.describe_statement(Id=result_id)
            if result_response['Status'] == 'FINISHED':
                results = client.get_statement_result(Id=result_id)
                for row in results['Records']:
                    logging.info(row)
                break
            elif result_response['Status'] == 'FAILED':
                logging.error(f"Query failed: {result_response['Error']}")
                break
            time.sleep(2)
    except ClientError as e:
        logging.error(f"Error querying data: {e}")

if __name__ == "__main__":
    cluster_id = 'example-cluster'
    db_name = 'exampledb'
    table_name = 'example_table'
    s3_bucket = 'your-s3-bucket'
    s3_key = 'data/example_data.json'
    iam_role = 'arn:aws:iam::123456789012:role/RedshiftCopyUnload'
    
    load_data_from_s3(cluster_id, db_name, table_name, s3_bucket, s3_key, iam_role)
    query_data(cluster_id, db_name, f"SELECT * FROM {table_name} LIMIT 10")
