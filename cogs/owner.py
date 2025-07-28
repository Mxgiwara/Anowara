import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands

class OwnerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="stop", help="Owner only command to stop the bot")
    async def stop(self, ctx):
        try:
            if not ctx.author.id == int(os.getenv('OWNER_ID')):
                await ctx.send("Get the fuck out")
                print(f'{ctx.author.name} ({ctx.author.id}) tried to stop the bot.')
                return
            await ctx.send("Bot shutdown...")
            await self.bot.close()
            print("----Bot stopped----")
            
        except Exception as e:
            await ctx.send("Une erreur s'est produite lors de l'arrêt du bot.")
            print(f"An error occurred in the stop command: {e}")    
    @commands.command(name="ping", help="Display the latency")
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)
        await ctx.send(f"Latency: {latency}ms")

async def setup(bot):
    await bot.add_cog(OwnerCommands(bot))
    print("OwnerCommands cog loaded successfully.")
