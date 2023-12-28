from gptHelper import GPT4

apiKey = open("../../Local-Storage/openAiApiKey.txt","r").readline()[:-1]

print('Hello this is CLI-GPT-4! What would you like to input as the system message?')

sysMessage = input('')

gpt4 = GPT4(apiKey, sysMessage)

while True:
	question = input('Q: ')
	answer = gpt4.ask(question)

	print(f"A: {answer}")