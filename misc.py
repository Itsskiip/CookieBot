from config import config, save_config
from checks import is_owner, is_moderator
from discord import Activity, ActivityType
from discord.ext import commands

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        help = '''
        Change Moderator Role
        Changes the role that is capable of using the 'replies' commands.
        Only one role may be registered at any time and isn't affected by role name changes.
        Can only be used by the owner.

        Examples:
        !!changemod Some Moderator Role
        ''',
        brief = 'Changes the moderator role',
        usage = '<role name>')
    @is_owner()
    async def changemod(self, ctx, role):
        rid = next((r.id for r in ctx.guild.roles if r.name.casefold() == role.casefold()), None)
        if rid is None:
            msg = "Unable to find the specified role."
        else:
            config['moderator_role'] = rid
            msg = 'The moderator role has been changed to "' + ctx.guild.get_role(rid).name + '".'
            save_config()
        await ctx.send('```' + msg + '```')

    @commands.command(
        help = '''
        Change Profile Picture
        Changes the profile picture of the bot.
        To use, post an image as an attachment. Under "Add a comment", type in the !!changepfp command.
        Only PNGs and JPEGs are supported.

        Examples:
        !!changepfp
        ''',
        brief = 'Changes the profile picture of the bot'
    )
    @is_moderator()
    async def changepfp(self, ctx):
        attachments = ctx.message.attachments
        if (len(attachments) == 0):
            msg = 'An error occurred while trying to update the pfp.'
        else:
            b = await attachments[0].read()
            await self.bot.user.edit(avatar=b)
            msg = 'Successfully updated the pfp.'
        await ctx.send('```' + msg + '```')


    @commands.command(
        help = '''
        Change Status
        Changes the status of the bot.
        <type> can be set to "playing", "streaming", "listening to" or "watching". Leave it blank to default to "playing".
        <status> should be entered with quotes if it is longer than one word.
        

        Examples:
        !!changestat "with many cats"
        !!changestat cats streaming
        !!changestat "cat meows" "listening to"
        ''',
        brief = 'Changes the status of the bot',
        usage = '"<status>" <type (optional)>'
    )
    @is_moderator()
    async def changestat(self, ctx, text, t = "playing"):
        if t == 'playing': parsedtype = ActivityType.playing
        elif t == 'streaming': parsedtype = ActivityType.streaming
        elif t == 'listening to': parsedtype = ActivityType.listening
        elif t == 'watching': parsedtype = ActivityType.watching
        else:
            await ctx.send('```Invalid type.```')
            return
        await self.bot.change_presence(activity=Activity(name = text, type = parsedtype))
        await ctx.send('```Status changed to "' + t + ' ' + text + '".```')
