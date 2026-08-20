from abc import ABC, abstractmethod


class LLMBackend(ABC):
    """
    Interface comum para modelos locais.

    O restante da ODA não precisa saber se o modelo
    usa ONNX, GGUF ou outro runtime.
    """

    @abstractmethod
    def generate(self, prompt: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def model_name(self) -> str:
        raise NotImplementedError
