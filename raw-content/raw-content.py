from discord.ext import commands

class Hello(commands.Cog):
  def __init__(self, bot):
      self.bot = bot

  @commands.command(help="Get raw content of an embed")
  async def raw(self, ctx, message_id):
    if not message_id.isnumeric():
      return await ctx.send("Please provide an integer ID for a message in this channel.")
    try:
      message = await ctx.channel.fetch_message(int(message_id))
    except:
      return await ctx.send("That is not a valid message ID in this channel.")
    if len(message.embeds) == 0:
      return await ctx.send("There is not content to make raw! (No embeds).")
    await ctx.send(message.embeds[0].description)

def setup(bot):
    bot.add_cog(Hello(bot))
