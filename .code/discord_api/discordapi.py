from dotenv import load_dotenv
import discord
import os

load_dotenv()

discord_token = os.getenv('DISCORD_TOKEN')

class MyClient(discord.Client):
    async def on_ready(self):
        print("Successfully logged in as: ", self.user)
    
    async def on_message(self, message):
        print(message.content)
        if message.author == self.user:
            return
        command, userMessage = None, None

        for text in ['/ai', '/bot', 'chatgpt']:
            if message.content.startswith(text):
                command = message.content.split(' ')[0]
                userMessage = message.content.replace(text, '')
                print(command, userMessage)
        
        if command == '/ai' or command == '/bot' or command == '/chatgpt':
            bot_response = chatgpt_response(prompt=userMessage)
            await message.channel.send(f"Answer: {bot_response}")

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)