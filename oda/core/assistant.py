from oda.android.accessibility.actions import (
    AccessibilityAction,
    ActionType,
)
from oda.android.accessibility.bridge import AccessibilityBridge
from oda.android.accessibility.mock_bridge import MockAccessibilityBridge
from oda.android.system.optimizer import SystemOptimizer
from oda.commands.registry import CommandRegistry
from oda.android.apps.mock_provider import MockAppProvider
from oda.android.apps.service import AppService
from oda.core.router import Router


class ODAAssistant:
    def __init__(
        self,
        accessibility: AccessibilityBridge | None = None,
    ):
        self.router = Router()
        self.commands = CommandRegistry()
        self.system = SystemOptimizer()
        self.apps = AppService(MockAppProvider())
        self.apps.refresh()

        self.accessibility = (
            accessibility
            or MockAccessibilityBridge()
        )

        self.voice_volume = 1.0

        self._register_system_commands()

    def _register_system_commands(self):
        commands = {
            "diagnóstico do sistema": self.system_diagnosis,
            "diagnostico do sistema": self.system_diagnosis,

            "status da ram": self.memory_status,
            "status da memória": self.memory_status,
            "status da memoria": self.memory_status,

            "aumente o volume": self.volume_up,
            "aumentar o volume": self.volume_up,
            "aumente volume": self.volume_up,
            "aumentar volume": self.volume_up,

            "diminua o volume": self.volume_down,
            "diminuir o volume": self.volume_down,
            "diminua volume": self.volume_down,
            "diminuir volume": self.volume_down,

            "volume máximo": self.volume_max,
            "volume maximo": self.volume_max,

            "volume mínimo": self.volume_min,
            "volume minimo": self.volume_min,

            "pare de falar": self.stop_speaking,
            "parar de falar": self.stop_speaking,
            "pare a fala": self.stop_speaking,
            "pare de falar oda": self.stop_speaking,

            "olá oda": self.hello,
            "ola oda": self.hello,
            "oi oda": self.hello,
            "oi": self.hello,
        }

        for name, handler in commands.items():
            self.commands.register(name, handler)

    def system_diagnosis(self):
        health = self.system.diagnose()

        return (
            f"Estado: {health.level}. "
            f"Uso de RAM: {health.memory.usage_percent}%. "
            f"{health.recommendation}"
        )

    def memory_status(self):
        memory = self.system.monitor.memory()

        return (
            f"RAM usada: {memory.used_mb} MB. "
            f"RAM disponível: {memory.available_mb} MB."
        )

    def volume_up(self):
        self.voice_volume = min(1.0, self.voice_volume + 0.1)

        return {
            "route": "command",
            "action": "volume_up",
            "volume": self.voice_volume,
            "speech": f"Volume em {round(self.voice_volume * 100)} por cento.",
        }

    def volume_down(self):
        self.voice_volume = max(0.0, self.voice_volume - 0.1)

        return {
            "route": "command",
            "action": "volume_down",
            "volume": self.voice_volume,
            "speech": f"Volume em {round(self.voice_volume * 100)} por cento.",
        }

    def volume_max(self):
        self.voice_volume = 1.0

        return {
            "route": "command",
            "action": "volume_max",
            "volume": self.voice_volume,
            "speech": "Volume máximo.",
        }

    def volume_min(self):
        self.voice_volume = 0.0

        return {
            "route": "command",
            "action": "volume_min",
            "volume": self.voice_volume,
            "speech": "Volume mínimo.",
        }

    def stop_speaking(self):
        return {
            "route": "command",
            "action": "stop_speaking",
            "speech": "",
        }

    def hello(self):
        return {
            "route": "command",
            "action": "hello",
            "speech": "Olá. ODA online. Pode falar.",
        }

    def open_app(self, app: str):
        installed = self.apps.find(app)

        if installed is None or not installed.launchable:
            return {
                "route": "accessibility",
                "action": "open_app",
                "app": app,
                "success": False,
                "reason": "Aplicativo não encontrado",
            }

        action = AccessibilityAction(
            type=ActionType.OPEN_APP,
            description=f"Abrir {installed.name}",
            app=installed.package_name,
        )

        if not self.accessibility.is_available():
            return {
                "route": "accessibility",
                "status": "unavailable",
            }

        success = self.accessibility.execute(action)

        return {
            "route": "accessibility",
            "action": action.type.value,
            "app": app,
            "success": success,
        }

    def process(self, text: str):
        result = self.router.route(text)

        if result.route == "command":
            normalized = result.text.strip().lower()

            if normalized.startswith("abra "):
                app_name = result.text.strip()[5:].strip()
                return self.open_app(app_name)

            if normalized.startswith("abra o "):
                app_name = result.text.strip()[7:].strip()
                return self.open_app(app_name)

            command_result = self.commands.execute(result.text)

            if command_result is not None:
                return command_result

            return {
                "route": "command",
                "action": "unknown",
                "text": result.text,
                "speech": "Não reconheci esse comando.",
            }

        return {
            "route": "llm",
            "text": result.text,
        }
