"""Ensure local AWS fakes are activated for the test suite."""

import sitecustomize  # noqa: F401

import pytest

import rtap.aws as aws


@pytest.fixture(autouse=True)
def reset_rtap_cache():
    aws.reset_cache()
    yield
    aws.reset_cache()
