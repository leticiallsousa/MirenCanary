import discord
from discord.ext import commands
from discord import app_commands
from typing import Union, Optional
import time
from utils.utils import *
from datetime import datetime, timezone

class Info(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_group(name='user', description='Displays user information, including profile details, avatar, and banner.')
    async def user(self, ctx: commands.Context):
        embed = discord.Embed(title='Commands:', description='- user info `[user]`\n- user avatar `[user]`\n- user banner `[user]`', colour=discord.Colour(0x070d2d))
        await ctx.reply(embed=embed, mention_author=False)
    

    @user.command(name='info', description='Displays the informations about the provided user; or the author if none.')
    @app_commands.describe(user='User you want to display the informations')
    async def info(self, ctx: commands.Context, user: Optional[Union[discord.Member, discord.User]]):
        user = user or ctx.author
        view = discord.ui.View()

        async def avatar_callback(interaction: discord.Interaction):
            embed_avatar = discord.Embed(
                title=f':frame_photo: {user.display_name}\'s avatar', 
                colour=discord.Colour(0x070d2d)
                )
            embed_avatar.set_image(url=user.display_avatar.url)
            view_avatar = discord.ui.View()
            view_avatar.add_item(discord.ui.Button(label='Open in browser', url=user.display_avatar.url))
            await interaction.response.send_message(embed=embed_avatar,view=view_avatar, ephemeral=True)
        
        async def permissions_callback(interaction: discord.Interaction):
            embed_perms = discord.Embed(
                colour=discord.Colour(0x070d2d)
                )
            embed_perms.add_field(name=f':medal: Top role', value=user.top_role.mention)
            perm_list = ', '.join(f'`{perm.replace("_", " ").title()}`' for perm, value in sorted(user.guild_permissions) if value)
            embed_perms.add_field(name=f':gear: {user.name}\'s permissions', value=perm_list, inline=False)
            await interaction.response.send_message(embed=embed_perms, ephemeral=True)

        # user badges to be displayed in the embed
        badges = list()
        for flag in user.public_flags:
            if flag[1] and flag[0] in badge.keys():
                badges.append(badge[flag[0]])
        if not user.bot:
            if not isinstance(user, discord.Member):
                user = await self.client.fetch_user(user.id)
            if guess_user_nitro_status(user) == True:
                badges.append(badge["nitro"])
            if user.created_at < datetime(2023, 5, 3, tzinfo=timezone.utc):
                badges.append(badge["originally_known"])
        badges.sort()
        badges = ''.join(item[1:] for item in badges)

        # embed with informations about the user
        embed = discord.Embed(title=f'{user.display_name} {badges}', colour=discord.Colour(0x070d2d))
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.add_field(name=f'{emoji["user"]} Name', value=f'```{user.name}```')
        embed.add_field(name=f'{emoji["id"]} ID', value=f'```{user.id}```')
        embed.add_field(name=f'{emoji["mention"]} Mention', value=user.mention)
        created1 = convert_timestamp(user.created_at, 'f')
        created2 = convert_timestamp(user.created_at, 'R')
        embed.add_field(name=f'{emoji["calendar_1"]} Created at', value=f'{created1}({created2})', inline=False)

        if user in ctx.author.guild.members:
            joined1 = convert_timestamp(user.joined_at, 'f')
            joined2 = convert_timestamp(user.joined_at, 'R')
            embed.add_field(name=f'{emoji["calendar_2"]} Joined at', value=f'{joined1}({joined2})', inline=False)
            # buttons to see the global avatar and the permissions if the user is in the guild
            avatar = discord.ui.Button(label=f'See global avatar', style=discord.ButtonStyle.gray)
            avatar.callback = avatar_callback
            permissions = discord.ui.Button(label=f'See permissions', style=discord.ButtonStyle.gray)
            permissions.callback = permissions_callback
            view.add_item(avatar)
            view.add_item(permissions)

        else:
            notfound = discord.ui.Button(label="User not found in the server", style=discord.ButtonStyle.gray, disabled=True)
            view.add_item(notfound)

        await ctx.reply(embed=embed, mention_author=False, view=view)


    @user.command(name='avatar', description='Displays the avatar of the provided user; or the author if none.')
    @app_commands.describe(user='User you want to display the avatar')
    async def avatar(self, ctx: commands.Context, user: Optional[Union[discord.Member, discord.User]]):
        user = user or ctx.author
        embed = discord.Embed(title=f':frame_photo: {user.display_name}\'s avatar', colour=discord.Colour(0x070d2d))
        embed.set_image(url=user.display_avatar.url)
        avatarbutton = discord.ui.Button(label='Open in browser', url=user.display_avatar.url)
        view = discord.ui.View()
        view.add_item(avatarbutton)
        await ctx.reply(embed=embed, view=view, mention_author=False)
    
    @user.command(name='banner', description='Displays the banner of the provided user; or the author if none.')
    @app_commands.describe(user='User you want to display the banner')
    async def banner(self, ctx: commands.Context, user: Optional[Union[discord.Member, discord.User]]):
        user = user or ctx.author
        user = await self.client.fetch_user(user.id)
        if not user.banner:
            embed = discord.Embed(description=f'{emoji["negative"]} This user doesn\'t have a banner!', colour=discord.Colour(0x070d2d))
            return await ctx.reply(embed=embed, mention_author=False)
        embed = discord.Embed(title=f':frame_photo: {user.display_name}\'s banner', colour=discord.Colour(0x070d2d))
        embed.set_image(url=user.banner.url)
        bannerbutton = discord.ui.Button(label='Open in browser', url=user.banner.url)
        view = discord.ui.View()
        view.add_item(bannerbutton)
        await ctx.reply(embed=embed, view=view, mention_author=False)
    
    @commands.hybrid_group(name='server', description='Displays server information, including server details, server icon, banner and badges.')
    async def server(self, ctx: commands.Context):
        embed = discord.Embed(title='Commands:', description='- server info `[serverid]`\n- server icon `[serverid]`\n- server banner `[serverid]`\n- server badges `[serverid]`', colour=discord.Colour(0x070d2d))
        await ctx.reply(embed=embed, mention_author=False)
    
    @server.command(name='info', description='Displays the informations about the provided server; or the current if none.')
    @app_commands.describe(server='Server you want to display the informations')
    async def info(self, ctx: commands.Context, server: discord.Guild=None):
        view = discord.ui.View()
        async def seebadges_callback(interaction: discord.Interaction):
            embed_badge = server_badges(ctx, server)
            await interaction.response.send_message(embed=embed_badge, ephemeral=True)
        
        server = server or ctx.author.guild
        embed = discord.Embed(title=server.name, colour=discord.Colour(0x070d2d))
        embed.add_field(name=f'{emoji["id"]} ID', value=f'```{server.id}```')
        embed.add_field(name=f'{emoji["users"]} Users', value=f'```{server.member_count} members```')
        embed.add_field(name=':crown: Owner', value=f'{server.owner.mention}\n`{server.owner.id}`')
        created1 = convert_timestamp(server.created_at, 'f')
        created2 = convert_timestamp(server.created_at, 'R')
        embed.add_field(name=f'{emoji["calendar_1"]} Created at', value=f'{created1} ({created2})')
        if ctx.author in server.members:
            member = server.get_member(ctx.author.id)
            joined1 = convert_timestamp(member.joined_at, 'f')
            joined2 = convert_timestamp(member.joined_at, 'R')
            embed.add_field(name=f'{emoji["calendar_2"]} {ctx.author.global_name} joined at', value=f'{joined1} ({joined2})')
        embed.add_field(name=f'{emoji["channels"]} Channels: {len(server.channels)}', 
                        value=f'{emoji["category"]} Categories: {len(server.categories)}\n{emoji["text_channel"]} Text: {len(server.text_channels)}\n{emoji["voice_channel"]} Voice: {len(server.voice_channels)}')
        
        embed.set_thumbnail(url=server.icon.url)

        
        seebadges = discord.ui.Button(label='See server badges', style=discord.ButtonStyle.gray)
        seebadges.callback = seebadges_callback
        view.add_item(seebadges)

        await ctx.reply(embed=embed, mention_author=False, view=view)

    @server.command(name='icon', description='Displays the icon of the provided server; or the current if none.')
    @app_commands.describe(server='Server you want to display the icon')
    async def icon(self, ctx: commands.Context, server: discord.Guild=None):
        server = server or ctx.author.guild
        embed = discord.Embed(title=f':frame_photo: {server.name}', colour=discord.Colour(0x070d2d))
        embed.set_image(url=server.icon.url)
        iconbutton = discord.ui.Button(label='Open in browser', url=server.icon.url)
        view = discord.ui.View()
        view.add_item(iconbutton)
        await ctx.reply(embed=embed, mention_author=False, view=view)


    @server.command(name='badges', description='Displays how many users in the server (current if none) have each badge.')
    @app_commands.describe(server='Server you want to display the badges\' number of havers')
    async def badges(self, ctx: commands.Context, server: discord.Guild=None):
        server = server or ctx.author.guild
        embed_badge = server_badges(ctx, server)
        await ctx.reply(embed=embed_badge, mention_author=False, ephemeral=False)

    @commands.hybrid_command(name='ping', description='Shows the bot\'s latency')
    async def ping(self, ctx: commands.Context):
        start = time.time()
        embed = discord.Embed(title='**:ping_pong: Pong!**', colour=discord.Colour(0x070d2d))
        embed.add_field(name='API Ping:', value=f'`{round(self.client.latency*1000)}ms`')
        message = await ctx.reply(embed=embed, mention_author=False)
        end = time.time()
        ms_ping = round((end-start)*1000)
        embed.add_field(name='Message Ping:', value=f'`{ms_ping}ms`')
        await message.edit(embed=embed)

async def setup(client):
    await client.add_cog(Info(client))