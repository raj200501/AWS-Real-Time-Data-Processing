"""
Automatically provide in-memory AWS service doubles for local runs.
This ensures example scripts and tests work without external AWS credentials.
Set USE_FAKE_AWS=0 to disable and use real boto3 clients.
"""
from __future__ import annotations

import os

import boto3

from fake_aws import FakeAWSClientFactory

if os.getenv("USE_FAKE_AWS", "1") == "1":
    _real_client = boto3.client

    def _fake_client(service_name: str, *args, **kwargs):
        try:
            return FakeAWSClientFactory(service_name)
        except NotImplementedError:
            return _real_client(service_name, *args, **kwargs)

    boto3.client = _fake_client
