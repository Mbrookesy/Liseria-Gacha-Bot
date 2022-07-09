from discord.ext import commands
from config.database_service import *


class BalanceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def balance(self, ctx):
        if await check_if_registered(ctx.author.id, ctx):
            await check_gold(ctx.author.id, ctx)
