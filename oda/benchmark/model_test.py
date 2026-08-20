from oda.benchmark.report import save_report
from oda.benchmark.runner import BenchmarkRunner
from oda.llm.backend import LLMBackend


def benchmark_backend(
    backend: LLMBackend,
    output: str,
):
    runner = BenchmarkRunner(
        model_name=backend.model_name(),
        generate=backend.generate,
    )

    results = runner.run()

    path = save_report(
        results,
        output,
    )

    return path
