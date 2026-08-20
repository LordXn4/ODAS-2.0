import io
import wave

from oda.stt.recognizer import SpeechRecognizer


class WhisperBackend(SpeechRecognizer):
    """
    Backend STT usando Faster-Whisper.

    Aceita PCM 16-bit mono e WAV.
    """

    def __init__(
        self,
        model_size: str = "tiny",
        language: str = "pt",
    ):
        from faster_whisper import WhisperModel

        self.model_size = model_size
        self.language = language

        self.model = WhisperModel(
            model_size,
            device="cpu",
            compute_type="int8",
        )

    def model_name(self) -> str:
        return f"faster-whisper-{self.model_size}"

    @staticmethod
    def _pcm_to_wav(
        audio: bytes,
        sample_rate: int = 16000,
    ) -> io.BytesIO:
        wav = io.BytesIO()

        with wave.open(wav, "wb") as output:
            output.setnchannels(1)
            output.setsampwidth(2)
            output.setframerate(sample_rate)
            output.writeframes(audio)

        wav.seek(0)
        return wav

    @staticmethod
    def _wav_to_wav_bytes(audio: bytes) -> io.BytesIO:
        """
        Valida e preserva um WAV existente.
        """
        source = io.BytesIO(audio)

        with wave.open(source, "rb") as wav:
            channels = wav.getnchannels()
            sample_width = wav.getsampwidth()
            sample_rate = wav.getframerate()

            if channels != 1:
                raise ValueError(
                    "O áudio precisa ser mono."
                )

            if sample_width != 2:
                raise ValueError(
                    "O áudio precisa ser PCM 16-bit."
                )

        source.seek(0)
        return source

    def transcribe(self, audio: bytes) -> str:
        if not audio:
            return ""

        # Detecta automaticamente WAV ou PCM.
        if audio[:4] == b"RIFF" and audio[8:12] == b"WAVE":
            wav = self._wav_to_wav_bytes(audio)
        else:
            wav = self._pcm_to_wav(audio)

        segments, _ = self.model.transcribe(
            wav,
            language=self.language,
            beam_size=1,
            vad_filter=True,
        )

        return " ".join(
            segment.text.strip()
            for segment in segments
        ).strip()
