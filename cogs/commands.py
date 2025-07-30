import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta
import typing



class UsefulCogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    try:
        try:
            @app_commands.command(name='help', description='Affiche les différentes commandes du bot')
            async def help_command(self, interaction: discord.Interaction):
                
                select = discord.ui.Select(
                    placeholder="Choisir une option",
                    options=[
                        discord.SelectOption(label='Modération', description='Voir les commandes de modération', value='embed1'),
                        discord.SelectOption(label='Calcul', description='Voir les commandes de calculs', value='embed2')
                    ]
                )

                embed = discord.Embed(
                    title="Liste des commandes",
                    color = 0x2764ad,
                    )
                
            

                async def select_callback(interaction_select: discord.Interaction):
                    value = select.values[0]
                    if value == "embed1":
                        new_embed = discord.Embed(
                            title='Modération', 
                            description=f'\
                            **/ban** : Permet de bannir un utilisateur\n \
                            **/unban** : Permet de débannir un utilisateur\n \
                            **/timeout** : Permet de timeout un utilisateur\
                            ', 
                            color=0x2764ad
                            )
                    else:
                        new_embed = discord.Embed(
                            title='Calcul', 
                            description=f'\
                            **/calculate** : Permet d\'utiliser la calculatrice\n\
                            **/integrale** : Permet de calculer une intégrale\
                            ', 
                            color= 0x2764ad)
                    await interaction_select.response.edit_message(embed=new_embed, view=view)
                
                select.callback = select_callback
                view = discord.ui.View()
                view.add_item(select)
                
                await interaction.response.send_message(embed=embed, view=view)

        except Exception as e:
            print(f"An error occurred in the help command: {e}")



    
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
                embed.add_field('Erreur lors du calcul !')
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