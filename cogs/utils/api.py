import nextcord
from nextcord.utils import get
from nextcord.ext import commands
from nextcord import Interaction
import datetime
import sqlite3
import random

def check_if_it_is_me(ctx):
    return ctx.message.author.id == 676895030094331915 or ctx.message.author.id == 687423771346599946

async def checkSetUp(interaction, type):
  con = sqlite3.connect("cogs/data/bot_server.db")
  cur = con.cursor()
  if type == "punishment":
    res = cur.execute(f"SELECT punishment_channel_id FROM setup_servers WHERE guild_id = '{int(interaction.guild.id)}'")
    guild = res.fetchone()
    if guild != None:
      
      return True
    else:
      em = nextcord.Embed(title="Setup", description="Please setup the bot!", color=nextcord.Color.blue())
      await interaction.followup.send(embed = em)
      return False
  elif type == "staff":
    res = cur.execute(f"SELECT staff_channel_id, staff_role_id, management_role_id, loa_role_id FROM setup_servers WHERE guild_id = '{int(interaction.guild.id)}'")
    guild = res.fetchone()
    if guild != None:
      return True
    else:
      em = nextcord.Embed(title="Setup", description="Please setup the bot!", color=nextcord.Color.blue())
      await interaction.followup.send(embed = em)
      return False
  elif type == "shift":
    res = cur.execute(f"SELECT shift_role_id, shift_channel_id, shift_reqirement FROM setup_servers WHERE guild_id = '{int(interaction.guild.id)}'")
    guild = res.fetchone()
    if guild != None:
      return True
    else:
      em = nextcord.Embed(title="Setup", description="Please setup the bot!", color=nextcord.Color.blue())
      await interaction.followup.send(embed = em)
      return False
  else:
    em = nextcord.Embed(title="Setup", description="Please setup the bot!", color=nextcord.Color.blue())
    await interaction.followup.send(embed = em)
    return False



async def shiftCheck(interaction):
  con = sqlite3.connect("cogs/data/bot_server.db")
  cur = con.cursor()
  res = cur.execute(f"SELECT user_id, shift_start, break_start, break_end FROM shifts WHERE user_id = '{interaction.user.id}' AND guild_id = '{interaction.guild.id}'")
  check = res.fetchone()
  res2 = cur.execute(f"SELECT * FROM setup_servers WHERE guild_id = '{interaction.guild.id}'")
  check2 = res2.fetchone()
  if check == None:
    return True
  elif check[1] != None:
    return "shift_already_started"
  elif check[2] != None:
    return "break_already_started"
  elif check[3] != None:
    return "break_already_ended"
  else:
    return False

async def end_shift_function(cur, interaction, end_time):

  break_overall_hours = 0
  break_overall_min = 0
  break_overall_sec = 0

  final_shift_hours = 0
  final_shift_min = 0
  final_shift_sec = 0
  
  
  s_result = cur.execute(f"SELECT shift_start FROM shifts WHERE user_id = '{interaction.user.id}' AND guild_id = '{interaction.guild.id}'")
  start_result = s_result.fetchone()
  
  start_list = []
  start_hours = ""
  start_min = ""
  start_sec = ""
  for item in start_result[0]:
    start_list.append(item)
  for num in start_list[0:2]:
    start_hours += num
  for num in start_list[3:5]:
    start_min += num
  for num in start_list[6:8]:
    start_sec += num

  try:
    s_result = cur.execute(f"SELECT break_start, break_end FROM shifts WHERE user_id = '{interaction.user.id}' AND guild_id = '{interaction.guild.id}'")
    break_result = s_result.fetchone()

    break_list = []
    break_hours = ""
    break_min = ""
    break_sec = ""
    for item in break_result[0]:
      break_list.append(item)
    for num in break_list[0:2]:
      break_hours += num
    for num in break_list[3:5]:
      break_min += num
    for num in break_list[6:8]:
      break_sec += num

    break_list2 = []
    break_hours_end = ""
    break_min_end = ""
    break_sec_end = ""
    for item in break_result[1]:
      break_list2.append(item)
    for number in break_list2[0:2]:
      break_hours_end += number
    for number in break_list2[3:5]:
      break_min_end += number
    for number in break_list2[6:8]:
      break_sec_end += number
    
    break_overall_hours = int(break_hours_end) - int(break_hours)
    break_overall_min = int(break_min_end) - int(break_min)
    break_overall_sec = int(break_sec_end) - int(break_sec)
    
    final_shift_hours = (int(end_time[0:2]) - int(start_hours)) - int(break_overall_hours)
    final_shift_min = (int(end_time[3:5]) - int(start_min)) - int(break_overall_min)
    final_shift_sec = (int(end_time[6:8]) - int(start_sec)) - int(break_overall_sec)

    
    
    return abs(final_shift_hours), abs(final_shift_min), abs(final_shift_sec)
  except Exception as e:
    #print(f"{e}")
    break_overall = 0
    final_shift_hours = (int(end_time[0:2]) - int(start_hours)) - int(break_overall_hours)
    final_shift_min = (int(end_time[3:5]) - int(start_min)) - int(break_overall_min)
    final_shift_sec = (int(end_time[6:8]) - int(start_sec)) - int(break_overall_sec)

    
    return abs(final_shift_hours), abs(final_shift_min), abs(final_shift_sec)

