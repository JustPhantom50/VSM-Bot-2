import nextcord
from nextcord.utils import get
from nextcord.ext import commands
from nextcord import Interaction
import datetime
import sqlite3
from cogs.utils.api import *
import asyncio
import re
from nextcord.ui import Select, View

#Inserts the shift data into the data base
async def insertShiftData(shift_channel, shift_role, shift_req, interaction):
  con = sqlite3.connect("cogs/data/bot_server.db")
  cur = con.cursor()
  try:
    res = cur.execute(f"SELECT guild_id FROM setup_servers WHERE guild_id = '{int(interaction.guild.id)}'")
    guild_id = res.fetchone()
    if guild_id == None:
      cur.execute(f"INSERT INTO setup_servers(guild_id, shift_role_id, shift_channel_id, shift_reqirement) VALUES ('{int(interaction.guild.id)}', '{int(shift_role)}', '{int(shift_channel)}', '{int(shift_req)}')")
    else:
      cur.execute(f"UPDATE setup_servers SET shift_role_id = '{int(shift_role)}', shift_channel_id = '{int(shift_channel)}', shift_reqirement = '{int(shift_req)}' WHERE guild_id = '{int(interaction.guild.id)}'")
  except:
    cur.execute(f"UPDATE setup_servers SET shift_role_id = '{int(shift_role)}', shift_channel_id = '{int(shift_channel)}', shift_reqirement = '{int(shift_req)}' WHERE guild_id = '{int(interaction.guild.id)}'")
  
  con.commit()
  con.close()

#inserts staff data into the data base
async def insertStaffData(staff_channel, staff_role, manage_role, loa_role, interaction):
  con = sqlite3.connect("cogs/data/bot_server.db")
  cur = con.cursor()
  try:
    res = cur.execute(f"SELECT guild_id FROM setup_servers WHERE guild_id = '{int(interaction.guild.id)}'")
    guild_id = res.fetchone()
    if guild_id == None:
      cur.execute(f"INSERT INTO setup_servers(guild_id, staff_channel_id, staff_role_id, management_role_id, loa_role_id) VALUES ('{int(interaction.guild.id)}', '{staff_channel}', '{staff_role}', '{manage_role}', '{loa_role}')")
    else:
      cur.execute(f"UPDATE setup_servers SET staff_channel_id = '{staff_channel}', staff_role_id = '{staff_role}', management_role_id = '{manage_role}', loa_role_id = '{loa_role}' WHERE guild_id = '{int(interaction.guild.id)}'")
  except:
    cur.execute(f"UPDATE setup_servers SET staff_channel_id = '{staff_channel}', staff_role_id = '{staff_role}', management_role_id = '{manage_role}', loa_role_id = '{loa_role}' WHERE guild_id = '{int(interaction.guild.id)}'")
  con.commit()
  con.close()

#inserts the punishment logging data into the data base
async def insertPunishData(punish_channel, interaction):
  con = sqlite3.connect("cogs/data/bot_server.db")
  cur = con.cursor()
  try:
    res = cur.execute(f"SELECT guild_id FROM setup_servers WHERE guild_id = '{int(interaction.guild.id)}'")
    guild_id = res.fetchone()
    if guild_id == None:
      cur.execute(f"INSERT INTO setup_servers(guild_id, punishment_channel_id) VALUES ('{int(interaction.guild.id)}', '{int(punish_channel)}')")
    else:
      cur.execute(f"UPDATE setup_servers SET punishment_channel_id = '{int(punish_channel)}' WHERE guild_id = '{int(interaction.guild.id)}'")
  except:
    cur.execute(f"UPDATE setup_servers SET punishment_channel_id = '{int(punish_channel)}' WHERE guild_id = '{int(interaction.guild.id)}'")
  con.commit()
  con.close()

