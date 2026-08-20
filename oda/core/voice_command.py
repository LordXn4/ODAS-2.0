from oda.audio.stt_adapter import STTCommandPipeline


class VoiceCommandHandler:
    """
    Recebe texto produzido pelo STT e entrega ao núcleo da ODA.
    """

    def __init__(self, assistant, pipeline: STTCommandPipeline):
        self.assistant = assistant
        self.pipeline = pipeline

    def start(self) -> None:
        self.pipeline.start_command()

    def process_audio(
        self,
        audio: bytes,
        is_speech: bool,
    ):
        text = self.pipeline.process(
            audio,
            is_speech,
        )

        if not text:
            return None

        return self.assistant.process(text)
