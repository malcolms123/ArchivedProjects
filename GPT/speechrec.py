
from pydub import AudioSegment
import speech_recognition as sr

inf = 'voice.mp3'
out = 'test.wav'

sound = AudioSegment.from_mp3(inf)
sound.export(out, format='wav')

r = sr.Recognizer()

with sr.AudioFile(out) as source:
	audio_data = r.record(source)
	text = r.recognize_google(audio_data)
	print(text)