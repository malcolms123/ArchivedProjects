import pyaudio
import audioop
import wave


def listen():
    # Set parameters for recording
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "output.wav"
    THRESHOLD = 500

    # Create an instance of PyAudio
    audio = pyaudio.PyAudio()
    print('-------------------------------')
    # Open a stream for recording audio
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("Waiting for noise...")

    # Wait for audio threshold to be exceeded
    while True:
        data = stream.read(CHUNK)
        rms = audioop.rms(data,2)
        if rms > THRESHOLD:
            print("Recording...")
            break

    # Collect audio data in chunks
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished recording.")

    # Stop and close the audio stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Write the recorded audio data to a WAV file
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()