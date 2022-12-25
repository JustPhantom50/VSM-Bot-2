import nextcord
from nextcord.utils import get
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
import datetime
import sqlite3
import time
from cogs.utils.api import *
import re

class events(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @nextcord.slash_command(description="Request an LOA")
  async def request(self, interaction: Interaction):
    return

  @request.subcommand()
  async def loa(self, interaction: Interaction, reason: str = "Not Specified"):
    await interaction.response.defer(ephemeral=False)
    con = sqlite3.connect("cogs/data/bot_server.db")
    cur = con.cursor()
    con.commit()
    con.close()
    em = nextcord.Embed(title="LOA Requested", description=f"You have just requested an LOA. Please wait for management to accpet or deny your request.")
    em.add_field(name="Reason", value=f"`{reason}`")
    await interaction.followup.send(embed=em)
    
def setup(bot):
  bot.add_cog(events(bot))