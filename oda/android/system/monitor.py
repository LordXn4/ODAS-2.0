import os
from dataclasses import dataclass


@dataclass
class MemoryStatus:
    total_mb: int
    available_mb: int
    used_mb: int
    usage_percent: float


class SystemMonitor:
    def memory(self) -> MemoryStatus:
        with open("/proc/meminfo", "r", encoding="utf-8") as file:
            values = {}

            for line in file:
                key, value = line.split(":", 1)

                if key in {"MemTotal", "MemAvailable"}:
                    values[key] = int(value.strip().split()[0])

        total_kb = values["MemTotal"]
        available_kb = values["MemAvailable"]
        used_kb = total_kb - available_kb

        return MemoryStatus(
            total_mb=total_kb // 1024,
            available_mb=available_kb // 1024,
            used_mb=used_kb // 1024,
            usage_percent=round(
                (used_kb / total_kb) * 100,
                1,
            ),
        )
