import boto3
from botocore.exceptions import ClientError
import time

def create_stream(stream_name, shard_count):
    client = boto3.client('kinesis')
    try:
        response = client.create_stream(
            StreamName=stream_name,
            ShardCount=shard_count
        )
        print(f"Stream {stream_name} created successfully.")
    except ClientError as e:
        print(f"Error creating stream: {e}")
        return None

    # Wait for the stream to become active
    while True:
        try:
            response = client.describe_stream(StreamName=stream_name)
            status = response['StreamDescription']['StreamStatus']
            if status == 'ACTIVE':
                print(f"Stream {stream_name} is now active.")
                break
            time.sleep(1)
        except ClientError as e:
            print(f"Error describing stream: {e}")
            return None

    return response

def delete_stream(stream_name):
    client = boto3.client('kinesis')
    try:
        client.delete_stream(StreamName=stream_name, EnforceConsumerDeletion=True)
        print(f"Stream {stream_name} deleted successfully.")
    except ClientError as e:
        print(f"Error deleting stream: {e}")

if __name__ == "__main__":
    stream_name = 'example-stream'
    shard_count = 1
    create_stream(stream_name, shard_count)
    # Uncomment to delete the stream
    # delete_stream(stream_name)
