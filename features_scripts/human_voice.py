import pyaudio
import numpy as np

# Audio parameters
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
THRESHOLD = 500  # Adjust this value to change sensitivity

def is_voice_detected(stream):
    """Check if voice is detected based on audio input."""
    data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
    energy = np.sum(np.abs(data)) / len(data)
    if energy > THRESHOLD:
        print("Voice Detected!")
        return True

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open audio stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

