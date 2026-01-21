from rtap.health import build_health_status


def test_health_status_ok():
    status = build_health_status({"kinesis": True, "s3": True})
    assert status.status == "ok"
    assert status.checks["kinesis"] == "ok"


def test_health_status_degraded():
    status = build_health_status({"kinesis": True, "s3": False})
    assert status.status == "degraded"
    assert status.checks["s3"] == "fail"
