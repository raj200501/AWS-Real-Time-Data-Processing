from rtap.plugins.base import EventPayload
from rtap.plugins.loader import PluginRegistry


def test_builtin_plugins_transform():
    payload = EventPayload(sensor_id=1, temperature=80.0, humidity=120.0, timestamp=1)
    registry = PluginRegistry()
    registry.register_builtin(["normalize_temperature", "clamp_humidity"])

    result = registry.process_all(payload)
    assert result.temperature < 80.0
    assert 0.0 <= result.humidity <= 100.0


def test_registry_rejects_unknown_plugin():
    registry = PluginRegistry()
    try:
        registry.register_builtin(["missing"])
    except ValueError as exc:
        assert "Unknown builtin plugin" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
