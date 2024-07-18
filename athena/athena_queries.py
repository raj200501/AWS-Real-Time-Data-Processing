import boto3
from botocore.exceptions import ClientError
import logging

logging.basicConfig(level=logging.INFO)

def execute_query(database_name, query):
    client = boto3.client('athena')
    try:
        response = client.start_query_execution(
            QueryString=query,
            QueryExecutionContext={'Database': database_name},
            ResultConfiguration={'OutputLocation': 's3://your-query-results-bucket/'}
        )
        query_execution_id = response['QueryExecutionId']
        logging.info(f"Query started with execution ID: {query_execution_id}")
        
        # Wait for the query to complete
        while True:
            query_status = client.get_query_execution(QueryExecutionId=query_execution_id)['QueryExecution']['Status']['State']
            if query_status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
                break
            time.sleep(2)
        
        if query_status == 'SUCCEEDED':
            results = client.get_query_results(QueryExecutionId=query_execution_id)
            for row in results['ResultSet']['Rows']:
                logging.info(row['Data'])
        else:
            logging.error(f"Query failed with status: {query_status}")
    except ClientError as e:
        logging.error(f"Error executing query: {e}")

if __name__ == "__main__":
    database_name = 'example_database'
    query = 'SELECT * FROM example_table LIMIT 10'
    
    execute_query(database_name, query)
