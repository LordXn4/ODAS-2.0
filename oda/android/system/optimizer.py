from dataclasses import dataclass

from oda.android.system.monitor import MemoryStatus, SystemMonitor


@dataclass
class SystemHealth:
    memory: MemoryStatus
    level: str
    recommendation: str


class SystemOptimizer:
    def __init__(self, monitor: SystemMonitor | None = None):
        self.monitor = monitor or SystemMonitor()

    def diagnose(self) -> SystemHealth:
        memory = self.monitor.memory()

        if memory.usage_percent >= 90:
            level = "critical"
            recommendation = "Liberar memória e verificar aplicativos pesados."
        elif memory.usage_percent >= 75:
            level = "attention"
            recommendation = "Verificar aplicativos consumindo muita memória."
        else:
            level = "normal"
            recommendation = "Memória dentro de uma faixa normal."

        return SystemHealth(
            memory=memory,
            level=level,
            recommendation=recommendation,
        )
