"""Plugin loader and registry."""

from __future__ import annotations

import importlib
from dataclasses import dataclass, field
from typing import Dict, Iterable, List

from .base import Plugin
from .builtin import HumidityClampPlugin, NormalizeTemperaturePlugin


BUILTIN_PLUGINS: Dict[str, type[Plugin]] = {
    "normalize_temperature": NormalizeTemperaturePlugin,
    "clamp_humidity": HumidityClampPlugin,
}


@dataclass
class PluginRegistry:
    """Registry for processing plugins."""

    plugins: List[Plugin] = field(default_factory=list)

    def register(self, plugin: Plugin) -> None:
        self.plugins.append(plugin)

    def register_builtin(self, names: Iterable[str]) -> None:
        for name in names:
            cls = BUILTIN_PLUGINS.get(name)
            if cls is None:
                raise ValueError(f"Unknown builtin plugin: {name}")
            self.register(cls())

    def register_from_path(self, path: str) -> None:
        module_path, attribute = path.rsplit(":", 1)
        module = importlib.import_module(module_path)
        plugin_cls = getattr(module, attribute)
        self.register(plugin_cls())

    def process_all(self, payload):
        for plugin in self.plugins:
            payload = plugin.process(payload)
        return payload
