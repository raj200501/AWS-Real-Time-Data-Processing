import os

import boto3

import rtap.aws  # noqa: F401


def test_cached_boto3_clients_reuse_instance(monkeypatch):
    monkeypatch.setenv("RTAP_CACHE_CLIENTS", "1")
    assert os.getenv("RTAP_CACHE_CLIENTS") == "1"
    client_a = boto3.client("s3")
    client_b = boto3.client("s3")

    assert client_a is client_b
