import discord
import os
from dotenv import load_dotenv  # Load environment variables securely

# Load the .env file (if using)
load_dotenv()

intents = discord.Intents.default()  # Define intents
client = discord.Client(intents=intents)  # Pass intents

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$hello'):
        await message.channel.send('Hello! How can I help you today?')

# Fetch the token securely
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
if not TOKEN:
    raise ValueError("No token found! Set DISCORD_BOT_TOKEN in environment variables.")

client.run(TOKEN)  # Run the bot safely

