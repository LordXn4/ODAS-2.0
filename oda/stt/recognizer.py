from abc import ABC, abstractmethod


class SpeechRecognizer(ABC):
    """
    Interface de reconhecimento de fala.

    O restante da ODA não precisa saber qual motor
    está sendo usado: Whisper, ONNX, Faster-Whisper etc.
    """

    @abstractmethod
    def model_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def transcribe(self, audio: bytes) -> str:
        raise NotImplementedError
