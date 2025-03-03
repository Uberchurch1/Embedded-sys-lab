import sounddevice as sd
import numpy as np
import wave
from faster_whisper import WhisperModel

def record_audio(filename="recorded_audio.wav", duration=10, samplerate=44100):
    print("Recording... Speak now.")
    audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype=np.int16)
    sd.wait()  # Wait for the recording to complete
    print("Recording finished.")

    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(audio_data.tobytes())

    return filename

def transcribe_audio(filename="recorded_audio.wav", lang="en"):
    model_size = "base"
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    print(f"Transcribing in {lang}...")
    segments, info = model.transcribe(filename, language=lang, beam_size=5)

    transcription = ""
    for segment in segments:
        transcription += segment.text + " "

    print("Transcription:", transcription.strip())
    return transcription.strip()

if __name__ == "__main__":
    audio_file = record_audio(duration=5)  # Adjust duration as needed
    result = transcribe_audio(audio_file, lang="fr")  # Change "fr" to any other supported language
    print("Final Transcription:", result)
