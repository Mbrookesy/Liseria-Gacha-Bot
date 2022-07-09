import sqlite3


def database_setup():
    conn = sqlite3.connect("gachaDatabase.db")
    print("Opened database successfully")

    conn.execute("""CREATE TABLE IF NOT EXISTS USER
    (ID INT PRIMARY KEY NOT NULL,
    GOLD INT            NOT NULL);
    """)

    conn.close()
