import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands


load_dotenv()

try:
    class Bot(commands.Bot):
        async def setup_hook(self):
            for extension in ['commands', 'moderation', 'owner']:
                await self.load_extension(f'cogs.{extension}')

    bot = Bot(command_prefix="*", intents=discord.Intents.all())
    print("----Bot launching----")


    @bot.event
    async def on_ready():
        print('----Bot launched----')
        try:
            synced = await bot.tree.sync()
            print(f"Synchronised commands: {len(synced)}")
        except Exception as e:
            print(e)    


    if __name__ == '__main__':
        bot.run(os.getenv('DISCORD_TOKEN'))

except Exception as e:
    print(e)
    print("An error occurred while launching the bot.")