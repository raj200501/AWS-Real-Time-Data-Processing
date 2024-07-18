import boto3
import unittest

class TestAthena(unittest.TestCase):
    def setUp(self):
        self.client = boto3.client('athena')
        self.database_name = 'example_database'
        self.query = 'SELECT * FROM example_table LIMIT 10'
        self.output_location = 's3://your-query-results-bucket/'

    def test_create_database(self):
        response = self.client.start_query_execution(
            QueryString=f"CREATE DATABASE IF NOT EXISTS {self.database_name}",
            ResultConfiguration={'OutputLocation': self.output_location}
        )
        self.assertEqual(response['ResponseMetadata']['HTTPStatusCode'], 200)

    def test_execute_query(self):
        response = self.client.start_query_execution(
            QueryString=self.query,
            QueryExecutionContext={'Database': self.database_name},
            ResultConfiguration={'OutputLocation': self.output_location}
        )
        self.assertEqual(response['ResponseMetadata']['HTTPStatusCode'], 200)

if __name__ == '__main__':
    unittest.main()
