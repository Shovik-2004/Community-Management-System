import discord
import os
from dotenv import load_dotenv  # Securely load environment variables
import requests
import json

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote
    

# Load the .env file (if using)
load_dotenv()

# Define intents & enable message_content for message reading
intents = discord.Intents.default()
intents.message_content = True  

client = discord.Client(intents=intents)  # Pass intents

@client.event
async def on_ready():
    print(f'✅ Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return  # Ignore messages from the bot itself

    if message.content.startswith('$hello'):
        await message.channel.send('Hello! How can I help you today?')
    if message.content.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)

# Fetch the token securely from .env
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

if not TOKEN:
    raise ValueError("❌ No token found! Set DISCORD_BOT_TOKEN in the .env file.")

# Run the bot
client.run(TOKEN)
