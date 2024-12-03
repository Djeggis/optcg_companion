from dotenv import load_dotenv
import discord
import os

from openai import OpenAI
from app.deck2vec import d2v as d2v

load_dotenv()

discord_token = os.getenv('DISCORD_TOKEN')

openai = OpenAI()

# setup discord client
class MyClient(discord.Client):
    async def on_ready(self):
        print("Successfully logged in as: ", self.user)    
    
    async def on_message(self, message):
        print(message.content)
        if message.author == self.user:
            return
        command, userMessage = None, None

        bot_commands = ['/ai', '/bot', 'chatgpt', '/suggest']

        for text in bot_commands:
            if message.content.startswith(text):
                command = message.content.split(' ')[0]
                userMessage = message.content.replace(text, '')
                print(command, userMessage)
        
        if command == '/ai' or command == '/bot' or command == '/chatgpt':
            bot_response = await self.card_assistant(prompt=userMessage)

            if len(bot_response) > 1500:
                # Split the content into chunks of 2000 characters or less
                while len(bot_response) > 1500:
                    await message.channel.send(f"Answer: {bot_response[:1500]}")
                    bot_response = bot_response[1500:]  # Update content to the next chunk

                # Send the remaining part (if any) of the content
                await message.channel.send(f"Answer: {bot_response}")

            else:
                # If the content is within the limit, send it in one message
                await message.channel.send(f"Answer: {bot_response}")

        if command == 'suggest':
            bot_response = await self.suggest(user_decklist=userMessage)

            if len(bot_response) > 1500:
                # Split the content into chunks of 2000 characters or less
                while len(bot_response) > 1500:
                    await message.channel.send(f"Answer: {bot_response[:1500]}")
                    bot_response = bot_response[1500:]  # Update content to the next chunk

                # Send the remaining part (if any) of the content
                await message.channel.send(f"Answer: {bot_response}")

            else:
                # If the content is within the limit, send it in one message
                await message.channel.send(f"Answer: {bot_response}")

    # openai model as card game assistnat
    async def card_assistant(self, prompt):
        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a card game assistant helping users optimize their One Piece TCG decks."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error: {str(e)}"
    
    # bot commands
    async def suggest(user_decklist):

        # compare a user's decklist to averages and suggest changes
        try:
            # Parse the user's decklist
            user_deck = d2v.deck_to_data(user_decklist)

            # Generate suggestions
            return d2v.suggestion(user_deck)
        except Exception as e:
            await ctx.send(f"Error processing your decklist: {str(e)}")

    
intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)