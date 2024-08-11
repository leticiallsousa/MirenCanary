import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional
from creator_en.embed_creator import EmbedCreator
from typing import Optional
from utils.utils import *

class Administration(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command(name=f'prefix', description='Changes the bot\'s prefix on the server; displays the current prefix if no argument is provided')
    @app_commands.describe(new_prefix=f'New prefix')
    @commands.has_guild_permissions(manage_guild=True)
    async def prefix(self, ctx: commands.Context, new_prefix: Optional[str]):
        with open('utils\guilds_data.json', 'r') as f:
            data = json.load(f)

        current_prefix = data["guilds"][str(ctx.guild.id)]["prefix"]
        if new_prefix:
            if len(new_prefix) > 5:
                embed = discord.Embed(description=f'{emoji["negative"]} Prefix length cannot exceed 5 characters!', colour=discord.Colour(0x070d2d))
                return await ctx.reply(embed=embed, mention_author=False)
            data["guilds"][str(ctx.guild.id)]["prefix"] = new_prefix
            with open('utils\guilds_data.json', 'w') as f:
                json.dump(data, f, indent=4)
            embed = discord.Embed(description=f'{emoji["positive"]} Prefix successfully changed to: `{new_prefix}`', colour=discord.Colour(0x070d2d))
            await ctx.reply(embed=embed, mention_author=False)
        else:
            embed = discord.Embed(description=f'{emoji["info"]} The current prefix for this server is: `{current_prefix}`', colour=discord.Colour(0x070d2d))
            await ctx.reply(embed=embed, mention_author=False)

    @commands.hybrid_group(name='create', description='Creates a text or voice channel, category, thread or event with a name provided by the user')
    async def create(self, ctx: commands.Context):
        embed = discord.Embed(title='Commands:', description='- create textchannel `<name>`\n- create voicechannel `<name>`\n- create category `<name>`', colour=discord.Colour(0x070d2d))
        await ctx.reply(embed=embed, mention_author=False)
    
    @create.command(name='textchannel', description='Creates a text channel with a name provided by the user')
    @app_commands.describe(name='New text channel\'s name')
    @commands.has_guild_permissions(manage_channels=True)
    async def textchannel(self, ctx: commands.Context, name: str):
        name = name or 'newtextchannel'
        newtextc = await ctx.guild.create_text_channel(name=name)
        embed = discord.Embed(description=f'{emoji["positive"]}Text channel {newtextc.mention} was successfully created', colour=discord.Colour(0x070d2d))
        await ctx.reply(embed=embed, mention_author=False)
    
    @create.command(name='voicechannel', description='Creates a voice channel with a name provided by the user')
    @app_commands.describe(name='New voice channel\'s name')
    @commands.has_guild_permissions(manage_channels=True)
    async def voicechannel(self, ctx: commands.Context, name: str):
        name = name or 'newvoicechannel'
        newvoicec = await ctx.guild.create_voice_channel(name=name)
        embed = discord.Embed(description=f'{emoji["positive"]} Voice channel {newvoicec.mention} was successfully created', colour=discord.Colour(0x070d2d))
        await ctx.reply(embed=embed, mention_author=False)
    
    @create.command(name='category', description='Creates a category with a name provided by the user')
    @app_commands.describe(name='New category\'s name')
    @commands.has_guild_permissions(manage_channels=True)
    async def category(self, ctx: commands.Context, name: str):
        name = name or 'newcategory'
        newcategory = await ctx.guild.create_category(name=name)
        embed = discord.Embed(description=f'{emoji["positive"]} Category {newcategory.mention} was successfully created', colour=discord.Colour(0x070d2d))
        await ctx.reply(embed=embed, mention_author=False)
    
    @commands.hybrid_command(name='clear', description='Purges the provided amount of messages from the current text channel')
    @app_commands.describe(amount='The amount of messages you want to purge')
    @commands.has_guild_permissions(manage_messages=True)
    async def clear(self, ctx: commands.Context, amount: int):
        if 1000 < amount or amount < 2:
            embed = discord.Embed(description=f'{emoji["negative"]} I can only delete from 2 to 1000 messages!', colour=discord.Colour(0x070d2d))
            return await ctx.reply(embed=embed, mention_author=False)
        await ctx.reply('Deleting...', mention_author=False) 
        purged = await ctx.channel.purge(limit=amount+1)
        embed = discord.Embed(description=f'{emoji["positive"]} Purged {len(purged)-1} messages successfully.', colour=discord.Colour(0x070d2d))
        await ctx.reply(embed=embed, mention_author=False)

    @commands.hybrid_command(name='lock', description='Locks the provided text channel; or the current one if none')
    @app_commands.describe(channel='Text channel you want to lock')
    @commands.has_guild_permissions(manage_channels=True)
    async def lock(self, ctx: commands.Context, channel: Optional[discord.TextChannel]):
        channel = channel or ctx.channel
        permissions = channel.overwrites_for(ctx.guild.default_role)
        if permissions.send_messages == False:
            embed = discord.Embed(description=f'{emoji["negative"]} Chat {channel.mention} is already locked!', colour=discord.Colour(0x070d2d))
            return await ctx.reply(embed=embed, mention_author=False)    
        permissions.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=permissions)
        embed = discord.Embed(description=f'{emoji["positive"]}{emoji["lock"]} Chat {channel.mention} was successfully locked.', colour=discord.Colour(0x070d2d))
        await ctx.reply(embed=embed, mention_author=False)
    
    @commands.hybrid_command(name='lockdown', description='Locks all text channels in the server')
    @commands.has_guild_permissions(manage_channels=True)
    async def lockdown(self, ctx: commands.Context):
        embed = discord.Embed(description=f'{emoji["loading"]} Locking all the text channels...', colour=discord.Colour(0x070d2d))
        await ctx.reply(embed=embed, mention_author=False)
        for channel in ctx.guild.text_channels:
            permissions = channel.overwrites_for(ctx.guild.default_role)
            permissions.send_messages = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=permissions)
        embed = discord.Embed(description=f'{emoji["positive"]}{emoji["lock"]} All text channels in the server were successfully locked.', colour=discord.Colour(0x070d2d))
        await ctx.reply(embed=embed, mention_author=False)

    @commands.hybrid_command(name='unlock', description='Unlocks the provided text channel; or the current one if none')
    @app_commands.describe(channel='Text channel you want to unlock')
    @commands.has_guild_permissions(manage_channels=True)
    async def unlock(self, ctx: commands.Context, channel: Optional[discord.TextChannel]):
        channel = channel or ctx.channel
        permissions = channel.overwrites_for(ctx.guild.default_role)
        if permissions.send_messages == True:
            embed = discord.Embed(description=f'{emoji["negative"]} Chat {channel.mention} is already unlocked!', colour=discord.Colour(0x070d2d))
            return await ctx.reply(embed=embed, mention_author=False)
        permissions.send_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=permissions)
        embed = discord.Embed(description=f'{emoji["positive"]}{emoji["unlock"]} Chat {channel.mention} was successfully unlocked.', colour=discord.Colour(0x070d2d))
        await ctx.reply(embed=embed, mention_author=False)

    @commands.hybrid_command(name='unlockdown', description='Unlocks all text channels in the server')
    @commands.has_guild_permissions(manage_channels=True)
    async def unlockdown(self, ctx: commands.Context):
        embed = discord.Embed(description=f'{emoji["loading"]} Unlocking all the text channels...', colour=discord.Colour(0x070d2d))
        await ctx.reply(embed=embed, mention_author=False)
        for channel in ctx.guild.text_channels:
            permissions = channel.overwrites_for(ctx.guild.default_role)
            permissions.send_messages = True
            await channel.set_permissions(ctx.guild.default_role, overwrite=permissions)
        embed = discord.Embed(description=f'{emoji["positive"]}{emoji["unlock"]} All text channels in the server were successfully unlocked.', colour=discord.Colour(0x070d2d))
        await ctx.reply(embed=embed, mention_author=False)

    @commands.hybrid_command(name='say', description='Sends a custom message provided by the user in a specified channel; or the current one if none')
    @app_commands.describe(message='Message you want to say', channel='Channel you want to send the message')
    @commands.has_guild_permissions(manage_guild=True)
    async def say(self, ctx: commands.Context, message: str, channel: Optional[discord.TextChannel]):
        channel = channel or ctx.channel
        embed = discord.Embed(description=message, color=discord.Colour(0x070d2d))
        embed.set_footer(text=f'Message sent by @{ctx.author.display_name}', icon_url=ctx.author.display_avatar.url)
        await ctx.reply(f'{emoji["positive"]} Message successfully sent!', mention_author=False)
        await channel.send(embed=embed)
    
    @commands.hybrid_command(name='embed', description='Creates a custom embed')
    async def embed(self, ctx: commands.Context):
        view = EmbedCreator(bot=self.client, timeout=300)
        async def check(interaction: discord.Interaction):
            if interaction.user.id == ctx.author.id:
                return True
            else:
                embed = discord.Embed(description=f'{emoji["negative"]} Only {ctx.author} can use this interaction!')
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return False
        view.interaction_check = check
        await ctx.reply(embed=view.get_default_embed, view=view, mention_author=False)
    
async def setup(client):
    await client.add_cog(Administration(client))