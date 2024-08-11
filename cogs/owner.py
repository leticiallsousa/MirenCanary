import discord
from discord.ext import commands
from discord import app_commands
from utils.utils import *

class Owner(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx: commands.Context):
        synced= await self.client.tree.sync()
        embed = discord.Embed(description=f'{emoji["positive"]} Synced {len(synced)} app commands to the current guild.', colour=discord.Colour(0x070d2d))
        await ctx.reply(embed=embed, mention_author=False) 

    @commands.command()
    @commands.is_owner()
    async def servers(self, ctx: commands.Context):
        guilds = ''
        for guild in self.client.guilds:
            guilds += f'\n`{guild.name}` - `{guild.id}`'
        await ctx.reply(guilds, mention_author=False)
            

async def setup(client):
    await client.add_cog(Owner(client))