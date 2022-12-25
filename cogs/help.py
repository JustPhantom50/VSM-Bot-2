import nextcord
from nextcord.utils import get
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
import datetime
import sqlite3
import time
from cogs.utils.api import *
import re

class help(commands.Cog):
  def __init__(self, bot): 
    self.bot = bot

  
  @nextcord.slash_command(description="this is a help commmand")
  async def help(self, interaction: Interaction):
    await interaction.response.defer(ephemeral=False)
    em = nextcord.Embed(title=f":gear: VSM Command List :gear:", description=f"`/setup` | *Use this to set up VSM.*\n\n`/shift manage` | *Use this to manage your shift.*\n\n`", color=nextcord.Color.blue())
    await interaction.followup.send(embed=em)


  # @help.subcommand()
  # async def shift(self, interaction: Interaction):
  #   await interaction.response.defer(ephemeral=False)
  #   em = nextcord.Embed(title=f"VSM Command List", description=f"`/setup` | Use this to set up VSM", color=nextcord.Color.blue())
  #   await interaction.followup.send(embed=em)

    
    
def setup(bot):
  bot.add_cog(help(bot))