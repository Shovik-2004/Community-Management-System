import discord
import os
import requests
import json
import random
from dotenv import load_dotenv  # Securely load environment variables
from replit import db  # Replit database

# List of sad words for encouragement
sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]

# Default encouraging messages
starter_encouragements = [
    "Cheer up!",
    "Hang in there.",
    "You are a great person / bot!"
]

# Function to get an inspirational quote
def get_quote():
    try:
        response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        quote = json_data[0]['q'] + " -" + json_data[0]['a']
        return quote
    except Exception as e:
        return f"Error fetching quote: {str(e)}"

# Function to update encouragement messages
def update_encouragements(encouraging_message):
    if "encouragements" in db.keys():
        encouragements = list(db["encouragements"])  # Convert to a normal list
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [encouraging_message]

# Function to delete encouragement messages
def delete_encouragement(index):
    if "encouragements" in db.keys():
        encouragements = list(db["encouragements"])  # Convert to a normal list
        if 0 <= index < len(encouragements):  # Ensure valid index
            del encouragements[index]
            db["encouragements"] = encouragements
            return "Encouragement deleted."
        else:
            return "Invalid index."
    return "No encouragements to delete."

# Load environment variables from .env file
load_dotenv()

# Define intents (message_content must be enabled!)
intents = discord.Intents.default()
intents.message_content = True  

# Initialize bot client with intents
client = discord.Client(intents=intents)

# Bot login event
@client.event
async def on_ready():
    print(f'✅ Logged in as {client.user}')

# Message event listener
@client.event
async def on_message(message):
    if message.author == client.user:
        return  # Ignore bot's own messages

    msg = message.content.lower()  # Convert message to lowercase for better matching

    # Greet the user
    if msg.startswith('$hello'):
        await message.channel.send('Hello! How can I help you today? 😊')

    # Send an inspirational quote
    if msg.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    # Respond with encouragement if message contains a sad word
    if any(word in msg for word in sad_words):
        options = starter_encouragements
        if "encouragements" in db.keys():
            options += list(db["encouragements"])  # Convert to list before concatenation
        await message.channel.send(random.choice(options))

    # Add a new encouragement message
    if msg.startswith("$new"):
        encouraging_message = msg.split("$new ", 1)[1]
        update_encouragements(encouraging_message)
        await message.channel.send("✅ New encouraging message added!")

    # Delete an encouragement message
    if msg.startswith("$del"):
        try:
            index = int(msg.split("$del ", 1)[1])
            result = delete_encouragement(index)
            await message.channel.send(result)
        except ValueError:
            await message.channel.send("⚠️ Please provide a valid number.")

    # Respond to "thanks"
    if "thanks" in msg or "thank you" in msg:
        await message.channel.send("You're welcome! 😊")

# Fetch bot token from environment variable
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Ensure token is set
if not TOKEN:
    raise ValueError("❌ No token found! Set DISCORD_BOT_TOKEN in the .env file.")

# Run the bot
client.run(TOKEN)
