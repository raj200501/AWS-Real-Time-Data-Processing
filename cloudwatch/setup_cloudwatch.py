import boto3
from botocore.exceptions import ClientError
import logging

logging.basicConfig(level=logging.INFO)

def create_alarm(alarm_name, metric_name, namespace, threshold, comparison_operator, evaluation_periods, period, statistic, actions_enabled, alarm_actions):
    client = boto3.client('cloudwatch')
    try:
        response = client.put_metric_alarm(
            AlarmName=alarm_name,
            MetricName=metric_name,
            Namespace=namespace,
            Threshold=threshold,
            ComparisonOperator=comparison_operator,
            EvaluationPeriods=evaluation_periods,
            Period=period,
            Statistic=statistic,
            ActionsEnabled=actions_enabled,
            AlarmActions=alarm_actions
        )
        logging.info(f"Alarm {alarm_name} created successfully.")
    except ClientError as e:
        logging.error(f"Error creating alarm: {e}")

def list_alarms():
    client = boto3.client('cloudwatch')
    try:
        response = client.describe_alarms()
        alarms = response['MetricAlarms']
        logging.info("CloudWatch Alarms:")
        for alarm in alarms:
            logging.info(f" - {alarm['AlarmName']}")
    except ClientError as e:
        logging.error(f"Error listing alarms: {e}")

def delete_alarm(alarm_name):
    client = boto3.client('cloudwatch')
    try:
        client.delete_alarms(AlarmNames=[alarm_name])
        logging.info(f"Alarm {alarm_name} deleted successfully.")
    except ClientError as e:
        logging.error(f"Error deleting alarm: {e}")

if __name__ == "__main__":
    alarm_name = 'example-alarm'
    metric_name = 'CPUUtilization'
    namespace = 'AWS/EC2'
    threshold = 70.0
    comparison_operator = 'GreaterThanThreshold'
    evaluation_periods = 2
    period = 60
    statistic = 'Average'
    actions_enabled = True
    alarm_actions = ['arn:aws:sns:us-west-1:123456789012:ExampleTopic']
    
    create_alarm(alarm_name, metric_name, namespace, threshold, comparison_operator, evaluation_periods, period, statistic, actions_enabled, alarm_actions)
    list_alarms()
    # Uncomment to delete the alarm
    # delete_alarm(alarm_name)
