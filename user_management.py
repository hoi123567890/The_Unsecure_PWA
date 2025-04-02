import sqlite3 as sql
import time
import random
from werkzeug.security import generate_password_hash, check_password_hash

def insertUser(username, pa, DoB):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    password=generate_password_hash(pa)
    cur.execute(
        "INSERT INTO users (username,password,dateOfBirth) VALUES (?,?,?)",
        (username, password, DoB),
    )
    con.commit()
    con.close()


def retrieveUsers(username, password):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cur.fetchone()
    if result is None:
        con.close()
        return False  # User not found
    else:
        hashed_password = result[0]
        if check_password_hash(hashed_password, password):
            # Plain text log of visitor count as requested by Unsecure PWA management
            try:
                with open("visitor_log.txt", "r+") as file:
                    content = file.read().strip()
                    number = int(content) if content else 0
                    number += 1
                    file.seek(0)
                    file.write(str(number))
                    file.truncate()
            except FileNotFoundError:
                with open("visitor_log.txt", "w") as file:
                    file.write("1")
            except ValueError:
                print("Warning: Invalid content in visitor_log.txt. Resetting to 1.")
                with open("visitor_log.txt", "w") as file:
                    file.write("1")
            # Simulate response time of heavy app for testing purposes
            time.sleep(random.randint(80, 90) / 1000)
            con.close()
            return True  # Authentication successful
        else:
            con.close()
            return False # Incorrect password


def insertFeedback(feedback):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute(f"INSERT INTO feedback (feedback) VALUES ('{feedback}')")
    con.commit()
    con.close()


def listFeedback():
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    data = cur.execute("SELECT * FROM feedback").fetchall()
    con.close()
    f = open("templates/partials/success_feedback.html", "w")
    for row in data:
        f.write("<p>\n")
        f.write(f"{row[1]}\n")
        f.write("</p>\n")
    f.close()