#these are the setup options
class setUpOptions():
  def __init__(self, bot):
    super().__init__(timeout=None)
    self.bot = bot

    #this is the shift setup options
  async def shift_setup(self, interaction):
    async def channelcallback(interaction):
      await interaction.response.defer(ephemeral=False)
      shift_channel = nextcord.utils.get(interaction.guild.channels, name=str(select_channel.values[0]))
      shift_channel_id = shift_channel.id
      self.shift_returns.append(shift_channel_id)
        
    async def rolecallback(interaction):
      await interaction.response.defer(ephemeral=False)
      shift_role = nextcord.utils.get(interaction.guild.roles, name=str(select_role.values[0]))
      shift_role_id = shift_role.id
      self.shift_returns.append(shift_role_id)
    try:
      em = nextcord.Embed(title=f"", description=f"What channel do you wish to use for shift management? (e.g Shift startups.)", color = nextcord.Color.green())
      select_channel = nextcord.ui.ChannelSelect(placeholder="Select A Channel", min_values=1, max_values=1)
      select_channel.callback = channelcallback
      view=View()
      view.add_item(select_channel)
      em1 = await interaction.followup.send(embed = em, view=view)
      await self.bot.wait_for('interaction', timeout=600.0, check=lambda message: message.user == interaction.user)
      await em1.delete()
  
      em = nextcord.Embed(title=f"", description=f"What role(s) would you like to be assigned to staff members when they start a shift?", color = nextcord.Color.green())
      select_role = nextcord.ui.RoleSelect(placeholder="Select A Role", min_values=1, max_values=1)
      select_role.callback = rolecallback
      view=View()
      view.add_item(select_role)
      em2 = await interaction.followup.send(embed = em, view=view)
      await self.bot.wait_for('interaction', timeout=60.0, check=lambda message: message.user == interaction.user)
      await em2.delete()
      
      
      
  
      em = nextcord.Embed(title=f"", description="What would you like the weekly shift requirement to be? (d/h/m/s... put `skip` to skip this question)", color = nextcord.Color.green())
      em3 = await interaction.followup.send(embed=em)
      
      reg = r"((\d+)[d])?((\d+)[h])?((\d+)[m])?((\d+)[s])?([a-z]+)?"
      time = []
      time_str = ""
      
      amount = await self.bot.wait_for('message', timeout=60.0, check=lambda message: message.author == interaction.user)
      for x in amount.content:
        time_str += x
      match = re.search(reg, time_str)

      if match.group(9) == 'skip':
        pass
      elif match.group(9) == None:
        pass
      else:
        embed = nextcord.Embed(title="Something Happened!", description=f"Something happened which you need to redo the setup, please make sure you follow the correct method, there will be examples below(If you have any questions please contact support)\n\n`1h1m0s`\t`1m0s`\t`20s`\t`1h`\t`1h12s`\t`12m40s`\n`skip`")
        return await interaction.followup.send(embed=embed, delete_after=5)
        
        
      for item in match.groups():
        
        if item == None:
          time.append("0")
        elif item == "skip":
          time.append("skip")
        else:
          time.append(item)
      try:
        if time[8] == "skip":
          shift_req = 0;
        else:
          shift_req = (int(time[1]) * 24 * 60 * 60) + (int(time[3]) * 3600) + (int(time[5]) * 60) + (int(time[7]))
 
      except:
        
        embed = nextcord.Embed(title="Something Happened!", description=f"Something happened which you need to redo the setup, please make sure you follow the correct method, there will be examples below(If you have any questions please contact support)\n\n`1h1m0s`\t`1m0s`\t`20s`\t`1h`\t`1h12s`\t`12m40s`\n`skip`")
        return await interaction.followup.send(embed=embed, delete_after=5)

      await insertShiftData(int(self.shift_returns[0]), int(self.shift_returns[1]), shift_req, interaction)
      await amount.delete()
      await em3.delete()
      return True
    except asyncio.TimeoutError:
      em = nextcord.Embed(title="Timeout", description="You took to long to respond! Please reset-up the bot.", color=nextcord.Color.red())
      return await interaction.followup.send(embed=em)
      
