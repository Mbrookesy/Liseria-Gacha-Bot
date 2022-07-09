from discord.ext import commands
from config.database_service import *


class DailyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        if await check_if_registered(ctx.author.id, ctx):
            gold_amount = 500

            await add_gold(ctx.author.id, gold_amount, ctx)

            await ctx.send(f"Daily applied, {gold_amount} gold added.")
