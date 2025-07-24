import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta
import typing

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

#Help command
@bot.tree.command(name='help', description='Affiche les différentes commandes du bot')
async def help(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Liste des commandes",
        color = 0x2764ad
        )
    embed.insert_field_at(0, name='Modération', value='test')

    await interaction.response.send_message(embed=embed)



operation_list = {
    '+': 'Addition',
    '-': 'Soustraction',
    '*': 'Multiplication',
    '/': 'Division'
}

#Calculator command
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

slash_commands = [help, calculate]
def setup_commands(bot: discord.ext.commands.Bot):
    for command in slash_commands:
        bot.tree.add_command(command)