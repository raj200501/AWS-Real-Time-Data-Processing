import json

from rtap.logging_utils import LogContext, configure_logging


def test_json_logging_contains_context(capfd):
    context = LogContext(service="rtap", component="test")
    logger = configure_logging(
        json_format=True, context=context, extra={"run_id": "abc"}
    )
    logger.info("hello")

    out, _ = capfd.readouterr()
    payload = json.loads(out.strip())
    assert payload["message"] == "hello"
    assert payload["service"] == "rtap"
    assert payload["component"] == "test"


def test_text_logging_includes_context(capfd):
    context = LogContext(service="rtap", component="text")
    logger = configure_logging(
        json_format=False, context=context, extra={"run_id": "123"}
    )
    logger.info("ping")

    out, _ = capfd.readouterr()
    assert "ping" in out
    assert "run_id" in out
