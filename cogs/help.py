import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta
import typing

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    try:
        @app_commands.command(name='help', description='Affiche les différentes commandes du bot')
        async def help_command(self, interaction: discord.Interaction, command: str=None):
            if command == 'ban':
                embed = discord.Embed(
                    title='Commande: /ban',
                    description='Bannir un utilisateur du serveur.',
                    color=0x2764ad
                )
                await interaction.response.send_message(embed=embed)
                return
            
            elif command == 'unban':
                embed = discord.Embed(
                    title='Commande: /unban',
                    description='Débannir un utilisateur du serveur.',
                    color=0x2764ad
                )
                await interaction.response.send_message(embed=embed)
                return
            
            elif command == 'timeout':
                embed = discord.Embed(
                    title='Commande: /timeout',
                    description='Mettre un utilisateur en timeout pour une durée spécifiée.',
                    color=0x2764ad
                )
                await interaction.response.send_message(embed=embed)
                return
            
            elif command == 'calculate':
                embed = discord.Embed(
                    title='Commande: /calculate',
                    description='Effectuer un calcul entre deux nombres.',
                    color=0x2764ad
                )
                await interaction.response.send_message(embed=embed)
                return
            
            elif command == 'integrale':
                embed = discord.Embed(
                    title='Commande: /integrale',
                    description='Calculer une intégrale.',
                    color=0x2764ad
                )
                await interaction.response.send_message(embed=embed)
                return
            
            else:
                select = discord.ui.Select(
                    placeholder="Choisir une option",
                    options=[
                        discord.SelectOption(label='Modération', description='Voir les commandes de modération', value='mod'),
                        discord.SelectOption(label='Calcul', description='Voir les commandes de calculs', value='calc')
                    ]
                )

                embed = discord.Embed(
                    title="Liste des commandes",
                    color = 0x2764ad,
                    )
                
            

                async def select_callback(interaction_select: discord.Interaction):
                    value = select.values[0]
                    if value == "mod":
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

    @help_command.autocomplete('command')
    async def help_command_autocomplete(
        self,
        interaction:discord.Interaction,
        current: str
    )-> typing.List[app_commands.Choice[str]]:
        
        help_list = {
            'ban': 'Bannir un utilisateur',
            'unban': 'Débannir un utilisateur',
            'timeout': 'Timeout un utilisateur',
            'calculate': 'Utiliser la calculatrice',
            'integrale': 'Calculer une intégrale'
        }

        commands = []
        for command, desc in help_list.items():
            if current.lower() in command.lower():
                commands.append(app_commands.Choice(name=f'({command}) : {desc}', value=command))
        
        if not commands:
            commands = [
                app_commands.Choice(name=f'({command}) : {desc}', value=command)
                for command, desc in help_list.items()
                ]

        return commands[:25]
        
async def setup(bot):
    await bot.add_cog(HelpCog(bot))
    print("HelpCog loaded successfully.")
