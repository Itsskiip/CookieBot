from discord.ext import commands
from config import config

def is_owner():
    async def predicate(ctx): 
        return ctx.author.id == ctx.guild.owner_id
    return commands.check(predicate)

def is_moderator():
    async def predicate(ctx):
        if 'moderator_role' not in config.keys(): return False

        mod_role = ctx.guild.get_role(config['moderator_role'])

        if mod_role is None: return False
        return ctx.author in mod_role.members

    return commands.check(predicate)