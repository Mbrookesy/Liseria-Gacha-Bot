from discord.ext import commands


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        await ctx.send(help_message)

#To Do - Make a better Help Section (Possible pages?)
help_message = """```Help Section (WIP):

To use the bot to its full capabilities please use the l!register command to register yourself.

Commands:
l!abgame - Starts an AB Game.
l!balance - Shows the amount of gold in the user's wallet.
l!blackjack - Starts a game of Blackjack.
l!daily - Gives you an amount of gold per day (24 Hour Cooldown)
l!help - Provides a help section for the user.

```"""