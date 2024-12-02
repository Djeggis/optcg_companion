from dotenv import load_dotenv
import discord
import os

import openai
from app.deck2vec import d2v as d2v

load_dotenv()

discord_token = os.getenv('DISCORD_TOKEN')
openai.api_key = os.getenv('CHATGPT_API_KEY')

# setup discord client
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

    # openai model as card game assistnat
    async def card_assistant(prompt):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a card game assistant helping users optimize their decks."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"Error: {str(e)}"
    
    # bot commands
    async def suggest(ctx, *, user_decklist: str):
        # compare a user's decklist to averages and suggest changes
        try:
            # Parse the user's decklist
            user_deck = d2v.deck_to_data(user_decklist)

            # Generate suggestions
            suggestions = d2v.suggestion(user_deck)
            if suggestions:
                await ctx.send("\n".join(suggestions))
            else:
                await ctx.send("Your deck matches the averages perfectly!")
        except Exception as e:
            await ctx.send(f"Error processing your decklist: {str(e)}")

    
intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)