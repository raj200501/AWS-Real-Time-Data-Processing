"""Cached boto3 client helper for local fakes."""

from __future__ import annotations

import os
from typing import Any, Dict

import boto3


_CLIENT_CACHE: Dict[str, Any] = {}
_REAL_CLIENT = boto3.client


def cached_client(service_name: str, *args, **kwargs):
    if os.getenv("RTAP_CACHE_CLIENTS", "1") != "1":
        return boto3.client(service_name, *args, **kwargs)
    if service_name not in _CLIENT_CACHE:
        _CLIENT_CACHE[service_name] = boto3.client(service_name, *args, **kwargs)
    return _CLIENT_CACHE[service_name]


def reset_cache() -> None:
    _CLIENT_CACHE.clear()


if os.getenv("RTAP_CACHE_CLIENTS", "1") == "1":
    boto3.client = cached_client


def cached_client_safe(service_name: str, *args, **kwargs):
    if os.getenv("RTAP_CACHE_CLIENTS", "1") != "1":
        return _REAL_CLIENT(service_name, *args, **kwargs)
    if service_name not in _CLIENT_CACHE:
        _CLIENT_CACHE[service_name] = _REAL_CLIENT(service_name, *args, **kwargs)
    return _CLIENT_CACHE[service_name]


if os.getenv("RTAP_CACHE_CLIENTS", "1") == "1":
    boto3.client = cached_client_safe
