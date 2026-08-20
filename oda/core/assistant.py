from oda.android.system.optimizer import SystemOptimizer
from oda.commands.registry import CommandRegistry
from oda.core.router import Router


class ODAAssistant:
    def __init__(self):
        self.router = Router()
        self.commands = CommandRegistry()
        self.system = SystemOptimizer()

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
            f"Uso de RAM: {health.memory.usage_percent}%. "
            f"{health.recommendation}"
        )

    def memory_status(self):
        memory = self.system.monitor.memory()

        return (
            f"RAM usada: {memory.used_mb} MB. "
            f"RAM disponível: {memory.available_mb} MB."
        )

    def process(self, text: str):
        result = self.router.route(text)

        if result.route == "command":
            response = self.commands.execute(result.text)

            if response is not None:
                return response

            return {
                "route": "command",
                "text": result.text,
                "status": "not_registered",
            }

        return {
            "route": "llm",
            "text": result.text,
        }
