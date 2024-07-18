import boto3
from botocore.exceptions import ClientError

def create_bucket(bucket_name, region=None):
    client = boto3.client('s3')
    try:
        if region:
            location = {'LocationConstraint': region}
            client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
        else:
            client.create_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} created successfully.")
    except ClientError as e:
        print(f"Error creating bucket: {e}")

def list_buckets():
    client = boto3.client('s3')
    response = client.list_buckets()
    print("Buckets:")
    for bucket in response['Buckets']:
        print(f"  {bucket['Name']}")

if __name__ == "__main__":
    bucket_name = 'your-s3-bucket'
    region = 'us-west-1'
    create_bucket(bucket_name, region)
    list_buckets()
