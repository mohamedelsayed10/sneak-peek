
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import os

def record_audio(recording, user_id, exam_id, duration=None):
    print("Recording...")

    sample_rate = 44100
    path = f'./data/logs_data/exams/{exam_id}/{user_id}'
    os.makedirs(path, exist_ok=True)
    output_file = os.path.join(path, 'audio.wav')


        # Indefinite recording until stopped via external control
    audio_data = []
    while recording[0]:  # Continue recording as long as recording[0] is True
        # Record 10 seconds at a time and append
        chunk = sd.rec(int(10 * sample_rate), samplerate=sample_rate, channels=2, dtype='int16')
        sd.wait()
        audio_data.append(chunk)
    # Concatenate recorded segments if indefinite duration
    audio_data = np.concatenate(audio_data, axis=0)
    write(output_file, sample_rate, np.array(audio_data))
    print(f"Recording saved as '{output_file}'")


