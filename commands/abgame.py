from discord.ext import commands
import random

user_points = 3
cpu_points = 3

double_ally_increase = 2
double_betray_increase = 0
betraying_ally_increase = 3
being_betrayed_decrease = -2


class AbGameCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def abgame(self, ctx):
        await ctx.send(welcome_message)

        async def rules():
            await ctx.send(rules_message)

        async def game():

            global user_points, cpu_points
            cpu_choices = ["Ally", "Betray"]

            while (0 < user_points < 9) and (0 < cpu_points < 9):
                await ctx.send(game_start_message)

                game_message = await self.bot.wait_for("message", check=lambda msg: msg.author == ctx.author, timeout=60.0)

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
            if cpu_points > 9 and user_points > 9:
                await ctx.send(f"```You have both reached 9 BP, Congratulations! You are both free.```")
            elif cpu_points > user_points:
                await ctx.send(f"```The opponent has reached 9 BP ({cpu_points} BP). Game Over.```")
            else:
                await ctx.send(f"```You have reached {user_points}BP You now are 9 BP. Enjoy your freedom.```")

        message = await self.bot.wait_for("message", check=lambda msg: msg.author == ctx.author, timeout=60.0)

        input_value = message.content
        if input_value == "2":
            await game()
        elif input_value == "1":
            await rules()
        else:
            await ctx.send("```Invalid input, type l!abgame to try again.```")


welcome_message = """
```Welcome to the AB game, what would you like to do? (Select 1 or 2, any other input will end the game)

1. Read Rules
2. Play Game```"""

game_start_message = f"""
```You are now on {user_points} BP while the opponent is on {cpu_points} BP
    
Please choose to either Ally or Betray.
    
1. Ally
2. Betray
    
Failure to choose an option will automatically Ally.```"""

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
