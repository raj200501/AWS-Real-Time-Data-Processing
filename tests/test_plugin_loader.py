from rtap.plugins.base import EventPayload
from rtap.plugins.loader import PluginRegistry


def test_plugin_loader_imports_from_path():
    registry = PluginRegistry()
    registry.register_from_path("tests.fixtures.custom_plugin:AddHumidityPlugin")

    payload = EventPayload(sensor_id=1, temperature=20.0, humidity=10.0, timestamp=1)
    result = registry.process_all(payload)
    assert result.humidity == 15.0
