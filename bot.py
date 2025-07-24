import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
from datetime import timedelta
import typing
load_dotenv()
print("Bot launching...")
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print('Bot launched !')
    try:
        synced = await bot.tree.sync()
        print(f"Commandes synchronisées: {len(synced)}")
    except Exception as e:
        print(e)

'''
#Yohon troll :
@bot.event
async def on_message(message: discord.Message):
    if message.content.lower() == 'est ce que yohon est con?':
        channel = message.channel
        await channel.send('Oui !')
'''

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

@bot.tree.command(name='calculate', description='Permet de faire un calcul')
async def calculate(interaction: discord.Interaction, nombre1: int, nombre2: int, operation: str):
    await interaction.response.send_message('test')

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

    return operations[:5]

    

    
bot.run(os.getenv('DISCORD_TOKEN'))