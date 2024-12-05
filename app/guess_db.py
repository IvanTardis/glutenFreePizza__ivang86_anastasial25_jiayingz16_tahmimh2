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

'''
def newGame(username, c_curr):
    guesses = sqlite3.connect(GUESS_FILE)
    c = guesses.cursor()
    c.execute("UPDATE guesses SET g_total = ? WHERE username = ?", (, username))
    c.execute("UPDATE guesses SET c_curr = ? WHERE username = ?", (c_curr, username))

newHint(username)
hint_num++
'''

def deleteGuesses():
    guesses = sqlite3.connect(GUESS_FILE) 
    c = guesses.cursor()
    c.execute("DROP table guesses")
