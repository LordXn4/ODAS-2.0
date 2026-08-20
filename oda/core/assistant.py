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

        self._register_system_commands()

    def _register_system_commands(self):
        self.commands.register(
            "diagnóstico do sistema",
            self.system_diagnosis,
        )

        self.commands.register(
            "status da ram",
            self.memory_status,
        )

    def system_diagnosis(self):
        health = self.system.diagnose()

        return (
            f"Estado: {health.level}. "
            f"Uso de RAM: "
            f"{health.memory.usage_percent}%."
            f" {health.recommendation}"
        )

    def memory_status(self):
        memory = self.system.monitor.memory()

        return (
            f"RAM usada: {memory.used_mb} MB. "
            f"RAM disponível: {memory.available_mb} MB."
        )

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

            return self.commands.execute(result.text)

        return {
            "route": "llm",
            "text": result.text,
        }
