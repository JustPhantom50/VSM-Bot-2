import nextcord
import os
import json
from nextcord.ext import commands 
import sqlite3
from nextcord.ui import Select, View
from cogs.utils.api import *

#pip install ffmpeg-python
intents = nextcord.Intents().all()
bot = commands.Bot(command_prefix="vsm.", intents=intents)
bot.remove_command('help')

#DO NOT DELETE THIS OR ELSE I WILL DO THE FUNNY
# class MySelect(Select):
#   def __init__(self) -> None:
#     super().__init__(min_values=2, max_values=4, placeholder="Make a Selection", row=2, options=[
#     nextcord.SelectOption(label="hi", value="0x1", description="hello there"),
#     nextcord.SelectOption(label="hello", description="hi there"),
#     nextcord.SelectOption(label="hehe", description="hi there"),
#     nextcord.SelectOption(label="hoho", description="hi there"),
#     nextcord.SelectOption(label="nono", description="hi there"),
#   ],)
#   async def callback(self, interaction):
#     if self.values[0] == "0x1":
#       print("oh hi")
#     await interaction.response.send_message(f"You chose {self.values}")


@bot.event
async def on_ready():
  await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name=f"In development!"))
  
  con = sqlite3.connect("cogs/data/bot_server.db")
  cur = con.cursor()
  cur.execute("DROP TABLE shifts")
  cur.execute("DROP TABLE setup_servers")
  cur.execute("DROP TABLE management")
  cur.execute("DROP TABLE kick_log")
  cur.execute("DROP TABLE warn_log")
  cur.execute("DROP TABLE ban_log")
  
  cur.execute("CREATE TABLE shifts(id INTEGER NOT NULL PRIMARY KEY, user_id INTEGER NOT NULL, shift_start NVARCHAR(50) NOT NULL, shift_end NVARCHAR(50), break_start NVARCHAR(50), break_end NVARCHAR(50), guild_id NVARCHAR(40) NOT NULL)")
  cur.execute("CREATE TABLE setup_servers(guild_id INTEGER NOT NULL PRIMARY KEY, shift_role_id INTEGER, shift_channel_id INTEGER, shift_reqirement INTEGER, staff_channel_id INTEGER, staff_role_id NVARCHAR(40), management_role_id NVARCHAR(40), loa_role_id NVARCHAR(40), punishment_channel_id INTEGER)")
  cur.execute("CREATE TABLE management(user_id INTEGER NOT NULL PRIMARY KEY, shift_time NVARCHAR(50), guild_id NVARCHAR(40) NOT NULL)")
  cur.execute("CREATE TABLE kick_log(id INTEGER NOT NULL PRIMARY KEY, user_id NVARCHAR(40) NOT NULL, kick_reason NVARCHAR(1000), kick_id NVARCHAR(40), guild_id NVARCHAR(40) NOT NULL)")
  cur.execute("CREATE TABLE warn_log(id INTEGER NOT NULL PRIMARY KEY, user_id NVARCHAR(40) NOT NULL, warn_reason NVARCHAR(1000), warn_id NVARCHAR(40), guild_id NVARCHAR(40) NOT NULL)")
  cur.execute("CREATE TABLE ban_log(id INTEGER NOT NULL PRIMARY KEY, user_id NVARCHAR(40) NOT NULL, ban_reason NVARCHAR(1000), ban_id NVARCHAR(40), guild_id NVARCHAR(40) NOT NULL)")
  con.commit()
  con.close()
  print(bot.user.name + " is ready.")

@bot.command(pass_context=True)
@commands.check(check_if_it_is_me)
async def get(ctx, extension):
  bot.load_extension(f"cogs.{extension}")
  await ctx.send("Command(s) was loaded!")

@bot.command(pass_context=True)
@commands.check(check_if_it_is_me)
async def delete(ctx, extension):
  bot.unload_extension(f"cogs.{extension}")
  await ctx.send("Command(s) was deleted!")

@bot.command(pass_context=True)
@commands.check(check_if_it_is_me)
async def reload(ctx, extension):
  bot.unload_extension(f"cogs.{extension}")
  bot.load_extension(f"cogs.{extension}")
  await ctx.send("Command(s) was reloaded!")

@bot.command()
async def testing(ctx):
  con = sqlite3.connect("cogs/data/bot_server.db")
  cur = con.cursor()
  res = cur.execute(f"SELECT * FROM setup_servers")
  result = res.fetchall()
  print(result)


for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(os.getenv('TOKEN'))
