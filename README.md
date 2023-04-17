# gpt-util
Some utilities to simplify and make the most of Chat GPT

Try:
  python3 chat_cli.py -c finances
To start a command line conversation with ChatGPT about your finances. Each time you re-run that command, you can send one new message to Chat GPT and it will respond. It remembers prior conversations; the content will be in local/finances

The chat agent (ChatConversation) will also notice when it nears the token limit and asks ChatGPT to summarize the conversation so far instead of dropping messages. If you're an expert prompt engineer I'd love PRs to improve ChatConversation.summarize()
