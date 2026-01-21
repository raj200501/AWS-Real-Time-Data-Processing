import boto3
import unittest
import json


class TestLambda(unittest.TestCase):
    def setUp(self):
        self.client = boto3.client("lambda")
        self.function_name = "example-processor"

    def test_invoke_function(self):
        response = self.client.invoke(
            FunctionName=self.function_name, Payload=json.dumps({"key": "value"})
        )
        self.assertEqual(response["StatusCode"], 200)
        self.assertTrue("Payload" in response)


if __name__ == "__main__":
    unittest.main()
