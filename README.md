# gpt-util
Some utilities to simplify and make the most of Chat GPT

Try `python3 chat_cli.py -c finances` to start a command line conversation with ChatGPT about your finances. Each time you re-run that command, you can send one new message to Chat GPT and it will respond. It remembers prior conversations; the content will be in local/finances

To start a new conversation about your dog Rover, run `python3 chat_cli.py -c rover`

The chat agent (ChatConversation) will notice when it nears the token limit and asks ChatGPT to summarize the conversation so far instead of dropping messages. If you're an expert prompt engineer I'd love PRs (or bug reports) to improve ChatConversation.summarize()
