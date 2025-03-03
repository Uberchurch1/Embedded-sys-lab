import sounddevice as sd
import numpy as np
import wave
from faster_whisper import WhisperModel

is_recording = False
filename = "recorded_audio.wav"

def start_recording(samplerate=44100):
    global is_recording
    is_recording = True
    print("Recording started... Press stop to end.")

    def record():
        audio_data = []
        with sd.InputStream(samplerate=samplerate, channels=1, dtype=np.int16) as stream:
            while is_recording:
                data, _ = stream.read(samplerate // 10)  # Read in 0.1s chunks
                audio_data.append(data)
        
        # Save the recorded audio
        audio_array = np.concatenate(audio_data, axis=0)
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(samplerate)
            wf.writeframes(audio_array.tobytes())
        
        print("Recording saved:", filename)

def stop_recording():
    """Stops recording audio."""
    global is_recording
    is_recording = False
    print("Recording stopped.")

def transcribe_audio(lang="en"):
    """Transcribes recorded audio using Faster-Whisper."""
    model_size = "base"
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    print(f"Transcribing in {lang}...")
    segments, info = model.transcribe(filename, language=lang, beam_size=5)

    transcription = " ".join(segment.text for segment in segments)
    print("Transcription:", transcription.strip())
    return transcription.strip()

def stop_recording_and_transcribe(lang="en"):
    """Stops recording and automatically transcribes the audio."""
    stop_recording()
    return transcribe_audio(lang=lang)

# Example usage:
if __name__ == "__main__":
    start_recording()  # Call this when "Start" button is pressed
    input("Press Enter to stop recording...")  # Simulate user stopping
    result = stop_recording_and_transcribe(lang="fr")  # Change "fr" to any other language
    print("Final Transcription:", result)
