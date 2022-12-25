import nextcord
from nextcord.utils import get
from nextcord.ext import commands
from nextcord import Interaction, SlashOption

import datetime
import sqlite3
import time
from cogs.utils.api import *
import re


class search(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @nextcord.slash_command(description="Search Anything Up")
  async def search(self, interaction: Interaction):
    return

  @search.subcommand(description="Search Up A Users Kick Log")
  async def kick(self, interaction: Interaction, user: str):
    await interaction.response.defer(ephemeral=False)
    is_setup = await checkSetUp(interaction, "punishment")
    if is_setup == False:
      return
    elif is_setup == True:
      try:
        con = sqlite3.connect("cogs/data/bot_server.db")
        cur = con.cursor()
    
        res = cur.execute(f"SELECT kick_reason, kick_id FROM kick_log WHERE user_id = '{user}' AND guild_id = '{interaction.guild.id}'")
        result = res.fetchall()
  
        if not result:
          em = nextcord.Embed(title=f"User not Found", description=f"", color=nextcord.Color.red())
          return await interaction.followup.send(embed=em)
        
        con.close()
        em = nextcord.Embed(title=f"{user}", description=f"", color=nextcord.Color.blue())
        em.set_footer(text=f"Staff Member: {interaction.user}")
        em.timestamp = datetime.datetime.utcnow()
        for x in result:
          em.add_field(name=f"{x[0]}", value=f"`{x[1]}`", inline=False)
        await interaction.followup.send(embed=em)
      except Exception as e:
        return

  @search.subcommand(description="Search Up A Users Kick Log")
  async def warn(self, interaction: Interaction, user: str):
    await interaction.response.defer(ephemeral=False)
    is_setup = await checkSetUp(interaction, "punishment")
    if is_setup == False:
      return
    elif is_setup == True:
      try:
        con = sqlite3.connect("cogs/data/bot_server.db")
        cur = con.cursor()
    
        res = cur.execute(f"SELECT warn_reason, warn_id FROM warn_log WHERE user_id = '{user}' AND guild_id = '{interaction.guild.id}'")
        result = res.fetchall()
        
        if not result:
          em = nextcord.Embed(title=f"User not Found", description=f"", color=nextcord.Color.red())
          return await interaction.followup.send(embed=em)
        
        con.close()
        em = nextcord.Embed(title=f"{user}", description=f"", color=nextcord.Color.blue())
        em.set_footer(text=f"Staff Member: {interaction.user}")
        em.timestamp = datetime.datetime.utcnow()
        for x in result:
          em.add_field(name=f"{x[0]}", value=f"`{x[1]}`", inline=False)
        await interaction.followup.send(embed=em)
      except Exception as e:
        return

  @search.subcommand(description="Search Up A Users Kick Log")
  async def ban(self, interaction: Interaction, user: str):
    await interaction.response.defer(ephemeral=False)
    is_setup = await checkSetUp(interaction, "punishment")
    if is_setup == False:
      return
    elif is_setup == True:
      try:
        con = sqlite3.connect("cogs/data/bot_server.db")
        cur = con.cursor()
    
        res = cur.execute(f"SELECT ban_reason, ban_id FROM ban_log WHERE user_id = '{user}' AND guild_id = '{interaction.guild.id}'")
        result = res.fetchall()
        
        if not result:
          em = nextcord.Embed(title=f"User not Found", description=f"", color=nextcord.Color.red())
          return await interaction.followup.send(embed=em)
        
        con.close()
        em = nextcord.Embed(title=f"{user}", description=f"", color=nextcord.Color.blue())
        em.set_footer(text=f"Staff Member: {interaction.user}")
        em.timestamp = datetime.datetime.utcnow()
        for x in result:
          em.add_field(name=f"{x[0]}", value=f"`{x[1]}`", inline=False)
        await interaction.followup.send(embed=em)
      except Exception as e:
        return
    
def setup(bot):
  bot.add_cog(search(bot))