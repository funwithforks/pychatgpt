import time
import openai


# Place api key in a file called 'secret' in the same directory as this script. Or paste it in below.
class Conversation:
	def __init__(self):
		# You may insert your OpenAI API key below. Replace the word secret that follows openai.api_key =
		# https://platform.openai.com/account/api-keys
		openai.api_key = self.check_secret()
		self.first_question = True
		# Choose the model you want to use by setting the engine ID
		# text-davinci-002, text-curie-001, text-babbage-001, text-ada-001, davinci, curie, babbage, ada
		self.engine_id = "text-davinci-003"

		# Define any additional parameters you want to use
		self.params = {
			"temperature": 0.5,
			"max_tokens": 256,
			"stop": "\n\n ",
			"top_p": .3,
			"frequency_penalty": 0.1,
			"presence_penalty": 0.5,
		}
		"""
			"temperature": This controls the "creativity" or randomness of the model's response. A lower temperature leads to 
			more conservative and predictable responses, while a higher temperature leads to more diverse and unexpected 
			responses. A value of 0.7 is a reasonable default.
		
			"max_tokens": This controls the maximum number of tokens that the model can generate in response to a prompt. 
			A higher value allows for longer and more detailed responses, but may also increase the likelihood of the model 
			generating irrelevant or nonsensical content.
		
			"stop": This is a string that tells the model to stop generating tokens when it encounters a specific sequence of 
			characters. In this case, "\n\n" tells the model to stop when it generates two consecutive line breaks, which is a 
			common way to denote the end of a paragraph.
		
			"top_p": This controls the probability distribution for selecting the next token. A higher value leads to more 
			diverse and surprising responses, while a lower value leads to more predictable responses. A value of 0.1 is 
			relatively low and may result in more conservative responses.
		
			"frequency_penalty": This is a penalty factor applied to tokens that have already been generated in the output. 
			A higher value discourages the model from repeating the same tokens, which can make the response more varied 
			and interesting.
		
			"presence_penalty": This is a penalty factor applied to tokens that have appeared in the prompt. A higher value 
			discourages the model from repeating words or phrases from the prompt in the output, which can make the response 
			more creative and independent."""

		# An ever-growing string containing prompts and responses. The longer this gets, the more it costs per prompt.
		self.chat_history = ""

	def check_secret(self):
		try:
			f = open('secret')
		except:
			print("Create a file called 'secret' and paste your OpenAI API key or paste your key into this file as the"
				"value for 'openai.api_key' on line 10, https://platform.openai.com/account/api-keys")
			quit()
		for line in f:
			if line.startswith('sk-'):
				secret = line.strip()
				break
		return secret

	# Call the OpenAI API to generate a response
	def generate_response(self, prompt, model=None):
		response = openai.Completion.create(
			engine=model if model else self.engine_id,
			prompt=prompt,
			**self.params
		)
		self.chat_history = self.chat_history + response.choices[0].text.strip() + "\n"
		print(response.choices[0].text.strip())
		self.write_to_chat_log('AI: ' + response.choices[0].text.strip() + '\n')
		return response

	@staticmethod
	def write_to_chat_log(content):
		with open('this_chat.txt', 'a') as chat_file:
			chat_file.write(content)

	def user_prompt(self):
		if self.first_question:
			prompt = input("Say something to the AI...\n")

			summary = self.generate_response("summarize this into 3-5 words: \n\n" + prompt)
			# Following line generates summary based on prompt
			self.write_to_chat_log("\n\n" + summary.choices[0].text.strip() + "\n")
			self.first_question = False
		else:
			prompt = input("")
		if prompt == 'quit':
			quit()
		elif prompt == 'new':
			self.chat_history = ''
			self.first_question = True
			return
		self.write_to_chat_log('User: ' + prompt + '\n')
		self.chat_history = self.chat_history + 'Human: ' + prompt + "\nAI: "

	def chat_loop(self):
		while True:
			self.user_prompt()
			if not self.first_question:
				self.generate_response(self.chat_history)
			time.sleep(0.5)


if __name__ == "__main__":
	convo = Conversation()
	convo.chat_loop()
