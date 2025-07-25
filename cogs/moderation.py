import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta
import typing


class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    #Commande for ban
    @app_commands.command(name='ban', description='Permet de bannir un membre')
    @app_commands.default_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, raison: str='Aucune raison n\'a été fournie'):
        embed = discord.Embed(
            title='Bannissement',
            color= 0xb02b20
        )
        embed.add_field(name='Membre\n', value=f'{member}',inline=True)
        embed.add_field(name='Raison:\n', value=f'{raison}', inline=True)
        await member.ban(reason=raison)
        await interaction.response.send_message(embed=embed)


    #Command for unban
    @app_commands.default_permissions(ban_members=True)
    @app_commands.command(name ='unban', description='Permet de débannir un membre')
    async def unban(self, interaction: discord.Interaction, user: discord.User, raison: str='Aucune raison n\'a été fournie'):
        embed = discord.Embed(
            title='Débannissement',
            color= 0xb02b20
        )
        embed.add_field(name='Membre\n', value=f'{user.name}',inline=True)
        embed.add_field(name='Raison:\n', value=f'{raison}', inline=True)
        await interaction.guild.unban(user, reason=raison)
        await interaction.response.send_message(embed=embed)
        

    #Command for timeout
    @app_commands.default_permissions(moderate_members=True)
    @app_commands.command(name='timeout', description='Permet de timeout un membre')
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, minutes: int, raison: str='Aucune raison n\'a été fournie'):
        duration = timedelta(minutes=minutes)
        await member.timeout(duration, reason=raison)
        embed = discord.Embed(
            title='Timeout',
            color= 0xb02b20
        )
        embed.add_field(name='Membre\n', value=f'{member}')
        embed.add_field(name='Durée:\n', value=f'{duration} minutes')
        embed.add_field(name='Raison:\n', value=f'{raison}')
        await interaction.response.send_message(embed=embed)
    


async def setup(bot):
    await bot.add_cog(ModerationCog(bot))

