import nextcord
from nextcord.utils import get
from nextcord.ext import commands

class events(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_message(self, ctx):
    if self.bot.user.mentioned_in(ctx) and len(ctx.content.split(' ')) == 1 and ctx.content[-1] == ">" and ctx.content[0] == '<':
      await ctx.channel.send("My prefix is `/`\nTry `/help music` for help with commands")
    
def setup(bot):
  bot.add_cog(events(bot))