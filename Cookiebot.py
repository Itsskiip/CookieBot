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

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot.run(config['token'])