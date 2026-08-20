from abc import ABC, abstractmethod


class AudioInput(ABC):
    """Fonte de áudio do ODAS."""

    @abstractmethod
    def start(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def stop(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def read(self) -> bytes:
        raise NotImplementedError


class VoiceActivityDetector(ABC):
    """Detecta se existe fala no áudio."""

    @abstractmethod
    def is_speech(self, audio: bytes) -> bool:
        raise NotImplementedError


class WakeWordDetector(ABC):
    """Detecta a palavra de ativação."""

    @abstractmethod
    def detect(self, audio: bytes) -> bool:
        raise NotImplementedError


class SpeechRecognizer(ABC):
    """Converte fala em texto."""

    @abstractmethod
    def transcribe(self, audio: bytes) -> str:
        raise NotImplementedError
