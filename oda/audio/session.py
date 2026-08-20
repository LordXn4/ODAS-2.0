from enum import Enum


class VoiceState(str, Enum):
    IDLE = "idle"
    LISTENING = "listening"
    PROCESSING = "processing"


class VoiceSession:
    def __init__(self):
        self.state = VoiceState.IDLE
        self.audio_buffer: list[bytes] = []

    def reset(self) -> None:
        self.state = VoiceState.IDLE
        self.audio_buffer.clear()

    def wake(self) -> None:
        self.state = VoiceState.LISTENING
        self.audio_buffer.clear()

    def add_audio(self, audio: bytes) -> None:
        if self.state == VoiceState.LISTENING:
            self.audio_buffer.append(audio)

    def begin_processing(self) -> bytes:
        self.state = VoiceState.PROCESSING
        return b"".join(self.audio_buffer)
