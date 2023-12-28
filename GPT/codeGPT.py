from gptHelper import GPT4
import os


def parsePython(code_string):
	try:
		code_segments = code_string.split("```")
		finalCode = code_segments[1]
		if (finalCode[0:6] == 'python'):
			print('Python flag found. Parsing code.')
			finalCode = finalCode[6:]
		else:
			print('No python flag found. Returning no code.')
			finalCode = ''
		print('----- PARSED CODE READOUT -----')
		print(finalCode)
		print('-------------------------------')
		f = open("GPTCode.py","w")
		f.write(finalCode)
		return True
	except:
		return False

apiKey = open("../../Local-Storage/openAiApiKey.txt","r").readline()[:-1]

sysMessage = "You are an export python developer. You can only respond with python code. Do not worry about package dependencies."

codeGPT = GPT4(apiKey, sysMessage)

request = input('What would you like me to create?\n')


response = codeGPT.ask(request)


parsePython(response)


os.system('python3.11 GPTCode.py')

while True:
	request = input('Any modifications?\n')
	response = codeGPT.ask(request)
	parsePython(response)
	os.system('python3.11 GPTCode.py')