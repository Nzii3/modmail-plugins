# A command to preview threads and thread info
import discord
from discord.ext import commands
from core import checks
from core.checks import PermissionLevel

class Preview(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.db = self.bot.plugin_db.get_partition(self)
  
  @checks.has_permissions(PermissionLevel.SUPPORTER)
  @commands.command(help="Preview a thread by ID or all")
  async def preview(self, ctx, thread_id=None):
    data = await self.db.find_one()
    await ctx.send(data)
    
async def setup(bot):
  await bot.add_cog(Preview(bot))
