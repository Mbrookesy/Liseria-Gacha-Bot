from discord.ext import commands
from config.database_service import *
import random


class FishCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def fish(self, ctx):
        if await check_if_registered(ctx.author.id, ctx):
            trash_or_fish = random.randrange(1, 21)
            trash = ["Boot", "Straw", "Bottle", "Rotten Apple"]
            fish_dict = {
                "Shrimp": 10,
                "Cod": 20,
                "Salmon": 50,
                "Eel": 100,
                "Lobster": 250,
                "Shark": 1000,
                "Whale": 10000
            }
            fish = list(fish_dict.keys())

            if trash_or_fish == 20:
                await ctx.send(f"You caught a {random.choice(trash)}, you earned 0 Gold")
            else:
                choice = random.choices(fish, weights=(50, 20, 10, 5, 1, 0.1, 0.0001), k=1000)
                await ctx.send(f"You caught a {choice[0]}, you earned {fish_dict[choice[0]]} Gold")
                await add_gold(ctx.author.id, fish_dict[choice[0]], ctx)