#staff setup options
  async def staff_setup(self, interaction):
    async def staffChannel(interaction):
      await interaction.response.defer(ephemeral=False)
      cstaff_Channel = nextcord.utils.get(interaction.guild.channels, name=str(staff_Select.values[0]))
      cstaff_Channel = cstaff_Channel.id
      self.staff_returns.append(cstaff_Channel)
        
    async def staffRoles(interaction):
      await interaction.response.defer(ephemeral=False)
      
      for role in staff_Roles_select.values:
        cstaff_Roles = nextcord.utils.get(interaction.guild.roles, name=str(role))
        cstaff_Roles = cstaff_Roles.id
        self.staff_roles_returns.append(cstaff_Roles)
        
    async def manageRoles(interaction):
      await interaction.response.defer(ephemeral=False)
      for role in manage_Roles_select.values:
        cmanage_Roles = nextcord.utils.get(interaction.guild.roles, name=str(role))
        cmanage_Roles = cmanage_Roles.id
        self.manage_roles_returns.append(cmanage_Roles)
        
    async def loaRoles(interaction):
      await interaction.response.defer(ephemeral=False)
      for role in loa_Roles_select.values:
        cloa_Roles = nextcord.utils.get(interaction.guild.roles, name=str(role))
        cloa_Roles = cloa_Roles.id
        self.loa_roles_returns.append(cloa_Roles)
    try:
      
      em = nextcord.Embed(title=f"", description=f"What channel would you like to use for staff management?", color = nextcord.Color.green())
      staff_Select = nextcord.ui.ChannelSelect(placeholder="Select A Channel", min_values=1, max_values=1)
      staff_Select.callback = staffChannel
      staffCView=View()
      staffCView.add_item(staff_Select)
      em1 = await interaction.followup.send(embed = em, view=staffCView)
      await self.bot.wait_for('interaction', timeout=60.0, check=lambda message: message.user == interaction.user)
      await em1.delete()
      
  
      em = nextcord.Embed(title=f"", description=f"Please mention all of your staff role(s) (e.g. @staff,@staff 2 ect)", color = nextcord.Color.green())
      staff_Roles_select = nextcord.ui.RoleSelect(placeholder="Select A Role", min_values=1, max_values=10)
      staff_Roles_select.callback = staffRoles
      staffView=View()
      staffView.add_item(staff_Roles_select)
      em2 = await interaction.followup.send(embed = em, view=staffView)
      await self.bot.wait_for('interaction', timeout=60.0, check=lambda message: message.user == interaction.user)
      await em2.delete()
      
      
  
      em = nextcord.Embed(title=f"", description=f"Please mention all of your management role(s) (e.g. @management,@management 2 ect)", color = nextcord.Color.green())
      manage_Roles_select = nextcord.ui.RoleSelect(placeholder="Select A Role", min_values=1, max_values=10)
      manage_Roles_select.callback = manageRoles
      mamagView=View()
      mamagView.add_item(manage_Roles_select)
      em3 = await interaction.followup.send(embed = em, view=mamagView)
      await self.bot.wait_for('interaction', timeout=60.0, check=lambda message: message.user == interaction.user)
      await em3.delete()
      
      
  
      em = nextcord.Embed(title=f"", description=f"What role(s) would you like to be given when someone requests an LoA?", color = nextcord.Color.green())
      loa_Roles_select = nextcord.ui.RoleSelect(placeholder="Select A Role", min_values=1, max_values=10)
      loa_Roles_select.callback = loaRoles
      loaView=View()
      loaView.add_item(loa_Roles_select)
      em4 = await interaction.followup.send(embed = em, view=loaView)
      await self.bot.wait_for('interaction', timeout=60.0, check=lambda message: message.user == interaction.user)
      await em4.delete()
      
      

      await interaction.followup.send("Loading...", delete_after=0)
      await insertStaffData(self.staff_returns[0], self.staff_roles_returns, self.manage_roles_returns, self.loa_roles_returns, interaction)
      return True
    except asyncio.TimeoutError:
      em = nextcord.Embed(title="Timeout", description="You took to long to respond! Please reset-up the bot.", color=nextcord.Color.red())
      return await interaction.followup.send(embed=em)

    #punishment logging setup options
  async def punish_setup(self, interaction):
    punish_returns = []
    async def punishcallback(interaction):
      await interaction.response.defer(ephemeral=False)
      punish_channel = nextcord.utils.get(interaction.guild.channels, name=str(select_punish.values[0]))
      punish_channel = punish_channel.id
      
      punish_returns.append(punish_channel)
      
    try:
     
      em = nextcord.Embed(title=f"", description=f"What channel do you wish to use for punishment logging?", color = nextcord.Color.green())
      select_punish = nextcord.ui.ChannelSelect(placeholder="Select A Channel", min_values=1, max_values=1)
      select_punish.callback = punishcallback
      view=View()
      view.add_item(select_punish)
      em1 = await interaction.followup.send(embed = em, view=view)
      await self.bot.wait_for('interaction', timeout=60.0, check=lambda message: message.user == interaction.user)
      await em1.delete()
      await interaction.followup.send("Loading...", delete_after=0)
      await insertPunishData(punish_returns[0], interaction)
      return True
    except asyncio.TimeoutError:
      em = nextcord.Embed(title="Timeout", description="You took to long to respond! Please reset-up the bot.", color=nextcord.Color.red())
      return await interaction.followup.send(embed=em)


class SetupPanel(nextcord.ui.View):
  def __init__(self, ctx, bot):
    super().__init__(timeout=10)
    self.ctx = ctx
    self.bot = bot
    self.shift_returns = []
    self.staff_returns = []
    self.punish_returns = []
    self.staff_roles_returns = []
    self.manage_roles_returns = []
    self.loa_roles_returns = []

