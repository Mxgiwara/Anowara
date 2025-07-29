import os
import openai
import discord
from discord.ext import commands

class ChatGPTCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.histories = {}  # {user_id: [ {"role": "user", ...}, {"role": "assistant", ...}, ... ] }

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        # Parle seulement si le message commence par "gpt:" (par exemple)
        if message.content.startswith("gpt:"):
            prompt = message.content[4:].strip()
            user_id = message.author.id
            # Récupère ou crée l'historique
            history = self.histories.get(user_id, [])
            history.append({"role": "user", "content": prompt})
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=history,
                    max_tokens=500
                )
                answer = response.choices[0].message.content
                embed = discord.Embed(
                    title="GPT Response",
                    description=answer,
                    color=discord.Color.blue()
                )
                await message.channel.send(embed=embed)
                history.append({"role": "assistant", "content": answer})
                self.histories[user_id] = history[-10:]  # Garde les 10 derniers échanges
            except Exception as e:
                await message.channel.send("Erreur avec ChatGPT.")
                print(e)
            if message.attachments:
                image = message.attachments[0]
                image_url = image.url

                try:
                    # Appel à GPT-4 Vision
                    response = self.client.chat.completions.create(
                        model="gpt-4.1-mini",
                        messages=[
                            {"role": "user", "content": [
                                {"type": "text", "text": prompt},
                                {"type": "image_url", "image_url": {"url": image_url}}
                            ]}
                        ],
                        max_tokens=1000
                    )
                    answer = response.choices[0].message.content
                    embed = discord.Embed(
                        title="GPT Response",
                        description=answer,
                        color=discord.Color.purple()
                    )
                    await message.channel.send(embed=embed)

                except Exception as e:
                    await message.channel.send("Erreur lors de l’analyse de l’image.")
                    print(e)
                return

async def setup(bot):
    await bot.add_cog(ChatGPTCog(bot))