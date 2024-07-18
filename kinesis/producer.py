import boto3
import json
import time
import random
import logging

logging.basicConfig(level=logging.INFO)

def send_data(stream_name, data, partition_key):
    client = boto3.client('kinesis')
    try:
        response = client.put_record(
            StreamName=stream_name,
            Data=json.dumps(data),
            PartitionKey=partition_key
        )
        logging.info(f"Data sent: {data}")
    except Exception as e:
        logging.error(f"Error sending data: {e}")
        return None
    return response

def generate_random_data():
    return {
        'sensor_id': random.randint(1, 100),
        'temperature': round(random.uniform(20.0, 30.0), 2),
        'humidity': round(random.uniform(30.0, 70.0), 2),
        'timestamp': int(time.time())
    }

if __name__ == "__main__":
    stream_name = 'example-stream'
    partition_key = 'partitionkey'

    while True:
        data = generate_random_data()
        send_data(stream_name, data, partition_key)
        time.sleep(1)
