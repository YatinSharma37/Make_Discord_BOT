import discord
import os
import cohere

token = os.environ['SECRET_KEY']
cohere_api_key = os.environ['COHERE_API_KEY']

co = cohere.Client(cohere_api_key)

CHAT_FILE = "chat.txt"

def append_chat_to_file(content):
    with open(CHAT_FILE, 'a') as f:
        f.write(content + "\n")

def read_chat_history():
    if os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, 'r') as f:
            return f.readlines()
    return []

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f"Received message: {message.content}")

        if self.user != message.author:
            if self.user in message.mentions:
                channel = message.channel

                append_chat_to_file(f"{message.author}: {message.content}")

                chat_history = read_chat_history()[-10:]

                combined_chat = "".join(chat_history)

                try:
                    response = co.generate(
                        model='command-xlarge-nightly',
                        prompt=combined_chat,
                        max_tokens=300,
                        temperature=0.75
                    )

                    messagetoSend = response.generations[0].text

                    append_chat_to_file(f"Bot: {messagetoSend}")

                    await channel.send(messagetoSend)

                except Exception as e:
                    await channel.send(f"Error: {e}")

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(token)
