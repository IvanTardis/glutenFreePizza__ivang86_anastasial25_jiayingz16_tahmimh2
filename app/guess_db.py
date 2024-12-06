# GlutenFreePizza: Anastasia, Ivan, Michelle, Tahmim
# P1: ArRESTed Development
# SoftDev
# Dec 2024

import sqlite3

GUESS_FILE = "guesses.db"

def createGuesses():
    guesses = sqlite3.connect(GUESS_FILE)
    c = guesses.cursor()
    command = "CREATE TABLE IF NOT EXISTS guesses (username TEXT, g_total INTEGER, c_num INTEGER, g_avg DECIMAL, c_curr TEXT, hint_num INTEGER)"
    c.execute(command)
    guesses.commit()

def addUserG(username):
    guesses = sqlite3.connect(GUESS_FILE)
    c = guesses.cursor()
    if (c.execute("SELECT 1 FROM guesses WHERE username=?", (username,))).fetchone() == None:
        c.execute("INSERT INTO guesses (username, g_total, c_num, g_avg, c_curr, hint_num) VALUES (?, ?, ?, ?, ?, ?)", (username, 0, 0, 0, "N/A", 0))
        guesses.commit()
        return
    return "Username taken"

def newGame(username, c_curr):
    guesses = sqlite3.connect(GUESS_FILE)
    c = guesses.cursor()
    # c_num++
    c.execute("SELECT c_num FROM users WHERE username = ?", (username,))
    old_c_num = c.fetchone()[0]
    c.execute("UPDATE guesses SET c_num = ? WHERE username = ?", (old_c_num+1, username))
    # hint_num = 1
    c.execute("UPDATE guesses SET hint_num = ? WHERE username = ?", (1, username))
    # c_curr = new current country
    c.execute("UPDATE guesses SET c_curr = ? WHERE username = ?", (c_curr, username))
    guesses.commit()

def finishGame(username):
    newHint(username)
    # update g_avg
    c.execute("SELECT g_total FROM users WHERE username = ?", (username,))
    g_total = c.fetchone()[0]
    c.execute("SELECT c_num FROM users WHERE username = ?", (username,))
    c_num = c.fetchone()[0]
    new_g_avg = g_total/c_num
    c.execute("UPDATE guesses SET g_avg = ? WHERE username = ?", (new_g_avg, username))
    guesses.commit()

def newHint(username):
    guesses = sqlite3.connect(GUESS_FILE)
    c = guesses.cursor()
    # g_total++
    c.execute("SELECT g_total FROM users WHERE username = ?", (username,))
    old_g_total = c.fetchone()[0]
    c.execute("UPDATE guesses SET g_total = ? WHERE username = ?", (old_g_total+1, username))
    # hint_num++
    c.execute("SELECT hint_num FROM users WHERE username = ?", (username,))
    old_hint_num = c.fetchone()[0]
    c.execute("UPDATE guesses SET hint_num = ? WHERE username = ?", (old_hint_num+1, username))
    guesses.commit()

def deleteGuesses():
    guesses = sqlite3.connect(GUESS_FILE) 
    c = guesses.cursor()
    c.execute("DROP table guesses")
