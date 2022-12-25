import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import CommandNotFound

class errors(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
      embed = nextcord.Embed(title="Please state all requirements!", description="")
      await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
      embed = nextcord.Embed(title="You do not have the permission to run this command!", description="")
      await ctx.send(embed=embed)
    elif isinstance(error, CommandNotFound):
      embed = nextcord.Embed(title="This Command is Not Found!!", description="")
      await ctx.send(embed=embed)
    elif isinstance(error, commands.CommandOnCooldown):
      embed = nextcord.Embed(title="Cooldown!", description=f"This command is on cooldown, please try again in `{round(error.retry_after)}` seconds.")
      await ctx.send(embed=embed)
    elif isinstance(error, commands.NotOwner):
      embed = nextcord.Embed(title="This command is an owner only command for the bot owner", description=f"")
      await ctx.send(embed=embed)
    
    else:
      channel = self.bot.get_channel(1047613842819125348)
      embed = nextcord.Embed(title="ERROR!", description=":x:Something went wrong!!\n\nTry `%modmail (your question)` for Mod/Admin support!!", color=nextcord.Color.red())
      await ctx.send(embed=embed)
      embed2 = nextcord.Embed(title="Something went wrong!", description=f"Error: `{error}`", color=nextcord.Color.blue())
      embed2.set_footer(text=f"Done by: {ctx.author.name}#{ctx.author.discriminator} in {ctx.guild.name}")
      await channel.send(embed=embed2)



      


def setup(bot):
  bot.add_cog(errors(bot))