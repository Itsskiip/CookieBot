from discord.ext import commands
from config import config

def is_owner():
    async def predicate(ctx): 
        return ctx.author.id == ctx.guild.owner_id
    return commands.check(predicate)

def is_moderator():
    async def predicate(ctx):
        return ('moderator_role' in config.keys()) and (ctx.author in ctx.guild.get_role(config['moderator_role']).members)
    return commands.check(predicate)