async def shiftLogFunc(type, time, interaction, bot):
  con = sqlite3.connect("cogs/data/bot_server.db")
  cur = con.cursor()

  res = cur.execute(f"SELECT shift_channel_id FROM setup_servers WHERE guild_id = '{interaction.guild.id}'")
  result = res.fetchone()
  shift_channel_id = result[0]
  shift_channel = bot.get_channel(shift_channel_id)

  embed = nextcord.Embed(title=f"{interaction.user}", description=f"", color=nextcord.Color.from_rgb(47,49,54))
  embed.add_field(name="Type:", value=f"{type}", inline=False)
  embed.add_field(name="Time(UTC)", value=f"`{time}`", inline=False)
  embed.set_footer(text=f"Shift Logging")

  await shift_channel.send(embed=embed)

async def punishLogFunc(type, time, interaction, bot):
  con = sqlite3.connect("cogs/data/bot_server.db")
  cur = con.cursor()

  res = cur.execute(f"SELECT punishment_channel_id FROM setup_servers WHERE guild_id = '{interaction.guild.id}'")
  result = res.fetchone()
  punishment_channel_id = result[0]
  punishment_channel = bot.get_channel(punishment_channel_id)

  embed = nextcord.Embed(title=f"{interaction.user}", description=f"", color=nextcord.Color.from_rgb(47,49,54))
  embed.add_field(name="Type:", value=f"{type}", inline=False)
  embed.add_field(name="Time(UTC)", value=f"`{time}`", inline=False)
  embed.set_footer(text=f"Punishment Logging")

  await punishment_channel.send(embed=embed)

async def create_id(interaction, type):
  unique_id = 0
  kickSTR = ""
  warnSTR = []
  banSTR = []
  kickNUM = 0
  warnNUM = 0
  banNUM = 0

  con = sqlite3.connect("cogs/data/bot_server.db")
  cur = con.cursor()

  try:

    if type == "kick_log":
      kickLOG = cur.execute(f"SELECT kick_id FROM kick_log")
      kicks = kickLOG.fetchall()
      if not kicks:
        return f"{type}-1"
      else:
        kicks = kicks[-1]
        for letter in kicks:
            kickSTR += letter

        length = len(kickSTR) + 1
        kickNUM = kickSTR[9:length]
          
        kickNUM = int(kickNUM)
        
        unique_id = kickNUM + 1
        unique_id = f"{type}-{unique_id}"
        return unique_id

    if type == "warn_log":
      warnLOG = cur.execute(f"SELECT warn_id FROM warn_log")
      warns = warnLOG.fetchall()
      if not warns:
        return f"{type}-1"
      else:
        warns = warns[-1]
        for letter in warns:
            warnSTR += letter

        length = len(warnSTR) + 1
        warnNUM = warnSTR[9:length]
          
        warnNUM = int(warnNUM)
        
        unique_id = warnNUM + 1
        unique_id = f"{type}-{unique_id}"
        return unique_id

    elif type == "ban_log":
      banLOG = cur.execute(f"SELECT ban_id FROM ban_log")
      bans = banLOG.fetchall()
      if not bans:
        return f"{type}-1"
      else:
        bans = bans[-1]
        for letter in bans:
            banSTR += letter

        length = len(banSTR) + 1
        banNUM = banSTR[9:length]
          
        banNUM = int(banNUM)
        
        unique_id = banNUM + 1
        unique_id = f"{type}-{unique_id}"
        return unique_id

      
    
    
  except Exception as e:
    print(e)
    return "Something went wrong"

async def checkIfStaff(interaction):
  return

async def checkIfManagement(interaction):
  return