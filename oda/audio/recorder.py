from oda.audio.session import VoiceSession, VoiceState


class VoiceRecorder:
    """
    Captura somente o comando após a ODA ser ativada.

    Fluxo:

    IDLE
      ↓ wake()
    LISTENING
      ↓ áudio + VAD
    PROCESSING
    """

    def __init__(
        self,
        session: VoiceSession,
        silence_limit: int = 8,
    ):
        self.session = session
        self.silence_limit = silence_limit
        self.silence_count = 0

    def start_command(self) -> None:
        self.session.wake()
        self.silence_count = 0

    def process(
        self,
        audio: bytes,
        is_speech: bool,
    ) -> bytes | None:

        if self.session.state != VoiceState.LISTENING:
            return None

        if is_speech:
            self.session.add_audio(audio)
            self.silence_count = 0
            return None

        self.silence_count += 1

        if self.silence_count < self.silence_limit:
            return None

        self.silence_count = 0

        return self.session.begin_processing()
