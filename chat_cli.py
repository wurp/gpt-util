import chat_conversation
import argparse
import json
import os
import tempfile
import pathlib

def parseArgs():
  # Create an ArgumentParser object
  parser = argparse.ArgumentParser()
  
  # Add the --convo argument
  parser.add_argument('--convo', '-c', type=str)
  parser.add_argument('--role', '-r', type=str)

  # Parse the command-line arguments
  return parser.parse_args()

class Convo:
  def __init__(self, system = "You are a helpful assistant.", identifier = None):
    self.system = system
    self.agent = None
    if identifier:
      self.temp_dir = pathlib.Path('local').joinpath(identifier)
      if os.path.isdir(self.temp_dir):
        self.loadConvo()
      else:
        os.mkdir(self.temp_dir)
        self._writeTempFile("system", json.dumps(self.system))
        self.idx = 0
    else: 
      self.temp_dir = tempfile.mkdtemp(dir='local')
      self._writeTempFile("system", json.dumps(self.system))
      self.idx = 0

  def _writeTempFile(self, filename, contents):
    with open(pathlib.Path(self.temp_dir).joinpath(filename), 'w') as f:
      f.write(contents)

  def _readTempFile(self, filename):
    fpath = pathlib.Path(self.temp_dir).joinpath(filename)
    if os.path.isfile(fpath):
      with open(fpath, 'r') as f:
        c = f.read()
        return json.loads(c)
    else:
      return None

  def id(self):
    return os.path.basename(self.temp_dir)

  def createChatConversation(self):
    if not self.agent:
      self.agent = chat_conversation.ChatConversation(self.system)
    return self.agent

  def addExchange(self, exchange):
    self._writeTempFile(str(self.idx), json.dumps(exchange))

  def loadConvo(self):
      system = self._readTempFile("system")
      if system: self.system = system

      self.createChatConversation()

      self.idx = 0
      while True:
        arr = self._readTempFile(str(self.idx))
        if arr:
          self.agent.replayObj(arr[0], arr[1])
          self.idx = self.idx + 1
        else:
          break

def main():
  args = parseArgs()
  if args.convo:
    convo = Convo(identifier=args.convo)
    agent = convo.createChatConversation()
    latestExchange = agent.getLatestExchange()
    if latestExchange and len(latestExchange) > 0:
      print("You last said to me: " + agent.asMessage(latestExchange[0])['content'])
      print("and I replied: " + agent.asMessage(latestExchange[1])['content'])
  else:
    system = args.role
    convo = Convo(system) 
    print("Conversation id: " + convo.id())

  agent = convo.createChatConversation()

  request = input("> ")
  print(agent.chat(request))

  convo.addExchange(agent.getLatestExchange())

if __name__ == "__main__":
    main()
