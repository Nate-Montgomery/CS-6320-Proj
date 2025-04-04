import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio  # Import asyncio to handle asynchronous tasks

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

# Enable intents, including message content
intents = discord.Intents.default()
# intents.message_content = True

# Create the bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.sync_commands()  # Sync commands with Discord
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    print("Bot is ready and connected to Discord!")

# Asynchronous function to load cogs
for filename in os.listdir('./bot/cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')  # Await the coroutine

bot.run(TOKEN)  # Start the bot
