import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
from datetime import timedelta
import typing

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.tree.command(name='help', description='Affiche les différentes commandes du bot')
async def help(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Liste des commandes",
        color = 0x2764ad
        )
    embed.insert_field_at(0, name='Modération', value='test')

    await interaction.response.send_message(embed=embed)

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

@app_commands.default_permissions(ban_members=True)
@bot.tree.command(name ='unban', description='Permet de débannir un membre')
async def unban(interaction: discord.Interaction, user: discord.User, raison: str='Aucune raison n\'a été fournie'):
    await interaction.guild.unban(user, reason=raison)
    await interaction.response.send_message(f'{user.name} a été débanni !\n Raison: {raison}')

@app_commands.default_permissions(moderate_members=True)
@bot.tree.command(name='timeout', description='Permet de timeout un membre')
async def timeout(interaction: discord.Interaction, member: discord.Member, minutes: int, raison: str='Aucune raison n\'a été fournie'):
    duration = timedelta(minutes=minutes)
    await member.timeout(duration, reason=raison)
    await interaction.response.send_message(f'{member} a été exclu !\n Raison:{raison}')

operation_list = {
    '+': 'Addition',
    '-': 'Soustraction',
    '*': 'Multiplication',
    '/': 'Division'
}

@bot.tree.command(name='calculate', description='Permet de faire un calcul entre deux nombres entiers')
async def calculate(interaction: discord.Interaction, nombre1: int, nombre2: int, operation: str):
    try:
        embed = discord.Embed(
            title = 'Calcul',
            color = 0x17E81F,
        )
        Titre = ''
        result = None
        if operation == '+':
            result = nombre1 + nombre2
            Titre = 'Addition'
        elif operation == '-':
            result = nombre1 - nombre2
            Titre = 'Soustraction'
        elif operation == '*':
            result = nombre1 * nombre2
            Titre = 'Multiplication'
        elif operation == '/':
            if nombre2 == 0:
                Titre = 'Erreur !'
                embed.color = 0xA60F0F
                embed.add_field(name=Titre, value='Division par zéro impossible !')
                await interaction.response.send_message(embed=embed)
                return
            result = nombre1 / nombre2
            Titre = 'Division'
        embed.add_field(name=Titre, value=f'**{nombre1}** **{operation}** **{nombre2}**')
        embed.add_field(name='Résultat', value=f'**{result}**')
        await interaction.response.send_message(embed=embed) 
    except Exception as e:
        embed = discord.Embed(
            titre = 'Calcul',
            color = 0xA60F0F
        )
        embed.add_field('Erreur lors du calcul !')
        await interaction.response.send_message(embed=embed, ephemeral=True)
        print(e)
    

@calculate.autocomplete('operation')
async def operation_autocomplete(
    interaction:discord.Interaction,
    current: str
)-> typing.List[app_commands.Choice[str]]:
    operations = []
    for operation_sign, desc in operation_list.items():
        if current.lower() in operation_sign.lower():
            operations.append(app_commands.Choice(name=f'{operation_sign} ➜ {desc}', value=operation_sign))
    
    if not operations:
        operations = [
            app_commands.Choice(name=f'{operation_sign} ➜ {desc}', value=operation_sign)
            for operation_sign, desc in operation_list.items()
            ]

    await interaction.response.autocomplete(operations[:25])

slash_commands = [help, timeout, ban, unban, calculate]
def setup_commands(bot: discord.ext.commands.Bot):
    for command in slash_commands:
        bot.tree.add_command(command)