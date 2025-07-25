import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
from datetime import timedelta
import typing
from events import setup_events

load_dotenv()


class Bot(commands.Bot):
    async def setup_hook(self):
        for extension in ['commands', 'moderation']:
            await self.load_extension(f'cogs.{extension}')

bot = Bot(command_prefix="!", intents=discord.Intents.all())
print("Bot launching...")


@bot.event
async def on_ready():
    print('Bot launched !')
    try:
        synced = await bot.tree.sync()
        print(f"Commandes synchronisées: {len(synced)}")
    except Exception as e:
        print(e)    

if __name__ == '__main__':
    bot.run(os.getenv('DISCORD_TOKEN'))