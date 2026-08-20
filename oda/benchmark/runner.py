import gc
import time

from dataclasses import dataclass
from typing import Callable

from oda.benchmark.prompts import BENCHMARK_PROMPTS


@dataclass
class BenchmarkResult:
    model: str
    prompt_id: str
    category: str
    response: str

    latency_ms: float

    memory_before_mb: float
    memory_after_mb: float
    memory_delta_mb: float


def process_memory_mb() -> float:
    """
    RSS do processo atual em MB.
    """
    with open("/proc/self/status", "r", encoding="utf-8") as file:
        for line in file:
            if line.startswith("VmRSS:"):
                kb = int(line.split()[1])
                return kb / 1024

    return 0.0


class BenchmarkRunner:
    def __init__(
        self,
        model_name: str,
        generate: Callable[[str], str],
        warmup: int = 1,
    ):
        self.model_name = model_name
        self.generate = generate
        self.warmup = warmup

    def _warmup(self) -> None:
        for _ in range(self.warmup):
            self.generate("Responda apenas: OK")

    def run(self) -> list[BenchmarkResult]:
        self._warmup()

        results = []

        for item in BENCHMARK_PROMPTS:
            gc.collect()

            memory_before = process_memory_mb()

            start = time.perf_counter()

            response = self.generate(item["prompt"])

            elapsed = time.perf_counter() - start

            memory_after = process_memory_mb()

            results.append(
                BenchmarkResult(
                    model=self.model_name,
                    prompt_id=item["id"],
                    category=item["category"],
                    response=response,
                    latency_ms=elapsed * 1000,
                    memory_before_mb=memory_before,
                    memory_after_mb=memory_after,
                    memory_delta_mb=(
                        memory_after - memory_before
                    ),
                )
            )

        return results


def summarize(
    results: list[BenchmarkResult],
) -> dict[str, float]:

    if not results:
        return {}

    latencies = [
        result.latency_ms
        for result in results
    ]

    memory_after = [
        result.memory_after_mb
        for result in results
    ]

    return {
        "average_latency_ms": (
            sum(latencies) / len(latencies)
        ),
        "min_latency_ms": min(latencies),
        "max_latency_ms": max(latencies),
        "average_memory_mb": (
            sum(memory_after) / len(memory_after)
        ),
        "max_memory_mb": max(memory_after),
    }
