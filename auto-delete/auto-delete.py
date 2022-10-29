import discord
from core import checks
from core.models import PermissionLevel
from discord.ext import commands
from .utils import *

class TypeFlags(commands.FlagConverter, prefix="?", delimiter=" "):
  type: str = commands.flag(aliases=['t'], default=None)

class SetFlags(commands.FlagConverter, prefix="?", delimiter=" "):
  set = None

class AutoDelete(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.db = bot.plugin_db.get_partition(self)
    self.version = "1.0.4b"

  """A plugin for automatically deleting messages from members that leave"""

  def success(self, message: str) -> discord.Embed:
    embed = discord.Embed(color=self.bot.main_color, description=message)
    return embed

  def error(self, message: str) -> discord.Embed:
    embed = discord.Embed(color=self.bot.error_color, description=message)
    return embed
  
  async def get_config(self):
    config = await self.db.find_one({'_id': 'config'})
    if config == None:
      await self.db.insert_one({'_id': 'config', 'channels': [], 'delete_limit': 100})
    config = await self.db.find_one({'_id': 'config'})
    return config

  async def update_config(self, key: str, data):
    config = await self.get_config() # make sure config is not None
    result = await self.db.find_one_and_update({'_id': 'config'}, {'$set': {key: data}})
    return result
  
  @commands.group(name="autodelete", aliases=['autodel'], description="Manage auto delete", invoke_without_command=True)
  @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
  async def autodelete(self, ctx):
    config = await self.get_config()
    if config['channels'] == []:
      channels = "*No channels set*"
    else:
      channels = "\n".join(f"• <#{c}>" for c in channels)
    limit = config['delete_limit']
    embed = discord.Embed(color=self.bot.main_color, description="These are the current configurations for **auto-delete**.")
    embed.set_author(name=f"{ctx.guild.name} - Auto-delete", icon_url=guild_icon(ctx.guild), url="https://github.com/Nzii3/modmail-plugins/tree/main/auto-delete")
    embed.add_field(name="Delete Limit", value=str(limit))
    embed.add_field(name="Auto-delete Channels", value=channels)
    embed.set_footer(text=f"v{self.version} • Auto-delete by vNziie--#7777")
    await ctx.send(embed=embed)
  
  @autodelete.command(name="limit", aliases=['messages'], help="Set the number of messages for the bot to search in each channel (less the better for bot latency)\n\n🚩 **Flags** 🚩\n>>> `?set <val>` - Sets the autodelete limit to `val`\n - *using no flags will show the autodelete limit*")
  @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
  async def autodelete_limit(self, ctx, *, flags: SetFlags):
    if flags.set == None:
      config = await self.get_config()
      embed = discord.Embed(color=self.bot.main_color, description=f"**{config['delete_limit']}** message(s)", title="Auto-delete Limit")
      embed.set_footer(text=f"Use '{ctx.prefix}help autodelete limit' for flag info")
      return await ctx.send(embed=embed)
    number = flags.set
    if not number.isnumeric():
      return await ctx.send("Please send a valid integer (number)!")
    if int(number) > 500:
      return await ctx.send("You can't provide a number above **500** to prevent Discord rate limits")
    if int(number) < 0:
      return await ctx.send("You can't provide a negative number.")
    await self.update_config(key="limit", data=number)
    await ctx.send(embed=self.success('Successfully set the message'))
  
  @autodelete.command(name="channels", help="View or add/remove auto-delete channels\n\n🚩 **Flags** 🚩\n\n>>> `?type <add|remove>` - Putting type as `add` will add `channels` and using `remove` will remove `channels`")
  @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
  async def autodelete_channels(self, ctx, channels: commands.Greedy[discord.TextChannel], *, flags: TypeFlags):
    if flags.type == None or flags.type.lower() not in ['add', 'remove', 'delete', 'del']:
      config = await self.get_config()
      embed = discord.Embed(color=self.bot.main_color, title="Auto-delete Channels", description="\n".join(f"<#{c}>" for c in config['channels']))
      embed.set_footer(text=f"Use '{ctx.prefix}help autodelete channels' for flag info")
      return await ctx.send(embed=embed)
    config = await self.get_config()
    channels = config['channels']
    TYPE = flags.type
    if TYPE.lower() == 'add':
      print(channels)
      complete = []
      errored = []
      for channel in channels:
        if channel.id in channels:
          errored.append({'channel': channel, 'error': 'Channel is already added'})
        channels.append(channel.id)
        complete.append({'channel': channel})
      desc = "\n".join(f"> ✅ {r['channel'].mention}" for r in complete)
      print(complete)
      await ctx.send(desc)
      EMBED = discord.Embed(color=discord.Colour.brand_green(), description=desc, title=f"✅ Successfully added channels")
      if errored != []:
        EMBED.add_field(name="Failed", value="\n".join(f"❌ {r['channel'].mention} - {r['error']}" for r in errored))
      return await ctx.send(embed=EMBED)
    if TYPE.lower() in ['delete', 'remove', 'del']:
      complete = []
      errored = []
      for channel in channels:
        if channel.id not in channels:
          errored.append({'channel': channel, 'error': 'Channel was never added'})
        try:
          channels.remove(channel.id)
          complete.append({'channel': channel})
        except:
          errored.append({'channel': channel, 'error': 'Channel was never added'})
      desc = "\n".join(f"> ✅ {r['channel'].mention}" for r in complete)
      EMBED = discord.Embed(color=discord.Colour.brand_green(), description=desc, title="🗑 Successfully removed channels")
      if errored != []:
        EMBED.add_field(name="Failed", value="\n".join(f"❌ {r['channel'].mention} - {r['error']}" for r in errored))
      return await ctx.send(embed=EMBED)

  
async def setup(bot):
  await bot.add_cog(AutoDelete(bot))
