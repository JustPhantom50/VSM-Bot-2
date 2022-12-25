import nextcord
from nextcord.utils import get
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
import datetime
import sqlite3
import time
from cogs.utils.api import *
import re


class punishments(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    

  @nextcord.slash_command(description="Log a Punishment")
  async def log(self, interaction: Interaction):
    return

  @log.subcommand(description="Log a Kick")
  async def kick(self, interaction: Interaction, member: str, reason: str = 'No reason specified'):
      
    await interaction.response.defer(ephemeral=False)
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    is_setup = await checkSetUp(interaction, "punishment")
    if is_setup == False:
      return
    elif is_setup == True:
      try:
        try:
          user = interaction.guild.get_member(int(member))
          member = user.id
        except Exception as e:
          user = interaction.guild.get_member(int(member.id))
          member = user.id
      except Exception as e:
        pass
        
      kickID = await create_id(interaction, "kick_log")
      con = sqlite3.connect("cogs/data/bot_server.db")
      cur = con.cursor()
      cur.execute(f"INSERT INTO kick_log(user_id, kick_reason, kick_id, guild_id) VALUES ('{member}', '{reason}', '{kickID}', '{interaction.guild.id}')")
      con.commit()
      con.close()
  
      em = nextcord.Embed(title=f"Kick Logged", description=f"You have logged a kick", color=nextcord.Color.green())
      em.add_field(name="User", value=f"{member}", inline=False)
      em.add_field(name="Reason", value=f"{reason}", inline=False)
      em.add_field(name="Kick ID", value=f" `{kickID}`", inline=False)
      em.set_footer(text=f"Staff Member: {interaction.user}")
      em.timestamp = datetime.datetime.utcnow()
      await interaction.followup.send(embed=em)
      await punishLogFunc("Log Kick", current_time, interaction, self.bot)

  @log.subcommand(description="Log a Ban")
  async def warn(self, interaction: Interaction, member: str, reason: str = 'No reason specified'):
    await interaction.response.defer(ephemeral=False)
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    is_setup = await checkSetUp(interaction, "punishment")
    if is_setup == False:
      return
    elif is_setup == True:
      try:
        try:
          user = interaction.guild.get_member(int(member))
          member = user.id
        except Exception as e:
          user = interaction.guild.get_member(int(member.id))
          member = user.id
      except Exception as e:
        pass
        
      warnID = await create_id(interaction, "warn_log")
      con = sqlite3.connect("cogs/data/bot_server.db")
      cur = con.cursor()
      cur.execute(f"INSERT INTO warn_log(user_id, warn_reason, warn_id, guild_id) VALUES ('{member}', '{reason}', '{warnID}', '{interaction.guild.id}')")
      con.commit()
      con.close()
  
      em = nextcord.Embed(title=f"Warn Logged", description=f"You have logged a warn", color=nextcord.Color.green())
      em.add_field(name="User", value=f"{member}", inline=False)
      em.add_field(name="Reason", value=f"{reason}", inline=False)
      em.add_field(name="Warn ID", value=f" `{warnID}`", inline=False)
      em.set_footer(text=f"Staff Member: {interaction.user}")
      em.timestamp = datetime.datetime.utcnow()
      await interaction.followup.send(embed=em)
      await punishLogFunc("Log Warn", current_time, interaction, self.bot)

  @log.subcommand(description="Log a ban")
  async def ban(self, interaction: Interaction, member: str, reason: str = 'No reason specified'):
    await interaction.response.defer(ephemeral=False)
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    is_setup = await checkSetUp(interaction, "punishment")
    if is_setup == False:
      return
    elif is_setup == True:
      try:
        try:
          user = interaction.guild.get_member(int(member))
          member = user.id
        except Exception as e:
          user = interaction.guild.get_member(int(member.id))
          member = user.id
      except Exception as e:
        pass
        
      banID = await create_id(interaction, "ban_log")
      con = sqlite3.connect("cogs/data/bot_server.db")
      cur = con.cursor()
      cur.execute(f"INSERT INTO ban_log(user_id, ban_reason, ban_id, guild_id) VALUES ('{member}', '{reason}', '{banID}', '{interaction.guild.id}')")
      con.commit()
      con.close()
  
      em = nextcord.Embed(title=f"Ban Logged", description=f"You have logged a ban", color=nextcord.Color.green())
      em.add_field(name="User", value=f"{member}", inline=False)
      em.add_field(name="Reason", value=f"{reason}", inline=False)
      em.add_field(name="Ban ID", value=f" `{banID}`", inline=False)
      em.set_footer(text=f"Staff Member: {interaction.user}")
      em.timestamp = datetime.datetime.utcnow()
      await interaction.followup.send(embed=em)
      await punishLogFunc("Log Ban", current_time, interaction, self.bot)

  @log.subcommand(description="Delete a Log")
  async def delete(self, interaction: Interaction, member: str, error_id: str, type: int = SlashOption(name="types", choices={"Kick": 1, "Warn": 2, "Ban": 3},)):
    await interaction.response.defer(ephemeral=False)
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    is_setup = await checkSetUp(interaction, "punishment")
    if is_setup == False:
      return
    elif is_setup == True:
      try:
        try:
          user = interaction.guild.get_member(int(member))
          member = user.id
        except Exception as e:
          user = interaction.guild.get_member(int(member.id))
          member = user.id
      except Exception as e:
        pass
      if type == 1:
        type = "kick"
      elif type == 2:
        type = "warn"
      elif type == 3:
        type = "ban"
      con = sqlite3.connect("cogs/data/bot_server.db")
      cur = con.cursor()
  
      cur.execute(f"DELETE FROM {type}_log WHERE user_id = '{member}' AND guild_id = '{interaction.guild.id}' AND {type}_id = '{error_id}'")
  
      con.commit()
      con.close()
  
      em = nextcord.Embed(title="Deleted", description=f"You have deleted punishment id `{error_id}` from {member}", color=nextcord.Color.blue())
      await interaction.followup.send(embed=em)
    
def setup(bot):
  bot.add_cog(punishments(bot))