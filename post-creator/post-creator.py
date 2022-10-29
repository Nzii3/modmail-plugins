import discord
from core import checks
from core.models import PermissionLevel
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Argument
from .utils import *

class PostCreator(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.version = "1.0.0"

  @app_commands.command(name="forum-post", description="Create a forum post")
  async def forum_post(self, interaction, title: str, message: str, channel: Argument(discord.AppCommandOptionType.channel, required=False)):
    await interaction.response.defer(ephemeral=True)
    channel: discord.ForumChannel = channel or interaction.channel
    await channel.create_thread(name=title, message=message)
    await interaction.followup.send(content=f'{self.bot.sent_emoji} Successfully created forum post!', ephemeral=True)

async def setup(bot):
  await bot.add_cog(PostCreator(bot), guilds=[discord.Object(id=841407843529523200)])