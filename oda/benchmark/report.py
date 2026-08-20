import json
from pathlib import Path

from oda.benchmark.runner import BenchmarkResult, summarize


def save_report(
    results: list[BenchmarkResult],
    output: str,
) -> Path:
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)

    summary = summarize(results)

    data = {
        "model": results[0].model if results else "unknown",
        "summary": summary,
        "results": [
            {
                "prompt_id": result.prompt_id,
                "category": result.category,
                "response": result.response,
                "latency_ms": result.latency_ms,
                "memory_before_mb": result.memory_before_mb,
                "memory_after_mb": result.memory_after_mb,
                "memory_delta_mb": result.memory_delta_mb,
            }
            for result in results
        ],
    }

    path.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    return path
