from discord.ext import commands

class Hello(commands.Cog):
  def __init__(self, bot):
      self.bot = bot

  @commands.command(help="Get raw content of an embed")
  async def say(self, ctx, message_id):

def setup(bot):
    bot.add_cog(Hello(bot))
