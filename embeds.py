from discord import Embed
from discord.ext import commands
from json import loads as jload
from checks import is_moderator
from datetime import datetime

class Embeds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command(
      help = '''
      JSON Embed
      Post a embed from a JSON string.
      You may use a visualiser such as the one here: https://leovoel.github.io/embed-visualizer/
      Do ensure that "Enable webhook mode" is turned off, and then copy and paste the code directly after your command.

      Examples:
      !!jsonembed {
        "content": "This is a test!",
        "embed": {
          "fields": [
            {"name": "OwO", "value": "Woah cool an embed"}
          ]
        }
      }
      ''',
      brief = 'Posts a custom embed',
      usage = '<json>'
    )
    async def jsonembed(self, ctx, *, json):
      try:
        input = jload(json)
        if 'content' not in input: input['content'] = ""

        emb = input['embed']
        if 'timestamp' in emb:  emb['timestamp'] = str(datetime.strptime(emb['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')) #Parse json time format to python time format
        
        emb_obj = Embed.from_dict(emb)
        await ctx.send(content = input['content'], embed = emb_obj)
      except:
        await ctx.send('```Unable to parse JSON, invalid format.```')
