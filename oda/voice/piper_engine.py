import subprocess
from pathlib import Path

from oda.config.settings import VoiceSettings
from oda.voice.engine import VoiceEngine


class PiperEngine(VoiceEngine):
    def __init__(
        self,
        settings: VoiceSettings,
        model_path: str,
        output_dir: str = "models/tts/output",
    ):
        super().__init__(settings)
        self.model_path = Path(model_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def speak(self, text: str) -> Path:
        output_file = self.output_dir / "oda-output.wav"

        command = [
            "python",
            "-m",
            "piper",
            "-m",
            str(self.model_path),
            "-f",
            str(output_file),
            "--volume",
            str(self.settings.volume),
        ]

        subprocess.run(
            command,
            input=text,
            text=True,
            check=True,
        )

        return output_file
