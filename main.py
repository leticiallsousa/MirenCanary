import discord
from discord.ext import commands
from dotenv import load_dotenv
from utils.utils import *
import asyncio
import os

def get_prefix(client, message):
    with open('utils\guilds_data.json', 'r') as f:
        data = json.load(f)
    return data["guilds"][str(message.guild.id)]["prefix"]
client = commands.Bot(command_prefix=get_prefix, intents=discord.Intents.all())
tree = client.tree

load_dotenv()
discord.utils.setup_logging()

@client.event
async def on_ready():
    print('Estou online!')

@client.event
async def on_guild_join(guild):
    with open('utils\guilds_data.json', 'r') as f:
        data = json.load(f)

    if str(guild.id) not in data["guilds"]:
        data["guilds"][guild.id] = {
             'prefix': '!', 
             'join_settings': {
                  'message_enabled': False,
                  'message_text': '',
                  'message_channel': '',
                  'image_enabled': False,
                  'image_url': ''
                  },
             'leave_settings': {
                  'message_enabled': False,
                  'message_text': '',
                  'message_channel': '',
                  'image_enabled': False,
                  'image_url': ''
                  }}
    
        with open('utils\guilds_data.json', 'w') as file:
            json.dump(data, file, indent=4)

@client.event
async def on_guild_remove(guild):
    with open('utils/guilds_data.json', 'r') as file:
        data = json.load(file)
    if str(guild.id) in data["guilds"]:
        del data["guilds"][str(guild.id)]
    with open('utils/guilds_data.json', 'w') as file:
        json.dump(data, file, indent=4)

@client.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    embed = discord.Embed(description=f'{emoji["error"]} ', colour=discord.Colour(0x070d2d))
    if isinstance(error, commands.CommandInvokeError):
        error = error.original
    if isinstance(error, commands.GuildNotFound):
        embed.description += 'The provided server is invalid. I might not be in it, or it doesn\'t exist.'
    if isinstance(error, commands.ChannelNotFound):
        embed.description += 'The provided channel is invalid. I might not have acess to it, or it doesn\'t exist.'
    else:
        embed.description += 'Oops! An error ocurred'
        embed.add_field(name='Error:', value=f'```py\n{type(error).__name__}: {error}```')
    await ctx.send(embed=embed, ephemeral=True) if ctx.interaction else await ctx.send(embed=embed, mention_author=False)

async def load():
	for filename in os.listdir('./cogs'):
		if filename.endswith('.py'):
			await client.load_extension(f'cogs.{filename[:-3]}')

async def main():
	await load()
	await client.start(os.getenv('TOKEN'))

asyncio.run(main())
