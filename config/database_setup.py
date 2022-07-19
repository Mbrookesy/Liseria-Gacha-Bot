import sqlite3
import csv


def database_setup():
    try:
        conn = sqlite3.connect("gachaDatabase.db")
        cursor = conn.cursor()

        with open("config/ocs.csv", mode="r") as file:
            data = csv.reader(file)

            print("Opened database successfully")

            conn.execute("""CREATE TABLE IF NOT EXISTS USER
            (ID INT PRIMARY KEY NOT NULL,
            GOLD INT            NOT NULL);
            """)

            conn.execute("""CREATE TABLE IF NOT EXISTS OCS
            (ID         INT PRIMARY KEY NOT NULL,
            NAME        VARCHAR(255)    NOT NULL,
            PRICE       INT             NOT NULL,
            RARITY      INT             NOT NULL,
            DESCRIPTION VARCHAR(255));
            """)

            cursor.execute(f"""SELECT ID FROM OCS WHERE ID = 1;""")
            first_cell = cursor.fetchall()

            if not first_cell:
                insert_oc_query = """
                INSERT INTO OCS (id, name, price, rarity, description)
                VALUES (?, ?, ?, ?, ?);"""

                print("Inserted oc data into database")

                cursor.executemany(insert_oc_query, data)
                conn.commit()

            cursor.close()
            conn.close()
    #Todo: Make error handling more specific
    except:
        print("Unknown Database Error")



