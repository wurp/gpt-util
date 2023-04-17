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
  def __init__(self, system, identifier = None):
    self.system = system
    self.identifier = identifier
    self.temp_dir = tempfile.mkdtemp(dir='local')
    self._writeTempFile("system", json.dumps(self.system))
    self.idx = 0

  def _writeTempFile(self, filename, contents):
    with open(pathlib.Path(self.temp_dir).joinpath(filename), 'w') as f:
      f.write(contents)

  def id(self):
    return os.path.basename(self.temp_dir)

  def createChatConversation(self):
    return chat_conversation.ChatConversation(self.system)

  def addExchange(self, exchange):
    self._writeTempFile(str(self.idx), json.dumps(exchange))

def loadConvo(convoId):
  #TODO actually load the conversation from the directory
  return Convo("You are a helpful assistant.")

def main():
  args = parseArgs()
  if args.convo:
    convo = loadConvo(args.convo)
  else:
    system = args.role if args.role else "You are a helpful assistant."
    convo = Convo(system) 
    print("Conversation id: " + convo.id())

  agent = convo.createChatConversation()

  request = input("> ")
  print(agent.chat(request))

  convo.addExchange(agent.getLatestExchange())

if __name__ == "__main__":
    main()
