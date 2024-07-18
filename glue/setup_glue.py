import boto3
from botocore.exceptions import ClientError
import logging

logging.basicConfig(level=logging.INFO)

def create_crawler(crawler_name, role, database_name, s3_target):
    client = boto3.client('glue')
    try:
        response = client.create_crawler(
            Name=crawler_name,
            Role=role,
            DatabaseName=database_name,
            Targets={'S3Targets': [{'Path': s3_target}]}
        )
        logging.info(f"Crawler {crawler_name} created successfully.")
    except ClientError as e:
        logging.error(f"Error creating crawler: {e}")

def start_crawler(crawler_name):
    client = boto3.client('glue')
    try:
        client.start_crawler(Name=crawler_name)
        logging.info(f"Crawler {crawler_name} started successfully.")
    except ClientError as e:
        logging.error(f"Error starting crawler: {e}")

def create_job(job_name, role, script_location, temp_dir):
    client = boto3.client('glue')
    try:
        response = client.create_job(
            Name=job_name,
            Role=role,
            Command={'Name': 'glueetl', 'ScriptLocation': script_location},
            DefaultArguments={'--TempDir': temp_dir}
        )
        logging.info(f"Job {job_name} created successfully.")
    except ClientError as e:
        logging.error(f"Error creating job: {e}")

def start_job(job_name):
    client = boto3.client('glue')
    try:
        response = client.start_job_run(JobName=job_name)
        job_run_id = response['JobRunId']
        logging.info(f"Job {job_name} started successfully with run ID: {job_run_id}")
        
        # Wait for the job to complete
        while True:
            job_status = client.get_job_run(JobName=job_name, RunId=job_run_id)['JobRun']['JobRunState']
            if job_status in ['SUCCEEDED', 'FAILED', 'STOPPED']:
                break
            time.sleep(10)
        
        if job_status == 'SUCCEEDED':
            logging.info(f"Job {job_name} completed successfully.")
        else:
            logging.error(f"Job {job_name} failed with status: {job_status}")
    except ClientError as e:
        logging.error(f"Error starting job: {e}")

if __name__ == "__main__":
    crawler_name = 'example-crawler'
    role = 'arn:aws:iam::123456789012:role/AWSGlueServiceRole'
    database_name = 'example_database'
    s3_target = 's3://your-s3-bucket/path/to/data'
    job_name = 'example-job'
    script_location = 's3://your-script-location/script.py'
    temp_dir = 's3://your-temp-dir/'

    create_crawler(crawler_name, role, database_name, s3_target)
    start_crawler(crawler_name)
    create_job(job_name, role, script_location, temp_dir)
    start_job(job_name)
