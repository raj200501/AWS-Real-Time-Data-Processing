import boto3
import unittest


class TestS3(unittest.TestCase):
    def setUp(self):
        self.client = boto3.client("s3")
        self.bucket_name = "your-s3-bucket"

    def test_create_bucket(self):
        response = self.client.create_bucket(Bucket=self.bucket_name)
        self.assertEqual(response["ResponseMetadata"]["HTTPStatusCode"], 200)

    def test_put_object(self):
        response = self.client.put_object(
            Bucket=self.bucket_name, Key="test.txt", Body="This is a test object."
        )
        self.assertEqual(response["ResponseMetadata"]["HTTPStatusCode"], 200)

    def test_get_object(self):
        response = self.client.get_object(Bucket=self.bucket_name, Key="test.txt")
        self.assertEqual(response["ResponseMetadata"]["HTTPStatusCode"], 200)
        self.assertEqual(
            response["Body"].read().decode("utf-8"), "This is a test object."
        )

    def test_delete_object(self):
        response = self.client.delete_object(Bucket=self.bucket_name, Key="test.txt")
        self.assertEqual(response["ResponseMetadata"]["HTTPStatusCode"], 204)


if __name__ == "__main__":
    unittest.main()
