import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta
import typing



class UsefulCogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    try:
           
        #Calculator command
        @app_commands.command(name='calculate', description='Permet de faire un calcul entre deux nombres')
        async def calculate(self, interaction: discord.Interaction, nombre1: float, nombre2: float, operation: str):
            try:
                embed = discord.Embed(
                    title = 'Calcul',
                    color = 0x17E81F,
                )
                titre = ''
                result = None
                if operation == '+':
                    result = nombre1 + nombre2
                    titre = 'Addition'
                elif operation == '-':
                    result = nombre1 - nombre2
                    titre = 'Soustraction'
                elif operation == '*':
                    result = nombre1 * nombre2
                    titre = 'Multiplication'
                elif operation == '/':
                    if nombre2 == 0:
                        titre = 'Erreur !'
                        embed.color = 0xA60F0F
                        embed.add_field(name=titre, value='Division par zéro impossible !')
                        await interaction.response.send_message(embed=embed)
                        return
                    result = nombre1 / nombre2
                    titre = 'Division'
                embed.add_field(name=titre, value=f'**{nombre1}** **{operation}** **{nombre2}**')
                embed.add_field(name='Résultat', value=f'**{result}**')
                await interaction.response.send_message(embed=embed) 
            except Exception as e:
                embed = discord.Embed(
                    title = 'Calcul',
                    color = 0xA60F0F
                )
                embed.add_field(name='Erreur', value='Une erreur est survenue lors du calcul. Veuillez vérifier les valeurs saisies et l\'opération choisie.', inline=False)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                print(e)
            

        @calculate.autocomplete('operation')
        async def operation_autocomplete(
            self,
            interaction:discord.Interaction,
            current: str
        )-> typing.List[app_commands.Choice[str]]:
            
            operation_list = {
            '+': 'Addition',
            '-': 'Soustraction',
            '*': 'Multiplication',
            '/': 'Division'
                }

            operations = []
            for operation_sign, desc in operation_list.items():
                if current.lower() in operation_sign.lower():
                    operations.append(app_commands.Choice(name=f'({operation_sign}) {desc}', value=operation_sign))
            
            if not operations:
                operations = [
                    app_commands.Choice(name=f'({operation_sign}) {desc}', value=operation_sign)
                    for operation_sign, desc in operation_list.items()
                    ]

            return operations[:25]

    except Exception as e:
        print(f"An error occurred in the UsefulCogs: {e}")

async def setup(bot):
    await bot.add_cog(UsefulCogs(bot))
    print("UsefulCogs loaded successfully.")