import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
from datetime import timedelta
import typing
from commands import setup_commands
from events import setup_events

load_dotenv()
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
setup_events(bot)


print("Bot launching...")

@bot.event
async def on_ready():
    print('Bot launched !')
    try:
        setup_commands(bot)
        synced = await bot.tree.sync()
        print(f"Commandes synchronisées: {len(synced)}")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    bot.run(os.getenv('DISCORD_TOKEN'))