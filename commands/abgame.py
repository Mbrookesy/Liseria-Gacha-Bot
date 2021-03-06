from discord.ext import commands
from config.database_service import *
import random

double_ally_increase = 2
double_betray_increase = 0
betraying_ally_increase = 3
being_betrayed_decrease = -2

#To Do - Make a better interface for this (Buttons?)
class AbGameCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def abgame(self, ctx):
        if await check_if_registered(ctx.author.id, ctx):
            async def rules():
                await ctx.send(rules_message)

            async def game():

                user_points = 3
                cpu_points = 3

                cpu_choices = ["Ally", "Betray"]

                while (user_points < 9 and cpu_points < 9) and (user_points > 0 or cpu_points > 0):
                    await ctx.send(generate_game_start_message(user_points, cpu_points))

                    game_message = await self.bot.wait_for("message", check=lambda msg: msg.author == ctx.author,
                                                           timeout=60.0)

                    input_game_value = game_message.content

                    cpu_pick = random.choice(cpu_choices)

                    if input_game_value == "2":
                        await ctx.send("```You have chosen, Betray.```")
                        player_pick = "Betray"
                    else:
                        await ctx.send("```You have chosen, Ally.```")
                        player_pick = "Ally"

                    await ctx.send("```Here are your results.```")

                    if player_pick == "Ally" and cpu_pick == "Ally":
                        user_points = user_points + double_ally_increase
                        cpu_points = cpu_points + double_ally_increase
                    elif player_pick == "Ally" and cpu_pick == "Betray":
                        user_points = user_points + being_betrayed_decrease
                        cpu_points = cpu_points + betraying_ally_increase
                    elif player_pick == "Betray" and cpu_pick == "Ally":
                        user_points = user_points + betraying_ally_increase
                        cpu_points = cpu_points + being_betrayed_decrease
                    else:
                        user_points = user_points + double_betray_increase
                        cpu_points = cpu_points + double_betray_increase

                    await ctx.send(f"```The opponent picked {cpu_pick}```")

                await ctx.send("```The game has finished.```")

                if cpu_points <= 0 and user_points <= 0:
                    await ctx.send(f"```You have both perished. Game Over. You gain 0 Gold.```")
                elif cpu_points > 0 and user_points <= 0:
                    await ctx.send(f"```You have perished. Your opponent is now able to win. Game Over. You gain 0 Gold.```")
                elif cpu_points <= 0 and user_points < 0:
                    await ctx.send(f"```Your opponent has perished. You are now able to win. Congratulations. You gain 100 Gold.```")
                    await add_gold(ctx.author.id, 100, ctx)
                elif cpu_points > 9 and user_points > 9:
                    await ctx.send(f"```You have both reached 9 BP, Congratulations! You are both free. You gain 50 Gold.```")
                    await add_gold(ctx.author.id, 50, ctx)
                elif cpu_points > user_points:
                    await ctx.send(f"```The opponent has reached 9 BP ({cpu_points} BP). Game Over. You gain 0 Gold.```")
                else:
                    await ctx.send(f"```You have reached {user_points} BP, above 9 BP. Enjoy your freedom. You gain 100 Gold.```")
                    await add_gold(ctx.author.id, 100, ctx)
                return

            await ctx.send(welcome_message)

            def check(m):
                return m.channel == ctx.channel and m.author == ctx.author

            message = await self.bot.wait_for("message", check=check, timeout=60.0)

            input_value = message.content
            if input_value == "2":
                await game()
            elif input_value == "1":
                await rules()
            elif input_value.startswith("l!"):
                return
            else:
                await ctx.send("```Invalid input, Exiting Game.```")
                return


welcome_message = """
```Welcome to the AB game, what would you like to do? (Select 1 or 2, any other input will end the game)

1. Read Rules
2. Play Game
```"""


def generate_game_start_message(u_points, c_points):
    game_start_message = f"""
    ```You are now on {u_points} BP while the opponent is on {c_points} BP
        
Please choose to either Ally or Betray.
        
1. Ally
2. Betray
        
Failure to choose an option will automatically Ally.```"""

    return game_start_message


rules_message = f"""```
Rules:

- You start the game with 3 BP (Bracelet Points)
- The main objective of the game is to reach 9 BP before your opponent does.
- To reach 9 BP you need to play a series of games which involve picking one of two choices, Ally or Betray

- If you both pick Ally then you both gain {double_ally_increase} BP
- If someone picked Ally while the other picks Betray then whoever picked Ally loses {being_betrayed_decrease} BP while the person who picked Betray gains {betraying_ally_increase} BP
- If you both pick betray then you both gain {double_betray_increase} BP

- If your BP reaches 0 or below then you will be unable to play and lose the game
- If you pick an option outside of Ally or Betray then it will automatically choose Ally

```"""
