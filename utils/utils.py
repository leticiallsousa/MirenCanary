import json
import discord
from discord import ButtonStyle
from discord.ext import commands
from typing import Dict, Union
from datetime import datetime, timezone

emoji = {
    "positive":"<:positive:1233138540708102285>", 
    "negative":"<:negative:1233138530138722394>",
    "lock":"<:Lock:1220920578035290113>",
    "unlock":"<:Unlock:1220920596049825872> ",
    "error":"<:error:1221499302308876298>",
    "loading":"<a:loading:1221530207677321359>",
    "warning":"<:Warning:1233153414096093284>",
    "info":"<:info:1233473131528585218>",
    "user":"<:user:1232067217282175006>",
    "users":"<:users:1233140937920745513>",
    "mention":"<:mention:1232067221958688848>",
    "id":"<:id:1232067220465651722>",
    "calendar_1":"<:calendar_1:1232067223577821215>",
    "calendar_2":"<:calendar_2:1232067842665611294>",
    "channels":"<:channels:1233137883305738311>",
    "category":"<:category:1233158769966583878>",
    "text_channel":"<:text_channel:1233137881002803291>",
    "voice_channel":"<:voice_channel:1233137879224680599>",
    "8ball":"<:8Ball:1233498237634084986>"
}

badge = {
    "staff":"a<:staff:1232026018970210374>",
    "partner":"b<:partner:1232026020790665247>",
    "discord_certified_moderator":"c<:discord_certified_moderator:1232045549851771083>",
    "hypesquad":"d<:hypesquad:1232040954530234378>",
    "hypesquad_bravery":"e<:hypesquad_bravery:1232028260729360485>",
    "hypesquad_brilliance":"f<:hypesquad_brilliance:1232028281956470865>",
    "hypesquad_balance":"g<:hypesquad_balance:1232028262562009179>",
    "bug_hunter":"h<:bug_hunter:1232026445677723679>",
    "bug_hunter_level_2":"i<:bug_hunter_level_2:1232026027417538652>",
    "active_developer":"j<:active_developer:1232045604008362094>",
    "early_supporter":"k<:early_supporter:1232026029472616498>",
    "nitro":"l<:nitro:1232026022594220093>",
    "originally_known":"m<:originally_known:1232045767145947216>",
    "verified_bot":"n<:verified_bot1:1232853794698690644><:verified_bot2:1232853793482342500>",
    "spammer": "o<:spammer:1232775439400042546>"
}

class Confirmation(discord.ui.View):
    """A UI view for a confirmation dialog with 'Confirm' and 'Cancel' buttons."""
    def __init__(self, callback):
        super().__init__(timeout=None)
        self.callback = callback
    @discord.ui.button(label='Confirm', style=ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.callback(interaction, confirmed=True)
    @discord.ui.button(label='Cancel', style=ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.callback(interaction, confirmed=False)

def hierarchy_check(author: Union[discord.Member, discord.User], user: Union[discord.Member, discord.User], punish: str) -> Union[str, None]:
    """
    Check if the author has the hierarchy to punish the user.

    Args:
        - author (Union[discord.Member, discord.User]): The user trying to execute the punish command.
        - user (Union[discord.Member, discord.User]): The user being punished.
        - punish (str): The type of punishment being attempted.

    Returns:
        str: A message indicating whether the punishment is allowed or not.
    """
    bot = author.guild.get_member(author.guild.me.id)
    if author.id == user.id:
        return f'You can\'t {punish} yourself!'
    elif author.guild.owner.id == user.id:
        return f'You can\'t {punish} the server owner!'
    elif user.top_role > author.top_role:
        return f'You can\'t {punish} this user, your top role is lower than theirs!'
    elif user.top_role > bot.top_role:
        return f'I can\'t {punish} this user, my top role is lower than theirs!'
    else:
        return None
    

def convert_timestamp(timestamp: datetime, type_: str) -> str:
    """
    Convert a given date and time to a Discord timestamp format.

    Args:
        - timestamp (datetime): The date and time to be converted.
        - type_ (str): The format type. Possible values:
            - 'F': Full date and time (e.g., January 1, 2022 12:30 PM).
            - 'f': Short date and time (e.g., 1/1/2022 12:30 PM).
            - 'D': Date only (e.g., January 1, 2022).
            - 'd': Short date only (e.g., 1/1/2022).
            - 'T': Time only (e.g., 12:30 PM).
            - 't': Short time only (e.g., 12:30).
            - 'R': Relative time (e.g., 3 days ago).

    Returns:
        str: The Discord timestamp format string.
    """
    if type_ not in ('F', 'f', 'D', 'd', 'T', 't', 'R'):
        return 'Invalid type_'
    
    date = datetime(timestamp.year, timestamp.month, timestamp.day, timestamp.hour, timestamp.minute)
    return f'<t:{int(date.timestamp())}:{type_}>'

def guess_user_nitro_status(user: Union[discord.User, discord.Member]) -> bool:
    """Guess if an user or member has Discord Nitro"""
    if isinstance(user, discord.Member):
        # Check if they have a custom emote in their status
        has_emote_status = any([a.emoji.is_custom_emoji() for a in user.activities if getattr(a, 'emoji', None)])
        return any([user.display_avatar.is_animated(), has_emote_status, user.premium_since, user.guild_avatar])
    return any([user.display_avatar.is_animated(), user.banner])


def server_badges(ctx: commands.Context, server: discord.Guild=None) -> discord.Embed:
    badge_counts = {}
    for flag in badge.keys():
        badge_counts[badge[flag]] = 0
    for member in server.members:
        for flag in member.public_flags:
            if flag[1] and flag[0] in badge.keys():
                badge_counts[badge[flag[0]]] += 1
        if not member.bot and member.created_at < datetime(2023, 5, 3, tzinfo=timezone.utc):
            badge_counts[badge["originally_known"]] += 1

    badge_string = ""
    for badge_name, count in badge_counts.items(): 
        badge_string += f"{badge_name[1:]} {count}\n"
    embed = discord.Embed(
        title=f'Badges in {server.name}', 
        description=badge_string, 
        colour=discord.Colour(0x070d2d))
    embed.set_footer(text=f'{server.member_count} members examined')
    return embed
