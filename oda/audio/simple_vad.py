import math
from oda.audio.interfaces import VoiceActivityDetector


class SimpleVAD(VoiceActivityDetector):
    """
    VAD RMS simples com limiar configurável.

    O valor padrão foi aumentado para evitar que o ruído
    ambiente seja interpretado como fala.
    """

    def __init__(self, threshold: int = 1500):
        self.threshold = threshold

    def is_speech(self, audio: bytes) -> bool:
        if not audio or len(audio) % 2 != 0:
            return False

        total = 0
        count = 0

        for i in range(0, len(audio), 2):
            sample = int.from_bytes(
                audio[i:i + 2],
                byteorder="little",
                signed=True,
            )
            total += sample * sample
            count += 1

        if count == 0:
            return False

        energy = math.sqrt(total / count)

        return energy >= self.threshold
