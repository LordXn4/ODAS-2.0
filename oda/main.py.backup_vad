import asyncio

from oda.core.assistant import ODAAssistant
from oda.hud_bridge import HudBridge
from oda.hud_state import hud
from oda.stt.whisper_backend import WhisperBackend
from oda.audio.simple_vad import SimpleVAD
from oda.voice.runtime import ODAVoiceRuntime


async def main():
    print("ODA 2.0 iniciada.")
    print("Modo: OFFLINE")
    print("Sistema: inicializando voz...")

    # --------------------------------------------------------
    # Núcleo
    # --------------------------------------------------------
    assistant = ODAAssistant()

    # --------------------------------------------------------
    # STT
    # --------------------------------------------------------
    print("[STT] carregando Faster-Whisper...")

    recognizer = WhisperBackend(
        model_size="tiny",
        language="pt",
    )

    print(f"[STT] backend: {recognizer.model_name()}")

    # --------------------------------------------------------
    # Runtime de voz
    # --------------------------------------------------------
    runtime = ODAVoiceRuntime(
        assistant=assistant,
        recognizer=recognizer,
        silence_limit=8,
    )

    # --------------------------------------------------------
    # VAD
    # --------------------------------------------------------
    vad = SimpleVAD(threshold=500)

    # --------------------------------------------------------
    # HUD / WebSocket
    # --------------------------------------------------------
    bridge = hud.bridge

    async def on_audio(audio: bytes):
        if not audio:
            return

        is_speech = vad.is_speech(audio)

        result = runtime.process_audio(
            audio,
            is_speech,
        )

        if result is not None:
            print(f"[ODA] resultado: {result}")

    bridge.set_audio_callback(on_audio)

    hud.start()

    # --------------------------------------------------------
    # MODO DE TESTE
    #
    # Não existe wake-word conectado ainda.
    # Portanto iniciamos a sessão diretamente em LISTENING.
    # --------------------------------------------------------
    runtime.start_command()

    print("[VOICE] escutando...")
    print("[VOICE] PCM: 16-bit / mono / 16 kHz")
    print("[VOICE] VAD: SimpleVAD")
    print("[VOICE] STT: Faster-Whisper tiny")
    print("[VOICE] WebSocket: ws://0.0.0.0:8766")
    print("[VOICE] ODA pronta.")

    try:
        while True:
            await asyncio.sleep(1)

    except KeyboardInterrupt:
        print("\n[ODA] encerrando...")

    finally:
        await bridge.stop()
        runtime.reset()


if __name__ == "__main__":
    asyncio.run(main())
