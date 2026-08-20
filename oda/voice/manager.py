from pathlib import Path

from oda.config.settings import VoiceSettings
from oda.voice.piper_engine import PiperEngine


class VoiceManager:
    def __init__(self, settings: VoiceSettings):
        self.settings = settings
        self._voices: dict[str, str] = {}

    def register_voice(self, name: str, model_path: str) -> None:
        self._voices[name] = model_path

    def available_voices(self) -> list[str]:
        return list(self._voices.keys())

    def selected_voice(self) -> str:
        return self.settings.voice

    def select_voice(self, name: str) -> None:
        if name not in self._voices:
            raise ValueError(f"Voz não encontrada: {name}")

        self.settings.voice = name

    def create_engine(self) -> PiperEngine:
        name = self.selected_voice()
        model_path = self._voices.get(name)

        if model_path is None:
            raise ValueError(f"Voz não encontrada: {name}")

        if not Path(model_path).exists():
            raise FileNotFoundError(model_path)

        return PiperEngine(
            self.settings,
            model_path,
        )
