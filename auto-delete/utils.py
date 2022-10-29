import discord

def guild_icon(guild: discord.Guild) -> str:
  try:
    icon_url = guild.icon.url
  except:
    icon_url = "https://cdn.discordapp.com/attachments/777767000520785950/934489467518070884/a.png"
  return icon_url