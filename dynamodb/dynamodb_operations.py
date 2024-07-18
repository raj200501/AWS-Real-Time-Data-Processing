import boto3
from botocore.exceptions import ClientError
import logging

logging.basicConfig(level=logging.INFO)

def put_item(table_name, item):
    client = boto3.client('dynamodb')
    try:
        response = client.put_item(
            TableName=table_name,
            Item=item
        )
        logging.info(f"Item {item} put into table {table_name}.")
    except ClientError as e:
        logging.error(f"Error putting item into table: {e}")

def get_item(table_name, key):
    client = boto3.client('dynamodb')
    try:
        response = client.get_item(
            TableName=table_name,
            Key=key
        )
        item = response.get('Item', None)
        logging.info(f"Item retrieved: {item}")
        return item
    except ClientError as e:
        logging.error(f"Error getting item from table: {e}")
        return None

def delete_item(table_name, key):
    client = boto3.client('dynamodb')
    try:
        response = client.delete_item(
            TableName=table_name,
            Key=key
        )
        logging.info(f"Item with key {key} deleted from table {table_name}.")
    except ClientError as e:
        logging.error(f"Error deleting item from table: {e}")

def scan_table(table_name):
    client = boto3.client('dynamodb')
    try:
        response = client.scan(TableName=table_name)
        items = response.get('Items', [])
        logging.info(f"Items in table {table_name}:")
        for item in items:
            logging.info(item)
    except ClientError as e:
        logging.error(f"Error scanning table: {e}")

if __name__ == "__main__":
    table_name = 'YourDynamoDBTable'
    item = {
        'sensor_id': {'S': '1'},
        'timestamp': {'N': '1627883981'},
        'temperature': {'N': '25.3'},
        'humidity': {'N': '60.2'}
    }
    key = {
        'sensor_id': {'S': '1'},
        'timestamp': {'N': '1627883981'}
    }

    put_item(table_name, item)
    get_item(table_name, key)
    scan_table(table_name)
    delete_item(table_name, key)
