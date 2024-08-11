import discord
from discord.ext import commands
from discord import app_commands
from utils.utils import *
import random

class Fun(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.hybrid_command(name='8ball', description='Make a question to the magic 8ball')
    @app_commands.describe(question='The question you want to be answered')
    async def _8ball(self, ctx: commands.Context, *, question: str):
        answers = [
            "It is certain", "It is decidedly so", "Without a doubt", "Yes definitely", "You may rely on it",
            "As I see it, yes", "Most likely", "Outlook good", "Yes", "Signs point to yes", 
            "Reply hazy, try again", "Ask again later", "Better not tell you now", "Cannot predict now", 
            "Concentrate and ask again", "Don't count on it", "My reply is no", "My sources say no", 
            "Outlook not so good", "Very doubtful"
        ]
        embed = discord.Embed(description=f'{emoji["8ball"]} {random.choice(answers)}.',  colour=discord.Colour(0x070d2d))  
        embed.set_author(name=f'{ctx.author.display_name}: {question}', icon_url=ctx.author.display_avatar.url)                                   
        await ctx.reply(embed=embed, mention_author=False)
        
async def setup(client):
    await client.add_cog(Fun(client))