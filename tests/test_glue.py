import boto3
import unittest

class TestGlue(unittest.TestCase):
    def setUp(self):
        self.client = boto3.client('glue')
        self.crawler_name = 'example-crawler'
        self.role = 'arn:aws:iam::123456789012:role/AWSGlueServiceRole'
        self.database_name = 'example_database'
        self.s3_target = 's3://your-s3-bucket/path/to/data'
        self.job_name = 'example-job'
        self.script_location = 's3://your-script-location/script.py'
        self.temp_dir = 's3://your-temp-dir/'

    def test_create_crawler(self):
        response = self.client.create_crawler(
            Name=self.crawler_name,
            Role=self.role,
            DatabaseName=self.database_name,
            Targets={'S3Targets': [{'Path': self.s3_target}]}
        )
        self.assertEqual(response['ResponseMetadata']['HTTPStatusCode'], 200)

    def test_start_crawler(self):
        response = self.client.start_crawler(Name=self.crawler_name)
        self.assertEqual(response['ResponseMetadata']['HTTPStatusCode'], 200)

    def test_create_job(self):
        response = self.client.create_job(
            Name=self.job_name,
            Role=self.role,
            Command={'Name': 'glueetl', 'ScriptLocation': self.script_location},
            DefaultArguments={'--TempDir': self.temp_dir}
        )
        self.assertEqual(response['ResponseMetadata']['HTTPStatusCode'], 200)

    def test_start_job(self):
        response = self.client.start_job_run(JobName=self.job_name)
        self.assertEqual(response['ResponseMetadata']['HTTPStatusCode'], 200)
        self.assertTrue('JobRunId' in response)

if __name__ == '__main__':
    unittest.main()
