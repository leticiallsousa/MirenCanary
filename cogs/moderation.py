import discord
from discord.ext import commands
from discord import app_commands, ButtonStyle
from typing import Union, Optional
from discord.ui import View, Button
from utils.utils import *

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    '''@commands.hybrid_command(name='template', description='any')
    @app_commands.describe(any='any')
    async def template(self, ctx: commands.Context, any: Optional[str]):
        async def confirmation_callback(interaction: discord.Interaction, confirmed: bool):
            if confirmed:
                await interaction.response.send_message(f'Confirmado! {bool}')
            else:
                await interaction.response.send_message(f'Cancelado! {any}')
        view = Confirmation(confirmation_callback)
        await ctx.reply('Test Message', view=view, mention_author=False)'''

    @commands.hybrid_command(name='kick', description='Kicks a provided user from the server')
    @app_commands.describe(user='User you want to kick', reason='Reason why you want to kick the user')
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, user: Union[discord.Member, discord.User], *, reason: Optional[str]):
        permission = hierarchy_check(ctx.author, user, 'kick')
        if permission is not None:
            embed = discord.Embed(description=f'{emoji["negative"]} **Error!** {permission}', colour=discord.Colour(0x070d2d))
            return await ctx.reply(embed=embed, mention_author=False)
        
        reason = reason or 'No reason'
        async def confirmation_callback(interaction: discord.Interaction, confirmed: bool):
            if confirmed:
                await user.kick(reason=reason)
                embed = discord.Embed(description=f'{emoji["positive"]} **Confirmed!** User @{user.display_name} `({user.name})` have been successfully kicked from the server. `Reason: {reason}`', colour=discord.Colour(0x070d2d))
                await interaction.response.edit_message(embed=embed, view=None)
            else:
                embed = discord.Embed(description=f'{emoji["negative"]} **Canceled!** The action to kick the user @{user.display_name} `({user.name})` from the server have been cancelled.', colour=discord.Colour(0x070d2d))
                await interaction.response.edit_message(embed=embed, view=None)
        view = Confirmation(confirmation_callback)
        embed = discord.Embed(description=f'{emoji["warning"]} Are you sure you want to kick @{user.display_name} `({user.name})` from the server? Please confirm by clicking the "Confirm" button.', colour=discord.Colour(0x070d2d))
        
        if user in ctx.guild.members:
            await ctx.reply(embed=embed, view=view, mention_author=False)
        else:
            embed = discord.Embed(description=f'{emoji["negative"]} User @{user.display_name} `({user.name})` is not currently a member of this server and cannot be kicked!', colour=discord.Colour(0x070d2d))
            await ctx.reply(embed=embed, mention_author=False)
    
    @commands.hybrid_command(name='ban', description='Bans a provided user from the server')
    @app_commands.describe(user='User you want to ban', reason='Reason why you want to ban the user')
    @commands.has_guild_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, user: Union[discord.Member, discord.User], *, reason: Optional[str]):
        permission = hierarchy_check(ctx.author, user, 'ban')
        if permission is not None:
            embed = discord.Embed(description=f'{emoji["negative"]} **Error!** {permission}', colour=discord.Colour(0x070d2d))
            return await ctx.reply(embed=embed, mention_author=False)
        
        reason = reason or 'No reason'
        async def confirmation_callback(interaction: discord.Interaction, confirmed: bool):
            if confirmed:
                await interaction.guild.ban(user, reason=reason)
                embed = discord.Embed(description=f'{emoji["positive"]} **Confirmed!** User @{user.display_name} `({user.name})` have been successfully banned from the server. `Reason: {reason}`', colour=discord.Colour(0x070d2d))
                await interaction.response.edit_message(embed=embed, view=None)
            else:
                embed = discord.Embed(description=f'{emoji["negative"]} **Canceled!** The action to ban the user @{user.display_name} `({user.name})` from the server have been cancelled.', colour=discord.Colour(0x070d2d))
                await interaction.response.edit_message(embed=embed, view=None)
        view = Confirmation(confirmation_callback)
        embed = discord.Embed(description=f'{emoji["warning"]} Are you sure you want to ban @{user.display_name} `({user.name})` from the server? Please confirm by clicking the "Confirm" button.', colour=discord.Colour(0x070d2d))
        
        banned_users = [entry async for entry in ctx.guild.bans()]
        if any(entry.user.id == user.id for entry in banned_users):
            embed = discord.Embed(description=f'{emoji["negative"]} User @{user.display_name} `({user.name})` is already banned!', colour=discord.Colour(0x070d2d))
            await ctx.reply(embed=embed, mention_author=False)
        else:
            await ctx.reply(embed=embed, view=view, mention_author=False)
    
    @commands.hybrid_command(name='unban', description='Unbans a provided user from the server')
    @app_commands.describe(user='User you want to unban', reason='Reason why you want to unban the user')
    @commands.has_guild_permissions(ban_members=True)
    async def unban(self, ctx: commands.Context, user: Union[discord.Member, discord.User], *, reason: Optional[str]):
        reason = reason or 'No reason'
        async def confirmation_callback(interaction: discord.Interaction, confirmed: bool):
            if confirmed:
                await interaction.guild.unban(user, reason=reason)
                embed = discord.Embed(description=f'{emoji["positive"]} **Confirmed!** User @{user.display_name} `({user.name})` have been successfully unbanned from the server. `Reason: {reason}`', colour=discord.Colour(0x070d2d))
                await interaction.response.edit_message(embed=embed, view=None)
            else:
                embed = discord.Embed(description=f'{emoji["negative"]} **Canceled!** The action to unban the user @{user.display_name} `({user.name})` from the server have been cancelled.', colour=discord.Colour(0x070d2d))
                await interaction.response.edit_message(embed=embed, view=None)
        view = Confirmation(confirmation_callback)
        embed = discord.Embed(description=f'{emoji["warning"]} Are you sure you want to unban @{user.display_name} `({user.name})` from the server? Please confirm by clicking the "Confirm" button.', colour=discord.Colour(0x070d2d))

        banned_users = [entry async for entry in ctx.guild.bans()]
        if any(entry.user.id == user.id for entry in banned_users):
            await ctx.reply(embed=embed, view=view, mention_author=False)
        else: 
            embed = discord.Embed(description=f'{emoji["negative"]} User @{user.display_name} `({user.name})` is not currently banned!', colour=discord.Colour(0x070d2d))
            await ctx.reply(embed=embed, mention_author=False)

async def setup(client):
    await client.add_cog(Moderation(client))