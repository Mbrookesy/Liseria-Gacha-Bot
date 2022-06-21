import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import logging

from commands.abgame import AbGameCog
from commands.blackjack import BlackjackCog

logging.basicConfig(level=logging.INFO)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

bot = commands.Bot(command_prefix="l!")


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")

# Adding each Command
bot.add_cog(AbGameCog(bot))
bot.add_cog(BlackjackCog(bot))

bot.run(TOKEN)
