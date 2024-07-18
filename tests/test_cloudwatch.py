import boto3
import unittest

class TestCloudWatch(unittest.TestCase):
    def setUp(self):
        self.client = boto3.client('cloudwatch')
        self.alarm_name = 'example-alarm'
        self.metric_name = 'CPUUtilization'
        self.namespace = 'AWS/EC2'
        self.threshold = 70.0
        self.comparison_operator = 'GreaterThanThreshold'
        self.evaluation_periods = 2
        self.period = 60
        self.statistic = 'Average'
        self.actions_enabled = True
        self.alarm_actions = ['arn:aws:sns:us-west-1:123456789012:ExampleTopic']
        self.dimensions = [{'Name': 'InstanceId', 'Value': 'i-1234567890abcdef0'}]

    def test_create_alarm(self):
        response = self.client.put_metric_alarm(
            AlarmName=self.alarm_name,
            MetricName=self.metric_name,
            Namespace=self.namespace,
            Threshold=self.threshold,
            ComparisonOperator=self.comparison_operator,
            EvaluationPeriods=self.evaluation_periods,
            Period=self.period,
            Statistic=self.statistic,
            ActionsEnabled=self.actions_enabled,
            AlarmActions=self.alarm_actions,
            Dimensions=self.dimensions
        )
        self.assertEqual(response['ResponseMetadata']['HTTPStatusCode'], 200)

    def test_describe_alarms(self):
        response = self.client.describe_alarms(
            AlarmNames=[self.alarm_name]
        )
        self.assertEqual(response['ResponseMetadata']['HTTPStatusCode'], 200)
        self.assertTrue('MetricAlarms' in response)

    def test_delete_alarm(self):
        response = self.client.delete_alarms(
            AlarmNames=[self.alarm_name]
        )
        self.assertEqual(response['ResponseMetadata']['HTTPStatusCode'], 200)

if __name__ == '__main__':
    unittest.main()
