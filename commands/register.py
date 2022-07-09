from discord.ext import commands
import sqlite3


class RegisterCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def register(self, ctx):
        conn = sqlite3.connect("gachaDatabase.db")
        try:
            conn.execute(f"""INSERT INTO USER (ID, GOLD)
            VALUES ({ctx.author.id}, 1000)""")
            conn.commit()
            await ctx.send("User has successfully been registered, you now have 1000 Gold.")
        except sqlite3.IntegrityError:
            await ctx.send("User is already registered")

        conn.close()




