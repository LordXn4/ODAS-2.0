from oda.audio.interfaces import (
    AudioInput,
    SpeechRecognizer,
    VoiceActivityDetector,
    WakeWordDetector,
)


class AudioPipeline:
    """
    Pipeline principal de voz da ODA.

    Microfone -> VAD -> Wake Word -> Whisper/STT -> texto
    """

    def __init__(
        self,
        audio: AudioInput,
        vad: VoiceActivityDetector,
        wake_word: WakeWordDetector,
        recognizer: SpeechRecognizer,
    ):
        self.audio = audio
        self.vad = vad
        self.wake_word = wake_word
        self.recognizer = recognizer

        self.running = False

    def start(self) -> None:
        self.running = True
        self.audio.start()

    def stop(self) -> None:
        self.running = False
        self.audio.stop()

    def process_chunk(self, audio: bytes) -> str | None:
        if not self.running:
            return None

        # Ignora silêncio.
        if not self.vad.is_speech(audio):
            return None

        # Ainda não ativou a ODA.
        if not self.wake_word.detect(audio):
            return None

        text = self.recognizer.transcribe(audio)

        text = text.strip()

        if not text:
            return None

        return text
