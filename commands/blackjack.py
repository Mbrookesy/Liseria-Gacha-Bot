from discord.ext import commands
from config.database_service import *
import random
import sqlite3

class Deck:
    def __init__(self, hand, value, value_with_max_aces, contains_aces):
        self._hand = hand
        self._value = value
        self._valueWithMaxAces = value_with_max_aces
        self._containsAces = contains_aces

    def getHand(self):
        return self._hand

    def getValue(self):
        return self._value

    def getValueWithMaxAces(self):
        return self._valueWithMaxAces

    def getContainsAces(self):
        return self._containsAces

    def addCard(self, card):
        self._hand.append(card)

    def addValue(self, value, new_ace):
        self._value = self._value + value
        if not new_ace:
            self._valueWithMaxAces = self._valueWithMaxAces + value
        else:
            self._valueWithMaxAces = self._valueWithMaxAces + 11

    def getFormattedHand(self):
        return ", ".join(self._hand)

    def aceAdded(self):
        self._containsAces = True

#To Do - Make a better interface for this (Buttons?)
class BlackjackCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def blackjack(self, ctx):
        if await check_if_registered(ctx.author.id, ctx):

            card_suits = ["Hearts", "Clubs", "Diamonds", "Spades"]
            card_values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

            player_hand = Deck([], 0, 0, False)
            cpu_hand = Deck([], 0, 0, False)

            async def grab_card(hand, user="You"):
                random_suit = random.choice(card_suits)
                random_value = random.choice(card_values)
                new_ace = False

                if random_value == "J":
                    true_value = 10
                    value_name = "Jack"
                elif random_value == "Q":
                    true_value = 10
                    value_name = "Queen"
                elif random_value == "K":
                    true_value = 10
                    value_name = "King"
                elif random_value == "A":
                    true_value = 1
                    value_name = "Ace"
                    new_ace = True
                    hand.aceAdded()
                else:
                    true_value = int(random_value)
                    value_name = random_value

                hand.addValue(true_value, new_ace)
                hand.addCard(f"{random_value}-{random_suit}")

                await ctx.send(f"```{user} drew the {value_name} of {random_suit}```")

            async def announce_hands(p_hand=player_hand, c_hand=cpu_hand):
                if player_hand.getContainsAces():
                    await ctx.send("```The value of your hand is " + str(p_hand.getValue()) + " or " + str(
                        p_hand.getValueWithMaxAces()) + " (With Aces at 11)```")
                else:
                    await ctx.send("```The value of your hand is " + str(p_hand.getValue()) + "```")
                await ctx.send("```Your hand is currently: " + p_hand.getFormattedHand() + "```")
                await ctx.send("```The dealer's hand is currently: " + c_hand.getFormattedHand() + "```")

            async def dealer_play(c_hand=cpu_hand):
                await ctx.send(f"```Dealer's hand is {c_hand.getFormattedHand()}```")
                while cpu_hand.getValueWithMaxAces() < 17:
                    await grab_card(cpu_hand, "Dealer")

                if cpu_hand.getValueWithMaxAces() <= 21:
                    return cpu_hand.getValueWithMaxAces()
                elif cpu_hand.getValue() <= 21:
                    return cpu_hand.getValue()
                else:
                    return 0

            stand_status = False
            started = True
            folded = False

            while not stand_status and not folded:

                if started:
                    await ctx.send("```The game of blackjack has started```")
                    await ctx.send("```You draw two cards.```")

                    await grab_card(cpu_hand, "Dealer")
                    await grab_card(player_hand)
                    await grab_card(player_hand)
                    await announce_hands()

                    started = False
                else:
                    await ctx.send("```You draw a card```")

                    await grab_card(player_hand)
                    await announce_hands()

                if player_hand.getValue() > 21:
                    folded = True
                else:
                    await ctx.send("```Would you like to hit or stand? (h/s)```")

                    def check(m):
                        return m.channel == ctx.channel and m.author == ctx.author

                    message = await self.bot.wait_for("message", check=check, timeout=60.0)
                    input_value = message.content.lower()

                    if input_value == "stand" or input_value == "s":
                        stand_status = True
                    elif input_value.startswith("l!"):
                        return
                    elif input_value != "hit" and input_value != "h":
                        await ctx.send("```Invalid input, Exiting Game.```")
                        return
                    else:
                        await ctx.send("```You hit.```")

            if folded:
                await ctx.send("```You have gone over 21, Game Over```")
            else:
                await ctx.send("```You stand.```")
                if player_hand.getValueWithMaxAces() < 21:
                    max_value = player_hand.getValueWithMaxAces()
                else:
                    max_value = player_hand.getValue()
                await ctx.send(f"```Your current value is {max_value}```")
                dealer_value = await dealer_play()

                if dealer_value > max_value:
                    await ctx.send(f"```The dealer has a value of {dealer_value}, higher than your value of {max_value} You Lose. You gain 0 Gold.```")
                elif dealer_value < max_value:
                    await ctx.send(f"```The dealer has a value of {dealer_value}, lower than your value of {max_value} You Win 50 Gold!```")
                    await add_gold(ctx.author.id, 50, ctx)
                else:
                    await ctx.send(f"```You both got the same value, you draw. You gain 5 Gold.```")
                    await add_gold(ctx.author.id, 5, ctx)