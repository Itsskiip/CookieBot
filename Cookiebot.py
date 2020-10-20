from discord.ext import commands
from config import config
from replies import Replies
from misc import Misc
from embeds import Embeds
import logging
from os import getcwd, path

bot = commands.Bot(command_prefix='!!')
bot.add_cog(Replies(bot))
bot.add_cog(Misc(bot))
bot.add_cog(Embeds(bot))

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)

logfilename = path.join(getcwd(), 'discord.log')
handler = logging.FileHandler(filename=logfilename, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot.run(config['token'])