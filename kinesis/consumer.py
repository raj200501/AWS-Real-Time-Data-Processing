import boto3
import json
import time
import logging

logging.basicConfig(level=logging.INFO)

def get_records(stream_name, shard_id, iterator_type='TRIM_HORIZON'):
    client = boto3.client('kinesis')
    shard_iterator = client.get_shard_iterator(
        StreamName=stream_name,
        ShardId=shard_id,
        ShardIteratorType=iterator_type
    )['ShardIterator']

    while True:
        response = client.get_records(ShardIterator=shard_iterator, Limit=100)
        records = response.get('Records', [])
        if records:
            for record in records:
                data = json.loads(record['Data'])
                logging.info(f"Data received: {data}")
        shard_iterator = response['NextShardIterator']
        time.sleep(1)

if __name__ == "__main__":
    stream_name = 'example-stream'
    shard_id = 'shardId-000000000000'
    get_records(stream_name, shard_id)
