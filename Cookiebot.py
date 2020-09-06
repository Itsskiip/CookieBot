from discord.ext import commands
from config import config
from replies import Replies
from misc import Misc
from embeds import Embeds
import logging

bot = commands.Bot(command_prefix='!!')
bot.add_cog(Replies(bot))
bot.add_cog(Misc(bot))
bot.add_cog(Embeds(bot))
logging.basicConfig(level=logging.WARNING)
bot.run(config['token'])