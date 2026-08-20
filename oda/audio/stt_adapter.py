from oda.audio.session import VoiceSession
from oda.audio.recorder import VoiceRecorder
from oda.stt.recognizer import SpeechRecognizer


class STTCommandPipeline:
    """
    Liga o VoiceRecorder ao backend de reconhecimento de fala.
    """

    def __init__(
        self,
        session: VoiceSession,
        recognizer: SpeechRecognizer,
        silence_limit: int = 8,
    ):
        self.recorder = VoiceRecorder(
            session,
            silence_limit=silence_limit,
        )
        self.recognizer = recognizer

    def start_command(self) -> None:
        self.recorder.start_command()

    def process(
        self,
        audio: bytes,
        is_speech: bool,
    ) -> str | None:
        command_audio = self.recorder.process(
            audio,
            is_speech,
        )

        if command_audio is None:
            return None

        return self.recognizer.transcribe(
            command_audio
        )
