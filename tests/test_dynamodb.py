import boto3
import unittest

class TestDynamoDB(unittest.TestCase):
    def setUp(self):
        self.client = boto3.client('dynamodb')
        self.table_name = 'YourDynamoDBTable'
        self.item = {
            'sensor_id': {'S': '1'},
            'timestamp': {'N': '1627883981'},
            'temperature': {'N': '25.3'},
            'humidity': {'N': '60.2'}
        }

    def test_create_table(self):
        response = self.client.create_table(
            TableName=self.table_name,
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
        self.assertEqual(response['TableDescription']['TableStatus'], 'ACTIVE')

    def test_put_item(self):
        response = self.client.put_item(
            TableName=self.table_name,
            Item=self.item
        )
        self.assertEqual(response['ResponseMetadata']['HTTPStatusCode'], 200)

    def test_get_item(self):
        response = self.client.get_item(
            TableName=self.table_name,
            Key={
                'sensor_id': {'S': '1'},
                'timestamp': {'N': '1627883981'}
            }
        )
        self.assertEqual(response['ResponseMetadata']['HTTPStatusCode'], 200)
        self.assertTrue('Item' in response)

    def test_delete_item(self):
        response = self.client.delete_item(
            TableName=self.table_name,
            Key={
                'sensor_id': {'S': '1'},
                'timestamp': {'N': '1627883981'}
            }
        )
        self.assertEqual(response['ResponseMetadata']['HTTPStatusCode'], 200)

if __name__ == '__main__':
    unittest.main()
