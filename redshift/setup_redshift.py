import boto3
from botocore.exceptions import ClientError
import logging

logging.basicConfig(level=logging.INFO)

def create_cluster(cluster_id, db_name, master_username, master_password, node_type, cluster_type):
    client = boto3.client('redshift')
    try:
        response = client.create_cluster(
            ClusterIdentifier=cluster_id,
            DBName=db_name,
            MasterUsername=master_username,
            MasterUserPassword=master_password,
            NodeType=node_type,
            ClusterType=cluster_type
        )
        logging.info(f"Redshift cluster {cluster_id} created successfully.")
    except ClientError as e:
        logging.error(f"Error creating Redshift cluster: {e}")
        return None

    # Wait for the cluster to become available
    while True:
        try:
            response = client.describe_clusters(ClusterIdentifier=cluster_id)
            status = response['Clusters'][0]['ClusterStatus']
            if status == 'available':
                logging.info(f"Redshift cluster {cluster_id} is now available.")
                break
            time.sleep(10)
        except ClientError as e:
            logging.error(f"Error describing Redshift cluster: {e}")
            return None

    return response

def delete_cluster(cluster_id):
    client = boto3.client('redshift')
    try:
        client.delete_cluster(ClusterIdentifier=cluster_id, SkipFinalClusterSnapshot=True)
        logging.info(f"Redshift cluster {cluster_id} deleted successfully.")
    except ClientError as e:
        logging.error(f"Error deleting Redshift cluster: {e}")

def list_clusters():
    client = boto3.client('redshift')
    try:
        response = client.describe_clusters()
        clusters = response['Clusters']
        logging.info("Redshift clusters:")
        for cluster in clusters:
            logging.info(f" - {cluster['ClusterIdentifier']}")
    except ClientError as e:
        logging.error(f"Error listing Redshift clusters: {e}")

if __name__ == "__main__":
    cluster_id = 'example-cluster'
    db_name = 'exampledb'
    master_username = 'admin'
    master_password = 'Password123!'
    node_type = 'dc2.large'
    cluster_type = 'single-node'

    create_cluster(cluster_id, db_name, master_username, master_password, node_type, cluster_type)
    list_clusters()
    # Uncomment to delete the cluster
    # delete_cluster(cluster_id)
