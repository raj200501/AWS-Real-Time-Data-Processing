import boto3
from botocore.exceptions import ClientError
import logging

logging.basicConfig(level=logging.INFO)

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
    job_name = 'example-job'
    role = 'arn:aws:iam::123456789012:role/AWSGlueServiceRole'
    script_location = 's3://your-script-location/script.py'
    temp_dir = 's3://your-temp-dir/'

    create_job(job_name, role, script_location, temp_dir)
    start_job(job_name)
