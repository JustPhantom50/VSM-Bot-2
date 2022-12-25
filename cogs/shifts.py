import nextcord
from nextcord.utils import get
from nextcord.ext import commands
from nextcord import Interaction
import datetime
import sqlite3
import time
from cogs.utils.api import *
import re

class ShiftPanel(nextcord.ui.View):
  def __init__(self, ctx, bot):
    super().__init__(timeout=None)
    self.ctx = ctx
    self.bot = bot

#this is the button to start a users shift
  @nextcord.ui.button(label="Start Shift", style=nextcord.ButtonStyle.green)
  async def Start_command(self, button: nextcord.ui.Button, interaction: Interaction):
    check = await shiftCheck(interaction)
    if check == "shift_already_started":
      
      em = nextcord.Embed(title="", description="You already started a shift!")
      return await interaction.message.edit(embed = em)
    else:
      
      t = time.localtime()
      current_time = time.strftime("%H:%M:%S", t)
  
      con = sqlite3.connect("cogs/data/bot_server.db")
      cur = con.cursor()
      cur.execute(f"INSERT INTO shifts(user_id, shift_start, guild_id) VALUES ('{int(interaction.user.id)}', '{current_time}', '{interaction.guild.id}')")
      res = cur.execute(f"SELECT shift_role_id, shift_channel_id FROM setup_servers WHERE guild_id = '{interaction.guild.id}'")
      result = res.fetchone()
      shift_role_id = result[0]
      shift_channel_id = result[1]
      shift_role = nextcord.utils.get(interaction.guild.roles, id = shift_role_id)
      shift_channel = self.bot.get_channel(shift_channel_id)
      await interaction.user.add_roles(shift_role)
      con.commit()
      con.close()
      
      em = nextcord.Embed(title=f"{interaction.user}", description=f"We have started your shift at {current_time}", color = nextcord.Color.green())
      await interaction.message.edit(embed=em)
  
      await shiftLogFunc("Shift Start", current_time, interaction, self.bot)

#button to end users shift
  @nextcord.ui.button(label="End Shift", style=nextcord.ButtonStyle.red)
  async def End_command(self, button: nextcord.ui.Button, interaction: Interaction):
    check = await shiftCheck(interaction)
    con = sqlite3.connect("cogs/data/bot_server.db")
    cur = con.cursor()
    res = cur.execute(f"SELECT user_id, break_start, break_end FROM shifts WHERE user_id = '{interaction.user.id}' AND guild_id = '{interaction.guild.id}'")
    break_info = res.fetchone()
    con.close()
    if break_info[1] != None and break_info[2] == None:
      em = nextcord.Embed(title="", description="Please end your break before you end your shift!")
      return await interaction.message.edit(embed=em)
    if check == True:
      
      em = nextcord.Embed(title="", description="Please start your shift!")
      return await interaction.message.edit(embed = em)
    else:
      
      t = time.localtime()
      current_time = time.strftime("%H:%M:%S", t)
      
  
      con = sqlite3.connect("cogs/data/bot_server.db")
      cur = con.cursor()
      shift_hours, shift_min, shift_sec = await end_shift_function(cur, interaction, current_time)
      shift_hours = abs(shift_hours)
      shift_min = abs(shift_min)
      shift_sec = abs(shift_sec)
      res = cur.execute(f"SELECT user_id, shift_time FROM management WHERE user_id = '{interaction.user.id}' AND guild_id = '{interaction.guild.id}'")
      result = res.fetchone()

      res2 = cur.execute(f"SELECT shift_role_id FROM setup_servers WHERE guild_id = '{interaction.guild.id}'")
      result2 = res.fetchone()
      shift_role_id = result2[0]
      shift_role = nextcord.utils.get(interaction.guild.roles, id = shift_role_id)
      

      reg = r"[0-9]{2}"
      if re.match(reg, str(shift_hours)) != None:
        shift_hours = shift_hours
        if re.match(reg, str(shift_min)) != None:
          shift_min = shift_min
        if re.match(reg, str(shift_sec)) != None:
          shift_sec = shift_sec
      
      if re.match(reg, str(shift_hours)) == None:
        shift_hours = f"0{shift_hours}"
        if re.match(reg, str(shift_min)) == None:
          shift_min = f"0{shift_min}"
        if re.match(reg, str(shift_sec)) == None:
          shift_sec = f"0{shift_sec}"
      
      if result != None:
        time_li = []
        for num in result[1]:
          time_li.append(num)
        
        time_str = ""
        for num in time_li:
          time_str += num
        print(time_str)
        
        
        final_time_hours = int(shift_hours) + int(time_str[0:2])
        final_time_min = int(shift_min) + int(time_str[3:5])
        final_time_sec = int(shift_sec) + int(time_str[6:8])

        reg = r"[0-9]{2}"
        if re.match(reg, str(final_time_hours)) != None:
          final_time_hours = final_time_hours
          if re.match(reg, str(final_time_min)) != None:
            final_time_min = final_time_min
          if re.match(reg, str(final_time_sec)) != None:
            final_time_sec = final_time_sec
        
        if re.match(reg, str(final_time_hours)) == None:
          final_time_hours = f"0{final_time_hours}"
          if re.match(reg, str(final_time_min)) == None:
            final_time_min = f"0{final_time_min}"
          if re.match(reg, str(final_time_sec)) == None:
            final_time_sec = f"0{final_time_sec}"
          
        cur.execute(f"UPDATE management SET shift_time = '{final_time_hours}:{final_time_min}:{final_time_sec}' WHERE user_id = '{interaction.user.id}' AND guild_id = '{interaction.guild.id}'")
        cur.execute(f"DELETE FROM shifts WHERE user_id = '{interaction.user.id}'")
        em = nextcord.Embed(title=f"{interaction.user}", description=f"We have ended your shift at `{current_time} UTC`, with `{shift_hours}:{shift_min}:{shift_sec}` time", color = nextcord.Color.green())
        em.set_footer(text=f"Your total shift time: {final_time_hours}:{final_time_min}:{final_time_sec}")
        await interaction.user.remove_roles(shift_role)
        await interaction.message.edit(embed=em)
      else:
          
        cur.execute(f"INSERT INTO management(user_id, shift_time, guild_id) VALUES ('{int(interaction.user.id)}', '{shift_hours}:{shift_min}:{shift_sec}', '{interaction.guild.id}')")
        cur.execute(f"DELETE FROM shifts WHERE user_id = '{interaction.user.id}'")
        em = nextcord.Embed(title=f"{interaction.user}", description=f"We have ended your shift at `{current_time} UTC`, with `{shift_hours}:{shift_min}:{shift_sec}` time", color = nextcord.Color.green())
        await interaction.user.remove_roles(shift_role)
        await interaction.message.edit(embed=em)
      await shiftLogFunc("Shift End", current_time, interaction, self.bot)
      con.commit()
      con.close()

