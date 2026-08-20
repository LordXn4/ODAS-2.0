
from oda.audio.session import VoiceSession
from oda.audio.stt_adapter import STTCommandPipeline
from oda.core.voice_command import VoiceCommandHandler


class ODAVoiceRuntime:
    """
    Orquestra o fluxo de voz da ODA.

    Fonte de áudio
        ↓
    VAD
        ↓
    VoiceRecorder
        ↓
    STT / Whisper
        ↓
    VoiceCommandHandler
        ↓
    ODAAssistant
        ↓
    HUD
    """

    def __init__(
        self,
        assistant,
        recognizer,
        silence_limit: int = 8,
    ):
        self.session = VoiceSession()

        self.pipeline = STTCommandPipeline(
            session=self.session,
            recognizer=recognizer,
            silence_limit=silence_limit,
        )

        self.handler = VoiceCommandHandler(
            assistant=assistant,
            pipeline=self.pipeline,
        )

    def start_command(self) -> None:
        self.handler.start()

    def process_audio(
        self,
        audio: bytes,
        is_speech: bool,
    ):
        return self.handler.process_audio(
            audio,
            is_speech,
        )

    def reset(self) -> None:
        self.session.reset()
