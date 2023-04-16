#!/usr/bin/python3

import openai

# Set the API key
openai.api_key = "YOUR_OPENAI_API_KEY"

# Maintain a threaded conversation with ChatGPT, sending one message at a time
# and getting a response that takes into account the conversation so far.
class ChatConversation:
  def __init__(self, agentDescription, modelEngine = "gpt-3.5-turbo", temperature=0.7):
      self.agentDescription = agentDescription
      self.modelEngine = modelEngine
      self.temperature = temperature
      self.messages = [{"role": "system", "content": agentDescription}]

  def chat(self, request):
    self.messages.append({"role": "user", "content": request})
    completion = openai.ChatCompletion.create(
            messages = self.messages,
            model=self.modelEngine,
            temperature=self.temperature)

    replyObj = completion['choices'][0]['message']
    reply = None
    if replyObj:
      reply = replyObj['content']
      self.messages.append(replyObj)

    return reply


def example():
  agent=ChatConversation("You are a master of linguistics and children's literature.")
  print(agent.chat("Where in the world is Carmen Lasvegas?"))
  print(agent.chat("I asked about Carmen Lasvegas, not Carmen Sandiego."))
