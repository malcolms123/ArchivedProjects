import openai



class GPT4:
	def __init__(self, apiKey, sysMessage):
		# setting and sending api key
		self.apiKey = apiKey
		openai.api_key = self.apiKey
		# preparing conversation with a system message
		self.sysMessage = sysMessage
		self.conversation = [{"role":"system", "content": self.sysMessage}]

	def ask(self, question):
		# prepare question
		qDict = {'role': 'user', 'content': question}
		self.conversation.append(qDict)
		try:
			# ask conversation to gpt
			response = openai.ChatCompletion.create(model="gpt-4", messages=self.conversation)
			# select the text response
			answer = response.choices[0].message.content
			# save answer in conversation
			aDict = {'role': 'assistant', 'content': answer}
			self.conversation.append(aDict)
			# return answer
			return answer
		except Exception as e:
			print(e)
			return 'Error getting response from GPT-4'