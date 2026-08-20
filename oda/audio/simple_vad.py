import math

from oda.audio.interfaces import VoiceActivityDetector


class SimpleVAD(VoiceActivityDetector):
    """
    VAD básico baseado na energia RMS do áudio PCM16.

    Serve como fallback/teste.
    O VAD real poderá substituir esta implementação
    sem alterar o AudioPipeline.
    """

    def __init__(self, threshold: int = 500):
        self.threshold = threshold

    def is_speech(self, audio: bytes) -> bool:
        if not audio:
            return False

        if len(audio) % 2 != 0:
            return False

        samples = []

        for i in range(0, len(audio), 2):
            sample = int.from_bytes(
                audio[i:i + 2],
                byteorder="little",
                signed=True,
            )
            samples.append(sample)

        if not samples:
            return False

        energy = math.sqrt(
            sum(sample * sample for sample in samples)
            / len(samples)
        )

        return energy >= self.threshold
