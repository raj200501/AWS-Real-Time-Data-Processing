import boto3
from botocore.exceptions import ClientError
import logging

logging.basicConfig(level=logging.INFO)

def upload_file(file_name, bucket, object_name=None):
    client = boto3.client('s3')
    try:
        if object_name is None:
            object_name = file_name
        client.upload_file(file_name, bucket, object_name)
        logging.info(f"File {file_name} uploaded to {bucket}/{object_name}.")
    except ClientError as e:
        logging.error(f"Error uploading file: {e}")

def download_file(bucket, object_name, file_name):
    client = boto3.client('s3')
    try:
        client.download_file(bucket, object_name, file_name)
        logging.info(f"File {file_name} downloaded from {bucket}/{object_name}.")
    except ClientError as e:
        logging.error(f"Error downloading file: {e}")

def list_files(bucket):
    client = boto3.client('s3')
    try:
        response = client.list_objects_v2(Bucket=bucket)
        logging.info(f"Files in {bucket}:")
        for obj in response.get('Contents', []):
            logging.info(f" - {obj['Key']}")
    except ClientError as e:
        logging.error(f"Error listing files: {e}")

def delete_file(bucket, object_name):
    client = boto3.client('s3')
    try:
        client.delete_object(Bucket=bucket, Key=object_name)
        logging.info(f"File {object_name} deleted from {bucket}.")
    except ClientError as e:
        logging.error(f"Error deleting file: {e}")

if __name__ == "__main__":
    bucket = 'your-s3-bucket'
    upload_file('example.txt', bucket)
    download_file(bucket, 'example.txt', 'downloaded_example.txt')
    list_files(bucket)
    delete_file(bucket, 'example.txt')
