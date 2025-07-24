import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta
import typing
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

#Commande for ban
@bot.tree.command(name='ban', description='Permet de bannir un membre')
@app_commands.default_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, raison: str='Aucune raison n\'a été fournie'):
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
@bot.tree.command(name ='unban', description='Permet de débannir un membre')
async def unban(interaction: discord.Interaction, user: discord.User, raison: str='Aucune raison n\'a été fournie'):
    await interaction.guild.unban(user, reason=raison)
    await interaction.response.send_message(f'{user.name} a été débanni !\n Raison: {raison}')
       

#Command for timeout
@app_commands.default_permissions(moderate_members=True)
@bot.tree.command(name='timeout', description='Permet de timeout un membre')
async def timeout(interaction: discord.Interaction, member: discord.Member, minutes: int, raison: str='Aucune raison n\'a été fournie'):
    duration = timedelta(minutes=minutes)
    await member.timeout(duration, reason=raison)
    await interaction.response.send_message(f'{member} a été timeout !\n Durée: {minutes} minutes.\n Raison:{raison}')
       
slash_commands = [ban, unban, timeout]

def setup_moderation_commands(bot: discord.ext.commands.Bot):
    for command in slash_commands:
        bot.tree.add_command(command)

