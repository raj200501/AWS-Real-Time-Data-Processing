import boto3
from botocore.exceptions import ClientError
import logging

logging.basicConfig(level=logging.INFO)

def create_dashboard(dashboard_name, widgets):
    client = boto3.client('cloudwatch')
    try:
        response = client.put_dashboard(
            DashboardName=dashboard_name,
            DashboardBody=json.dumps({
                "widgets": widgets
            })
        )
        logging.info(f"Dashboard {dashboard_name} created successfully.")
    except ClientError as e:
        logging.error(f"Error creating dashboard: {e}")

def list_dashboards():
    client = boto3.client('cloudwatch')
    try:
        response = client.list_dashboards()
        dashboards = response['DashboardEntries']
        logging.info("CloudWatch Dashboards:")
        for dashboard in dashboards:
            logging.info(f" - {dashboard['DashboardName']}")
    except ClientError as e:
        logging.error(f"Error listing dashboards: {e}")

def delete_dashboard(dashboard_name):
    client = boto3.client('cloudwatch')
    try:
        client.delete_dashboards(DashboardNames=[dashboard_name])
        logging.info(f"Dashboard {dashboard_name} deleted successfully.")
    except ClientError as e:
        logging.error(f"Error deleting dashboard: {e}")

if __name__ == "__main__":
    dashboard_name = 'example-dashboard'
    widgets = [
        {
            "type": "metric",
            "x": 0,
            "y": 0,
            "width": 12,
            "height": 6,
            "properties": {
                "metrics": [
                    ["AWS/EC2", "CPUUtilization", "InstanceId", "i-1234567890abcdef0"]
                ],
                "period": 300,
                "stat": "Average",
                "region": "us-west-1",
                "title": "EC2 Instance CPU Utilization"
            }
        }
    ]
    
    create_dashboard(dashboard_name, widgets)
    list_dashboards()
    # Uncomment to delete the dashboard
    # delete_dashboard(dashboard_name)
