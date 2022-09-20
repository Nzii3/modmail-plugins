import discord
from core import checks
from core.models import PermissionLevel
from discord.ext import commands

class AutoDelete(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.db = bot.plugin_db.get_partition(self)
    self.version = "1.0.4b"

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
    embed = discord.Embed(color=discord.Colour.blurple(), description="These are the current configurations for **auto-delete**.")
    embed.set_author(name=f"{ctx.guild.name} - Auto-delete", icon_url=ctx.guild.icon_url, url="https://github.com/Nzii3/modmail-plugins/tree/main/auto-delete")
    embed.add_field(name="Delete Limit", value=str(limit))
    embed.add_field(name="Auto-delete Channels", value=channels)
    embed.set_footer(text=f"Auto-delete v{self.version} • Auto-delete by vNziie--#7777")
    await ctx.send(embed=embed)
  
  @autodelete.command(name="limit", aliases=['messages'], help="Set the number of messages for the bot to search in each channel (less the better for bot latency)")
  @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
  async def autodelete_limit(self, ctx, number):
    if not number.isnumeric():
      return await ctx.send("Please send a valid integer (number)!")
    if int(number) > 500:
      return await ctx.send("You can't provide a number above **500** to prevent Discord rate limits")
    if int(number) < 0:
      return await ctx.send("You can't provide a negative number.")
    await self.update_config(key="limit", data=number)
    await ctx.send(embed=self.success('Successfully set the message'))
  
  @autodelete.command(name="channels", help="View or add/remove auto-delete channels")
  @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
  async def autodelete_channels(self, ctx, channels: commands.Greedy[discord.TextChannel]):
    return await ctx.send(embed=self.error('This command is still in development!'))
  
def setup(bot):
  bot.add_cog(AutoDelete(bot))