#setup embed & buttons
  @nextcord.ui.button(label="All", style=nextcord.ButtonStyle.green)
  async def all_button(self, button: nextcord.ui.Button, interaction: Interaction):
    await interaction.response.defer(ephemeral=False)
    staff_setup = await setUpOptions.staff_setup(self, interaction)
    if staff_setup == True:
      punish_setup = await setUpOptions.punish_setup(self, interaction)
      if punish_setup == True:
        shift_setup = await setUpOptions.shift_setup(self, interaction)
        if shift_setup == True:
          em = nextcord.Embed(title="Success", description="Your server is now all set-up you may now use VSM!", color=nextcord.Color.green())   
          await interaction.followup.send(embed=em)
    else:
      em = nextcord.Embed(title="Something Happened", description="Soemthing wrong happened while setting up, please contact support!", color=nextcord.Color.red())   
      return await interaction.followup.send(embed=em)
    # if staff_setup == True and punish_setup == True and shift_setup == True:
    #   em = nextcord.Embed(title="Success", description="Your server is now all set-up you may now use VSM!", color=nextcord.Color.green())   
    #   await interaction.followup.send(embed=em)
    
  @nextcord.ui.button(label="Shift Management", style=nextcord.ButtonStyle.blurple)
  async def shift_button(self, button: nextcord.ui.Button, interaction: Interaction):
    await interaction.response.defer(ephemeral=False)
    is_setup = await setUpOptions.shift_setup(self, interaction)
    if is_setup == True:
      em = nextcord.Embed(title="Success", description="Your server is now all set-up!", color=nextcord.Color.green())
      await interaction.followup.send(embed=em)

  @nextcord.ui.button(label="Staff Management", style=nextcord.ButtonStyle.blurple)
  async def staff_button(self, button: nextcord.ui.Button, interaction: Interaction):
    await interaction.response.defer(ephemeral=False)
    is_setup = await setUpOptions.staff_setup(self, interaction)
    if is_setup == True:
      em = nextcord.Embed(title="Success", description="Your server is now all set-up!", color=nextcord.Color.green())
      await interaction.followup.send(embed=em)
    

  @nextcord.ui.button(label="Punishment Logging", style=nextcord.ButtonStyle.blurple)
  async def punishments_button(self, button: nextcord.ui.Button, interaction: Interaction):
    await interaction.response.defer(ephemeral=False)
    is_setup = await setUpOptions.punish_setup(self, interaction)

    if is_setup == True:
      em = nextcord.Embed(title="Success", description="Your server is now all set-up!", color=nextcord.Color.green())
      await interaction.followup.send(embed=em)

class preSetUpButtons(nextcord.ui.View):
  def __init__(self, ctx, bot):
    super().__init__(timeout=10)
    self.ctx = ctx
    self.bot = bot

  @nextcord.ui.button(label="Continue", style=nextcord.ButtonStyle.green)
  async def continue_button(self, button: nextcord.ui.Button, interaction: Interaction):
    await interaction.response.defer(ephemeral=False)
    em = nextcord.Embed(title="Set-up", description=f"Hello, {interaction.user.name}, please select your desired section to set-up.", color=nextcord.Color.blue())
    em.add_field(name=f"All", value=f"All features within the bot", inline=False)
    em.add_field(name=f"Shift Management", value=f"Set-up Shift Management", inline=False)
    em.add_field(name=f"Staff Management", value=f"Set-up LOA", inline=False)
    em.add_field(name=f"Punishments", value=f"Set-up kick, ban, and warn logs", inline=False)
    em.timestamp = datetime.datetime.utcnow()
    em.set_footer(text='VSM - Setup \u200b')
    view = SetupPanel(interaction, self.bot)
    msg = await interaction.followup.send(embed=em, view=view)
    inter = await self.bot.wait_for('interaction', timeout=None, check=lambda message: message.user == interaction.user)
    await msg.delete()
    for child in self.children:
      child.disabled = True
    
    

class setup_bot(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @nextcord.slash_command(description="setup the bot")
  async def setup(self, interaction: Interaction):
    await interaction.response.defer(ephemeral=False)

    em = nextcord.Embed(title="", description="Please make sure that you have given the appropriate permissions to VSM or else it will not work properly.", color=nextcord.Color.green())
    em.timestamp = datetime.datetime.utcnow()
    em.set_footer(text='VSM - Setup \u200b')
    view = preSetUpButtons(interaction, self.bot)
    msg = await interaction.followup.send(embed=em, view=view)
    inter = await self.bot.wait_for('interaction', timeout=None, check=lambda message: message.user == interaction.user)
    await msg.delete()
    
    
    
def setup(bot):
  bot.add_cog(setup_bot(bot))