from IO import file_io
from checks import is_moderator
from random import randint
from discord.ext import commands

class Replies(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.replies = file_io('data.json', 'load')

    def save_replies(self): file_io('data.json', 'save', self.replies)

    def parse_replylist(self, replylist):
        return '\n'.join([str(i) + ': "' + s + '"' for i, s in enumerate(replylist)])


    @commands.command(
        help = '''
        Add Reply
        Registers a new reply to a new or existing string of text.
        If the text is longer than 1 word, make sure to enclose it in quotes.
        If more than one reply is assigned to the same one, a reply will be selected at random from the available options.
        The text #mention# will be replaced by a ping for the user.
        
        Examples:
        !!addrep exampletext replytext
        !!addrep "example text" "reply text"
        !!addrep "hello there!" "hi #mention#!"
        ''',
        brief = 'Adds a reply',
        usage = '"<text>" "<reply>"'
    )

    @is_moderator()
    async def addrep(self, ctx, text, reply):
        text = text.casefold()

        if text not in self.replies: self.replies[text] = []
        self.replies[text].append(reply)
        msg = 'Added "' + reply + '" as a reply to "' + text + '".'

        num_replies = len(self.replies[text])
        if num_replies > 1: msg += '\nCurrent number of replies registered to this text: ' + str(num_replies) + '.'

        await ctx.send('```' + msg + '```')
        self.save_replies()

    @commands.command(
        help = '''
        Delete Reply
        Removes one reply to an existing string of text.
        The index of the reply to be deleted must be specified. Reply indexes may be viewed by using the listrep command.
        To remove all replies, use the delallrep command.

        Examples:
        !!delrep "exampletext" 0
        !!delrep "hi" 4
        ''',
        brief = 'Removes one reply',
        usage = '"<text>" <index>'
    )
    @is_moderator()
    async def delrep(self, ctx, text, index: int):
        text = text.casefold()
        num_replies = len(self.replies[text])
        if num_replies == 0:
            msg = 'Unable to find any replies to "' + text + '".'
        elif index < 0 or index >= num_replies:
            msg = 'There are ' + str(num_replies) + ' replies to "' + text + '" , but you selected index ' + index + ', which is invalid.'
        else:
            deleted = self.replies[text].pop(index)
            num_replies -= 1
            msg = 'Removed reply: "' + deleted + '"'
            if num_replies == 0: #If the last reply was removed
                del self.replies[text]
                msg += 'There are no longer any registered replies to the specified text.'
            else:
                msg += 'Remaining replies registered to the the text: ' + str(num_replies)
            self.save_replies()
        await ctx.send('```' + msg + '```')


    @commands.command(
        help = '''
        Delete All Replies
        Removes all replies to one string of text.
        To remove one reply instead, use the delrep command.

        Examples:
        !!delallrep example text
        !!delallrep hi
        ''',
        brief = 'Removes all replies to one message',
        usage = '<text>'
    )
    @is_moderator()
    async def delallrep(self, ctx, text):
        text = text.casefold()
        if text not in self.replies:
            msg = 'There are no replies assigned to "' + text + '".'
        else:
            del self.replies[text]
            msg = 'All associated replies have been removed from "' + text + '".'
            self.save_replies()
        await ctx.send('```' + msg + '```')

    @commands.command(
        help = '''
        List Replies
        Lists all replies to one message with their indexes.
        Use the listallrep command to view all replies at the same time.

        Examples:
        !!listrep "exampletext"
        !!listrep "hi"
        ''',
        brief = 'Lists the replies to one message',
        usage = '<text>'
    )
    @is_moderator()
    async def listrep(self, ctx, text):
        text = text.casefold()
        num_replies = len(self.replies[text]) if text in self.replies else 0

        if      num_replies == 0:   msg = 'No replies registered for "' + text + '".'
        elif    num_replies == 1:   msg = '1 reply registered for "' + text + '": "' + self.replies[text][0] + '"'
        else:                       msg = str(num_replies) + ' replies registered for "' + text + '": \n' + self.parse_replylist(self.replies[text])

        await ctx.send('```' + msg + '```')

    @commands.command(
        help = '''
        List All Replies
        Lists all replies to all messages with their indexes.

        Examples:
        !!listallrep
        ''',
        brief = 'Lists all replies',
    )
    @is_moderator()
    async def listallrep(self, ctx):
        keys = [k + ': \n' + self.parse_replylist(v) for k, v in self.replies.items()]
        msg = 'Listing all registered replies:\n\n' + '\n\n'.join(keys)

        await ctx.send('```' + msg + '```')

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return
        if msg.content.casefold() in self.replies:
            choices = self.replies[msg.content.casefold()]
            reply = choices[randint(0, len(choices) - 1)]

            reply = reply.replace("#mention#", msg.author.mention)

            await msg.channel.send(reply)