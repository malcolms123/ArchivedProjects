from audioTest import listen
import openai, json, os, sys, subprocess, time
from gtts import gTTS

openai.api_key = open("../../Local-Storage/openAiApiKey.txt","r").readline()[:-1]

def parsePython(code_string):
	try:
		code_segments = code_string.split("```")
		finalCode = code_segments[1]
		if (finalCode[0:6] == 'python'):
			print('found it')
			finalCode = finalCode[6:]
		print('----- PARSED CODE READOUT -----')
		print(finalCode)
		print('-------------------------------')
		f = open("GPTCode.py","w")
		f.write(finalCode)
		return True
	except:
		return False

def askChatGPT(question, sysContent):
	try:
		print('aaa')
		response = openai.ChatCompletion.create(model="gpt-4-0314",messages=[{"role": "system", "content": sysContent},{'role':'user','content':question}])
		answer = response.choices[0].message.content
		return answer
	except Exception as e:
		print(e)
		return 'Finding it hard to think with all this rate limiting.'

while True:
	time.sleep(0.1)
	audibleResponse = False
	executableResponse = False
	'''
	listen()

	print("Transcribing audio...")
	audio_file = open("output.wav", "rb")
	transcript = openai.Audio.transcribe("whisper-1", audio_file)
	
	question = transcript.text
	print(f"Question: {question}")
	'''
	question = "Jimmy make game where you control a blue circle and dodge red circles and collect yellow coins"

	if question.count('Gary') > 0:
		answer = askChatGPT(question,"You are a helpful assistant.")
		audibleResponse = True
	elif question.count('Jimmy') > 0:
		question = question + " in a python script please"
		tries = question.count('please')
		for i in range(tries):
			print(question)
			answer = askChatGPT(question, "You can only respond with python code.")
			print(answer)
			if parsePython(answer):
				answer = 'Code above.'
				executableResponse = True
				break
			print(f"Attempt #{i+1} failed.")
		if not executableResponse:
			answer = f"Sorry, I don't understand I tried {tries} times."

	else:
		answer = "Unknown AI."

	print(f"Answer: {answer}")

	if audibleResponse:
		tts = gTTS(answer,lang='en',tld='co.uk')
		tts.save('voice.mp3')
		os.system('mpg123 ' + 'voice.mp3')

	if executableResponse:
		os.system('python3 GPTCode.py')





