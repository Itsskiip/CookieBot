from discord.ext import commands
from config import config
from replies import Replies
from misc import Misc

bot = commands.Bot(command_prefix='!!')
bot.add_cog(Replies(bot))
bot.add_cog(Misc(bot))
bot.run(config['token'])