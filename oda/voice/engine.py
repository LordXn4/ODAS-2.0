from abc import ABC, abstractmethod

from oda.config.settings import VoiceSettings


class VoiceEngine(ABC):
    def __init__(self, settings: VoiceSettings):
        self.settings = settings

    @abstractmethod
    def speak(self, text: str) -> None:
        """Converte texto em fala."""
        raise NotImplementedError

    def set_pitch(self, pitch: float) -> None:
        self.settings.pitch = pitch

    def set_speed(self, speed: float) -> None:
        self.settings.speed = speed

    def set_volume(self, volume: float) -> None:
        self.settings.volume = volume
