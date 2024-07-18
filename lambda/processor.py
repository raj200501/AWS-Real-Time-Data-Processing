import json
import boto3
import logging

logging.basicConfig(level=logging.INFO)
s3 = boto3.client('s3')
dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    for record in event['Records']:
        payload = json.loads(record['kinesis']['data'])
        logging.info(f"Processing record: {payload}")

        # Save the processed data to S3
        s3.put_object(
            Bucket='your-s3-bucket',
            Key=f"processed/{payload['sensor_id']}_{payload['timestamp']}.json",
            Body=json.dumps(payload)
        )

        # Save the processed data to DynamoDB
        dynamodb.put_item(
            TableName='YourDynamoDBTable',
            Item={
                'sensor_id': {'S': str(payload['sensor_id'])},
                'timestamp': {'N': str(payload['timestamp'])},
                'temperature': {'N': str(payload['temperature'])},
                'humidity': {'N': str(payload['humidity'])}
            }
        )

    return {
        'statusCode': 200,
        'body': json.dumps('Processing complete')
    }
