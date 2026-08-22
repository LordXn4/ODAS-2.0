from oda.audio.stt_adapter import STTCommandPipeline
from oda.hud_state import hud


class VoiceCommandHandler:
    """
    Recebe texto produzido pelo STT e entrega ao núcleo da ODA.
    """

    def __init__(self, assistant, pipeline: STTCommandPipeline):
        hud.start()
        self.assistant = assistant
        self.pipeline = pipeline

    def start(self) -> None:
        hud.listening()
        self.pipeline.start_command()

    def process_audio(
        self,
        audio: bytes,
        is_speech: bool,
    ):
        hud.processing()

        text = self.pipeline.process(
            audio,
            is_speech,
        )

        if not text:
            return None

        try:
            return self.assistant.process(text)
        finally:
            hud.idle()
            self.pipeline.recorder.session.reset()
