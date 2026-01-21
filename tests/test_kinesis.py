import boto3
import unittest


class TestKinesis(unittest.TestCase):
    def setUp(self):
        self.client = boto3.client("kinesis")
        self.stream_name = "example-stream"
        self.partition_key = "partitionkey"

    def test_create_stream(self):
        response = self.client.create_stream(StreamName=self.stream_name, ShardCount=1)
        self.assertEqual(response["ResponseMetadata"]["HTTPStatusCode"], 200)

    def test_put_record(self):
        response = self.client.put_record(
            StreamName=self.stream_name,
            Data='{"sensor_id":1,"temperature":25.3,"humidity":60.2,"timestamp":1627883981}',
            PartitionKey=self.partition_key,
        )
        self.assertEqual(response["ResponseMetadata"]["HTTPStatusCode"], 200)

    def test_get_records(self):
        shard_iterator = self.client.get_shard_iterator(
            StreamName=self.stream_name,
            ShardId="shardId-000000000000",
            ShardIteratorType="TRIM_HORIZON",
        )["ShardIterator"]

        response = self.client.get_records(ShardIterator=shard_iterator, Limit=1)
        self.assertEqual(response["ResponseMetadata"]["HTTPStatusCode"], 200)
        self.assertTrue("Records" in response)


if __name__ == "__main__":
    unittest.main()