#Button to put a user on brake
  @nextcord.ui.button(label="Start Break", style=nextcord.ButtonStyle.blurple )
  async def Break_start(self, button: nextcord.ui.Button, interaction: Interaction):
    check = await shiftCheck(interaction)
    if check == True:
      
      em = nextcord.Embed(title="", description="Please start your shift")
      await interaction.message.edit(embed = em)
    elif check == "break_already_started":
      
      em2 = nextcord.Embed(title="", description="You have already started your break")
      await interaction.message.edit(embed = em2)
    else:
      
      t = time.localtime()
      current_time = time.strftime("%H:%M:%S", t)
  
      con = sqlite3.connect("cogs/data/bot_server.db")
      cur = con.cursor()
      cur.execute(f"UPDATE shifts SET break_start = '{current_time}' WHERE user_id = '{int(interaction.user.id)}' AND guild_id = '{interaction.guild.id}'")
      res = cur.execute(f"SELECT break_start FROM shifts WHERE user_id = '{interaction.user.id}' AND guild_id = '{interaction.guild.id}'")
      time_s = res.fetchone()
      
      con.commit()
      con.close()
      
      em = nextcord.Embed(title=f"{interaction.user}", description=f"We have started your break at {current_time}", color = nextcord.Color.green())
      await interaction.message.edit(embed=em)
      await shiftLogFunc("Break Start", current_time, interaction, self.bot)

    #end a users brake
  @nextcord.ui.button(label="End Break", style=nextcord.ButtonStyle.blurple )
  async def Break_end(self, button: nextcord.ui.Button, interaction: Interaction):
    check = await shiftCheck(interaction)
    if check == True:
      
      em = nextcord.Embed(title="", description="Please start your shift")
      await interaction.message.edit(embed = em)
    elif check == "break_already_ended":
      
      em2 = nextcord.Embed(title="", description="Please start a break")
      await interaction.message.edit(embed = em2)
    else:
      
      t = time.localtime()
      current_time = time.strftime("%H:%M:%S", t)

      con = sqlite3.connect("cogs/data/bot_server.db")
      cur = con.cursor()
      cur.execute(f"UPDATE shifts SET break_end = '{current_time}' WHERE user_id = '{int(interaction.user.id)}' AND guild_id = '{interaction.guild.id}'")
      res = cur.execute(f"SELECT break_end FROM shifts WHERE user_id = '{interaction.user.id}' AND guild_id = '{interaction.guild.id}'")
      time_s = res.fetchone()
      con.commit()
      con.close()
      
      em = nextcord.Embed(title=f"{interaction.user}", description=f"We have ended your break at {current_time}", color = nextcord.Color.green())
      await interaction.message.edit(embed=em)
      await shiftLogFunc("Break End", current_time, interaction, self.bot)

class shift_management(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    #self.mreminder.start(interaction)

  @tasks.loop(seconds=604800.0)
  async def mreminder(self, interaction):
    con = sqlite3.connect("cogs/data/bot_server.db")
    cur = con.cursor()
    cur.execute(f"SELECT staff_role_id FROM setup_servers WHERE guild_id = '{interaction.guild.id}'")
    em = nextcord.Embed(title="This is an M Command Reminder", description=f"`:m 🍁 Welcome to Greater Vancouver Roleplay! Feel free to join our communications to join more sessions like these: x-N-j-C-b-z-z-K-2-p (No Dashes)\n\n:m 👮‍♂️ Our staff team is hiring! Join our communications to apply! Code: x-N-j-C-b-z-z-K-2-p (No Dashes)`", color=nextcord.Color.from_rgb(255, 255, 254))
    await channel.send(embed=em)

    #this is used to manage someones shift
  @nextcord.slash_command(description="Manage Your Shift")
  async def shift(self, interaction: Interaction):
    return

  @shift.subcommand(description="Manage Your Shift")
  async def manage(self, interaction: Interaction):
    await interaction.response.defer(ephemeral=False)
    is_setup = await checkSetUp(interaction, "shift")
    if is_setup == False:
      return
    elif is_setup == True:
      em = nextcord.Embed(title="Manage Your Shifts", description=f"Hello, {interaction.user.name}, please select an option below.", color=nextcord.Color.blue())
      view = ShiftPanel(interaction, self.bot)
      await interaction.followup.send(embed=em, view=view)
def setup(bot):
  bot.add_cog(shift_management(bot))