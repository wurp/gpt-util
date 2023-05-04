#!/usr/bin/python3

import openai
import re
import sys

try:
  import pii
except ImportError as impErr:
    print("Copy pii.py.template to pii.py and edit it to add your key")
    #print("[Error]: Failed to import (Import Error) {}.".format(impErr.args[0]))
    sys.exit(1)

# Set the API key
openai.api_key = pii.openai_api_key

## Actual max tokens for gpt-3.5-turbo is 4096, but let's summarize before
# Actual max tokens for gpt-4 is 8192, but let's summarize before
# we get too close. Note that if a single request takes up 1192 tokens
# this will overflow.
#MAX_TOKENS_BEFORE_SUMMARY=110
#MAX_TOKENS_AFTER_SUMMARY=80
MAX_TOKENS_BEFORE_SUMMARY=7000
MAX_TOKENS_AFTER_SUMMARY=4000

#Valid modelEngines:
# 'gpt-3.5-turbo'
# 'gpt-4'

# Maintain a threaded conversation with ChatGPT, sending one message at a time
# and getting a response that takes into account the conversation so far.
class ChatConversation:
  def __init__(self, agentDescription = "You are a helpful assistant.", modelEngine = 'gpt-4', temperature=0.7):
    self.agentDescription = agentDescription
    self.modelEngine = modelEngine
    self.temperature = temperature
    self.messages = [{'role': 'system', 'content': agentDescription}]
    self.totalTokens = 0

  def asMessage(self, m):
    if 'role' in m:
      return m
    #else it's a full response object from ChatGPT, slice out the bit we want
    else:
      return m['choices'][0]['message']

  def chat(self, request):
    self.summarizeAsNeeded()

    self.messages.append({'role': 'user', 'content': request})
    completion = openai.ChatCompletion.create(
            messages = [self.asMessage(m) for m in self.messages],
            model=self.modelEngine,
            temperature=self.temperature)
    self.messages.append(completion)
    self.totalTokens = completion['usage']['total_tokens']

    replyObj = completion['choices'][0]['message']
    reply = None
    if replyObj:
      reply = replyObj['content']

    return reply

  def summarizeAsNeeded(self):
    if self.totalTokens > MAX_TOKENS_BEFORE_SUMMARY:
      summary = self.summarize()
      self.messages = [{'role': 'system', 'content': self.agentDescription}]
      self.messages.append({'role': 'assistant', 'content': summary})
      print("Summary: " + summary)

  def convo(self):
      return self.messagesToString(self.messages)

  def messagesToString(self, messages):
      simpleMessages = [self.asMessage(m) for m in messages if 'role' not in m or m['role'] != 'system']
      return "\n\n".join([m['role'] + " said: \"" + m['content'] + "\"\n" for m in simpleMessages])

  def summarize(self):
    prevMessages = self.convo()
    messages = [{'role': 'system', 'content': "You write Cliff's Notes for LLMs, but with no concern for grammar, only brevity."}]
    messages.append({
        'role': 'user',
        'content': "Provide an overview of the following conversation in as many as "
        + str(MAX_TOKENS_AFTER_SUMMARY) + " words. Include all important details, but you're just making notes for yourself; they can be quite cryptic as long as you'll understand them.\n\n" + prevMessages}
        )
    completion = openai.ChatCompletion.create(
            messages = messages,
            model=self.modelEngine,
            temperature=self.temperature)

    replyObj = completion['choices'][0]['message']
    return replyObj['content'] if replyObj else None

  # Pretend you had an exchange with the agent
  def replayObj(self, request, reply):
    self.messages.append(request)
    self.messages.append(reply)
    if 'usage' in reply:
      self.totalTokens = reply['usage']['total_tokens']
      self.summarizeAsNeeded()

  # Pretend you had an exchange with the agent
  def replay(self, request, reply):
    self.replayObj(
            {'role': 'user', 'content': request},
            {'role': 'assistant', 'content': reply})

  def getLatestExchange(self):
    if len(self.messages) > 1:
      return [self.messages[-2], self.messages[-1]]

def example():
  agent=ChatConversation("You are a master of linguistics and children's literature.")
  print(agent.chat("Where in the world is Carmen Lasvegas?"))
  print(agent.chat("I asked about Carmen Lasvegas, not Carmen Sandiego."))
  print(agent.chat("Can you invent a story about Carmen Lasvegas?"))
  #print("\n\nAgent after convo: " + agent.convo())

if __name__ == "__main__":
    example()
