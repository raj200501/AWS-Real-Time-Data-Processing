from rtap.plugins.base import EventPayload
from rtap.policy import PolicyEngine, RiskLevel


def test_policy_allows_safe_event():
    engine = PolicyEngine(max_temperature=40.0, max_humidity=90.0)
    payload = EventPayload(sensor_id=1, temperature=25.0, humidity=40.0, timestamp=1)
    decision = engine.evaluate(payload)

    assert decision.allowed is True
    assert decision.risk == RiskLevel.low


def test_policy_blocks_out_of_range():
    engine = PolicyEngine(max_temperature=30.0, max_humidity=50.0)
    payload = EventPayload(sensor_id=1, temperature=35.0, humidity=60.0, timestamp=1)
    decision = engine.evaluate(payload)

    assert decision.allowed is False
    assert decision.risk in (RiskLevel.high, RiskLevel.medium)
