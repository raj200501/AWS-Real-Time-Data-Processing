import boto3
import unittest

class TestRedshift(unittest.TestCase):
    def setUp(self):
        self.client = boto3.client('redshift')
        self.cluster_identifier = 'example-cluster'

    def test_create_cluster(self):
        response = self.client.create_cluster(
            ClusterIdentifier=self.cluster_identifier,
            DBName='exampledb',
            MasterUsername='admin',
            MasterUserPassword='Password123!',
            NodeType='dc2.large',
            ClusterType='single-node'
        )
        self.assertEqual(response['Cluster']['ClusterStatus'], 'creating')

    def test_delete_cluster(self):
        response = self.client.delete_cluster(
            ClusterIdentifier=self.cluster_identifier,
            SkipFinalClusterSnapshot=True
        )
        self.assertEqual(response['Cluster']['ClusterStatus'], 'deleting')

if __name__ == '__main__':
    unittest.main()
