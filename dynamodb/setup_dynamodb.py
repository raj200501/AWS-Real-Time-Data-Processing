import boto3
from botocore.exceptions import ClientError
import logging

logging.basicConfig(level=logging.INFO)

def create_table(table_name):
    client = boto3.client('dynamodb')
    try:
        response = client.create_table(
            TableName=table_name,
            KeySchema=[
                {'AttributeName': 'sensor_id', 'KeyType': 'HASH'},
                {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'sensor_id', 'AttributeType': 'S'},
                {'AttributeName': 'timestamp', 'AttributeType': 'N'}
            ],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        logging.info(f"Table {table_name} created successfully.")
    except ClientError as e:
        logging.error(f"Error creating table: {e}")
        return None

    # Wait for the table to become active
    while True:
        try:
            response = client.describe_table(TableName=table_name)
            status = response['Table']['TableStatus']
            if status == 'ACTIVE':
                logging.info(f"Table {table_name} is now active.")
                break
            time.sleep(1)
        except ClientError as e:
            logging.error(f"Error describing table: {e}")
            return None

    return response

def delete_table(table_name):
    client = boto3.client('dynamodb')
    try:
        client.delete_table(TableName=table_name)
        logging.info(f"Table {table_name} deleted successfully.")
    except ClientError as e:
        logging.error(f"Error deleting table: {e}")

def list_tables():
    client = boto3.client('dynamodb')
    try:
        response = client.list_tables()
        tables = response['TableNames']
        logging.info("DynamoDB tables:")
        for table in tables:
            logging.info(f" - {table}")
    except ClientError as e:
        logging.error(f"Error listing tables: {e}")

if __name__ == "__main__":
    table_name = 'YourDynamoDBTable'
    create_table(table_name)
    list_tables()
    # Uncomment to delete the table
    # delete_table(table_name)
