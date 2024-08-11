import discord
from discord.ext import commands
from discord import app_commands
import json


class WelcomeSystem(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client  

    # setar mensagem padrão de join e leave quando forem ativados       

    @commands.hybrid_group(name='join')
    async def join(self, ctx: commands.Context):
        embed = discord.Embed(title='Commands:', description='- join_message enable\n- join disable\n- create category `<name>`', colour=discord.Colour(0x070d2d))
        await ctx.reply(embed=embed, mention_author=False)

    @join.command(name='enable', description='Activates the bot\'s join message feature for your server')
    @commands.has_guild_permissions(manage_messages=True)
    async def enable(self, ctx: commands.Context, channel: discord.TextChannel):
        with open('utils/guilds_data.json', 'r') as file:
            data = json.load(file)
            join_settings = data["guilds"][str(ctx.guild.id)]["join_settings"]
        if not join_settings["message_enabled"]:
            join_settings["message_enabled"] = True
            join_settings["message_channel"] = channel.id
            with open('utils/guilds_data.json', 'w') as file:
                json.dump(data, file, indent=4)
            embed = discord.Embed(description=f'a mensagem de welcome foi ativada agora no chat {channel.mention}', colour=discord.Colour(0x070d2d))
            await ctx.reply(embed=embed, mention_author=False)
        else:
            embed = discord.Embed(description='a mensagem de welcome ja tava ativada', colour=discord.Colour(0x070d2d))
            return await ctx.reply(embed=embed, mention_author=False)

    @join.command(name='disable', description='Deactivates the bot\'s join message feature for your server')
    @commands.has_guild_permissions(manage_messages=True)
    async def disable(self, ctx: commands.Context):
        with open('utils/guilds_data.json', 'r') as file:
            data = json.load(file)
            settings = data["guilds"][str(ctx.guild.id)]["join_settings"]
        if settings["message_enabled"]:

            settings["message_enabled"] = False
            settings["message_text"] = ''
            settings["message_channel"] = ''
            settings["image_enabled"] = False
            settings["image_url"] = ''

            with open('utils/guilds_data.json', 'w') as file:
                json.dump(data, file, indent=4)
            embed = discord.Embed(description='a mensagem de welcome foi desativada agora', colour=discord.Colour(0x070d2d))
            await ctx.reply(embed=embed, mention_author=False)
        else:
            embed = discord.Embed(description='a mensagem de welcome ja tava desativada', colour=discord.Colour(0x070d2d))
            await ctx.reply(embed=embed, mention_author=False)

    @join.command(name='channel', description='Designates the channel where the bot will send the join message')
    @commands.has_guild_permissions(manage_messages=True)
    async def channel(self, ctx: commands.Context):
        pass

    @join.command(name='message', description='Configures the content of the join message for new server members')
    @commands.has_guild_permissions(manage_messages=True)
    async def message(self, ctx: commands.Context):
        pass

    @join.command(name='image', description='Updates the image displayed in the join message when a new user joins the server')
    @commands.has_guild_permissions(manage_channels=True, attach_files=True)
    async def image(self, ctx: commands.Context):
        pass





    @commands.hybrid_group(name='leave')
    async def leave(self, ctx: commands.Context):
        pass

    @leave.command(name='enable', description='Activates the bot\'s leave message feature for your server')
    @commands.has_guild_permissions(manage_messages=True)
    async def enable(self, ctx: commands.Context, channel: discord.TextChannel):
        with open('utils/guilds_data.json', 'r') as file:
            data = json.load(file)
            leave_settings = data["guilds"][str(ctx.guild.id)]["leave_settings"]
        if not leave_settings["message_enabled"]:
            leave_settings["message_enabled"] = True
            leave_settings["message_channel"] = channel.id
            with open('utils/guilds_data.json', 'w') as file:
                json.dump(data, file, indent=4)
            embed = discord.Embed(description=f'a mensagem de leave foi ativada agora no chat {channel.mention}', colour=discord.Colour(0x070d2d))
            await ctx.reply(embed=embed, mention_author=False)
        else:
            embed = discord.Embed(description='a mensagem de leave ja tava ativada', colour=discord.Colour(0x070d2d))
            await ctx.reply(embed=embed, mention_author=False)

    @leave.command(name='disable', description='Deactivates the bot\'s leave message feature for your server')
    @commands.has_guild_permissions(manage_messages=True)
    async def disable(self, ctx: commands.Context):
        with open('utils/guilds_data.json', 'r') as file:
            data = json.load(file)
            settings = data["guilds"][str(ctx.guild.id)]["leave_settings"]
        if settings["message_enabled"]:
            
            settings["message_enabled"] = False
            settings["message_text"] = ''
            settings["message_channel"] = ''
            settings["image_enabled"] = False
            settings["image_url"] = ''
            
            with open('utils/guilds_data.json', 'w') as file:
                json.dump(data, file, indent=4)
            embed = discord.Embed(description='a mensagem de leave foi desativada agora', colour=discord.Colour(0x070d2d))
            await ctx.reply(embed=embed, mention_author=False)
        else:
            embed = discord.Embed(description='a mensagem de leave ja tava desativada', colour=discord.Colour(0x070d2d))
            await ctx.reply(embed=embed, mention_author=False)

    @leave.command(name='channel', description='Designates the channel where the bot will send the leave message')
    @commands.has_guild_permissions(manage_messages=True)
    async def channel(self, ctx: commands.Context):
        pass

    @leave.command(name='message', description='Configures the content of the leave message for new server members')
    @commands.has_guild_permissions(manage_messages=True)
    async def message(self, ctx: commands.Context):
        pass

    @leave.command(name='image', description='Updates the image displayed in the leave message when a new user leaves the server')
    @commands.has_guild_permissions(manage_messages=True)
    async def image(self, ctx: commands.Context):
        pass
    

async def setup(client):
    await client.add_cog(WelcomeSystem(client))