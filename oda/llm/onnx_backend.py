from pathlib import Path

import onnxruntime as ort

from oda.llm.backend import LLMBackend
from oda.llm.runtime import create_cpu_session_options


class ONNXLLMBackend(LLMBackend):
    def __init__(
        self,
        model_path: str,
        name: str = "onnx-model",
        threads: int = 4,
    ):
        self.path = Path(model_path)

        if not self.path.exists():
            raise FileNotFoundError(
                f"Modelo não encontrado: {self.path}"
            )

        self.name = name

        options = create_cpu_session_options(
            threads=threads,
        )

        self.session = ort.InferenceSession(
            str(self.path),
            sess_options=options,
            providers=["CPUExecutionProvider"],
        )

    def model_name(self) -> str:
        return self.name

    def generate(self, prompt: str) -> str:
        raise NotImplementedError(
            "O tokenizer e o formato de entrada "
            "dependem do modelo."
        )
