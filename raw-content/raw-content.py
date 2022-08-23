import discord
from discord.ext import commands
from core import checks
from core.models import PermissionLevel

class Raw(commands.Cog):
  def __init__(self, bot):
      self.bot = bot
      self.db = bot.api.get_plugin_partition(self)

  @commands.group(help="Get raw content of an embed", invoke_without_command=True)
  @checks.has_permissions(PermissionLevel.SUPPORTER)
  async def raw(self, ctx, message_id):
    if not message_id.isnumeric():
      return await ctx.send("Please provide an integer ID for a message in this channel.")
    try:
      message = await ctx.channel.fetch_message(int(message_id))
    except:
      return await ctx.send("That is not a valid message ID in this channel.")
    if len(message.embeds) == 0:
      return await ctx.send("There is no content to make raw! (No embeds).")
    await ctx.send(message.embeds[0].description)
  
  @raw.command(name="codeblock", aliases=['cb'], description="Get raw content from an embed (in codeblock)")
  @checks.has_permissions(PermissionLevel.SUPPORTER)
  async def raw_codeblock(self, ctx, message_id):
    if not message_id.isnumeric():
      return await ctx.send("Please provide an integer ID for a message in this channel.")
    try:
      message = await ctx.channel.fetch_message(int(message_id))
    except:
      return await ctx.send("That is not a valid message ID in this channel.")
    if len(message.embeds) == 0:
      return await ctx.send("There is no content to make raw! (No embeds).")
    await ctx.send(f"```\n{message.embeds[0].description}\n```")

  @commands.command()
  @checks.has_permissions(PermissionLevel.OWNER)
  async def testdb(self, ctx, *, content: str):
    await self.db.find_one_and_update({'_id': 'config'}, {'$set': {'test_content': content}}, upsert=True)
    await ctx.send(f"Successfully set `content` as:\n>>> {content}")

def setup(bot):
    bot.add_cog(Raw(bot))
