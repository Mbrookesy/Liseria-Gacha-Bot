import sqlite3


async def check_if_registered(user, ctx):
    conn = sqlite3.connect("gachaDatabase.db")
    try:
        cur = conn.cursor()
        cur.execute(f"""SELECT ID FROM USER WHERE ID = {user};""")
        data = cur.fetchall()
        if not data:
            await ctx.send("User not registered. Please register with the l!register command.")
            return False
        else:
            return True
    except sqlite3.IntegrityError:
        await ctx.send("Unknown Database Error")

    conn.close()


async def add_gold(user, amount, ctx):
    conn = sqlite3.connect("gachaDatabase.db")
    try:
        cur = conn.cursor()
        cur.execute(f"""SELECT GOLD FROM USER WHERE ID = {user};""")
        data = cur.fetchone()
        conn.execute(f"""UPDATE USER SET GOLD = {data[0] + amount} WHERE ID = {user}""")

        conn.commit()
    except sqlite3.IntegrityError:
        await ctx.send("Unknown Database Error")

    conn.close()


async def check_gold(user, ctx):
    conn = sqlite3.connect("gachaDatabase.db")
    try:
        cur = conn.cursor()
        cur.execute(f"""SELECT GOLD FROM USER WHERE ID = {user};""")
        data = cur.fetchone()

        await ctx.send(f"You currently have {data[0]} Gold.")
    except sqlite3.IntegrityError:
        await ctx.send("Unknown Database Error")

    conn.close()

