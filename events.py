import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
from datetime import timedelta
import typing

load_dotenv()
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

#Yohon troll :
def setup_events(bot: commands.Bot):

    @bot.event
    async def on_message(message: discord.Message):
        if message.content.lower() == 'est ce que yohon est con?':
            channel = message.channel
            await channel.send('Oui !')


