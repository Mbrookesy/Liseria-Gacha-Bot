import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import logging

from commands.abgame import AbGameCog
from commands.blackjack import BlackjackCog
from commands.register import RegisterCog
from commands.daily import DailyCog
from commands.balance import BalanceCog
from commands.help import HelpCog

from config.database_setup import database_setup

logging.basicConfig(level=logging.INFO)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

bot = commands.Bot(command_prefix="l!", help_command=None)


@bot.event
async def on_ready():
    database_setup()
    print(f"{bot.user} has connected to Discord!")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):

        num = error.retry_after
        hour = num // 3600
        num %= 3600
        minutes = num // 60
        num %= 60
        seconds = num

        await ctx.send(f'This command is on cooldown, you can use it in {round(hour)} hours {round(minutes)} minutes {round(seconds)} seconds')

# Adding each Command
bot.add_cog(AbGameCog(bot))
bot.add_cog(BlackjackCog(bot))
bot.add_cog(RegisterCog(bot))
bot.add_cog(DailyCog(bot))
bot.add_cog(BalanceCog(bot))
bot.add_cog(HelpCog(bot))

bot.run(TOKEN)
