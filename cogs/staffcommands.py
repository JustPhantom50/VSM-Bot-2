import nextcord
from nextcord.utils import get
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, ChannelType
import datetime
import sqlite3
from cogs.utils.api import *
import asyncio
import re

class staffcmd(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @nextcord.slash_command(description="This allows Developers to delete peoples setups", guild_ids=[1000207936204836965,])
  @commands.check(check_if_it_is_me)
  async def delete_setup(self, interaction: Interaction, guild: str = SlashOption(description="Guild ID")):
    await interaction.response.defer(ephemeral=False)
    con = sqlite3.connect("cogs/data/bot_server.db")
    cur = con.cursor()
    try:
      cur.execute(f"DELETE FROM setup_servers WHERE guild_id = '{int(guild)}'")
      con.commit()
      con.close()
      return await interaction.followup.send(f"Guild is now deleted")
    except:
      
      con.commit()
      con.close()
      return await interaction.followup.send(f"Something Went Wrong!")
    
    
def setup(bot):
  bot.add_cog(staffcmd(bot))