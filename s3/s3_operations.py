import boto3
from botocore.exceptions import ClientError

def upload_file(file_name, bucket, object_name=None):
    client = boto3.client('s3')
    try:
        if object_name is None:
            object_name = file_name
        client.upload_file(file_name, bucket, object_name)
        print(f"File {file_name} uploaded to {bucket}/{object_name}.")
    except ClientError as e:
        print(f"Error uploading file: {e}")

def download_file(bucket, object_name, file_name):
    client = boto3.client('s3')
    try:
        client.download_file(bucket, object_name, file_name)
        print(f"File {file_name} downloaded from {bucket}/{object_name}.")
    except ClientError as e:
        print(f"Error downloading file: {e}")

if __name__ == "__main__":
    bucket = 'your-s3-bucket'
    upload_file('example.txt', bucket)
    download_file(bucket, 'example.txt', 'downloaded_example.txt')
