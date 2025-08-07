import os
from urllib import response
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
        if message.content.startswith("gpt:"):
            prompt = message.content[4:].strip()
            user_id = message.author.id
            
            if message.attachments:
                image = message.attachments[0]
                image_url = image.url

                try:
                    response = self.client.chat.completions.create(
                        model="o4-mini-2025-04-16",
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
                    
                    #Logger
                    print("=== GPT IMAGE RESPONSE ===")
                    print(f"Model utilisé : {response.model}")
                    print(f"Tokens (prompt) : {response.usage.prompt_tokens}")
                    print(f"Tokens (réponse) : {response.usage.completion_tokens}")
                    print(f"Tokens (total) : {response.usage.total_tokens}")
                    

                except Exception as e:
                    await message.channel.send(f"Error: {e}")
                    print(e)
                return
            else:
                
                # History management
                history = self.histories.get(user_id, [])
                history.append({"role": "user", "content": prompt})
                try:
                    response = self.client.chat.completions.create(
                        model="o4-mini-2025-04-16",
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
                    self.histories[user_id] = history[-10:]  
                    
                    #Logger
                    print("=== GPT TEXT RESPONSE ===")
                    print(f"Model utilisé : {response.model}")
                    print(f"Tokens (prompt) : {response.usage.prompt_tokens}")
                    print(f"Tokens (réponse) : {response.usage.completion_tokens}")
                    print(f"Tokens (total) : {response.usage.total_tokens}")
                
                except Exception as e:
                    await message.channel.send(f"Error : {e}")
                    print(e)
            
            

async def setup(bot):
    await bot.add_cog(ChatGPTCog(bot))