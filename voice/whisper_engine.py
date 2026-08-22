import sys
import whisper

MODEL_NAME = "base"

print(f"[WHISPER] carregando modelo {MODEL_NAME}...", flush=True)
model = whisper.load_model(MODEL_NAME)
print("[WHISPER] modelo carregado", flush=True)

def transcribe(audio_file):
    result = model.transcribe(
        audio_file,
        language="pt",
        fp16=False,
        temperature=0,
    )
    return result.get("text", "").strip()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python whisper_engine.py <audio.wav>")
        sys.exit(1)

    text = transcribe(sys.argv[1])
    print(text)
