# GlutenFreePizza: Anastasia, Ivan, Michelle, Tahmim
# P1: ArRESTed Development
# SoftDev
# Dec 2024

import sqlite3

GUESS_FILE = "guesses.db"

# Creates guesses table
def createGuesses():
    guesses = sqlite3.connect(GUESS_FILE)
    c = guesses.cursor()
    command = "CREATE TABLE IF NOT EXISTS guesses (username TEXT, g_total INTEGER, c_num INTEGER, g_avg DECIMAL, c_curr TEXT, hint_num INTEGER, unit TEXT)"
    c.execute(command)
    guesses.commit()

# Adds a new user's info to table
def addUserG(username):
    guesses = sqlite3.connect(GUESS_FILE)
    c = guesses.cursor()
    if (c.execute("SELECT 1 FROM guesses WHERE username=?", (username,))).fetchone() == None:
        c.execute("INSERT INTO guesses (username, g_total, c_num, g_avg, c_curr, hint_num, unit) VALUES (?, ?, ?, ?, ?, ?, ?)", (username, 0, 0, 0, "N/A", 1, "metric"))
        guesses.commit()
        return
    return "Username taken"

# Sets up stats for a new game for a given user
def newGame(username, c_curr):
    guesses = sqlite3.connect(GUESS_FILE)
    c = guesses.cursor()
    # hint_num = 1
    c.execute("UPDATE guesses SET hint_num = ? WHERE username = ?", (1, username))
    # c_curr = new current country
    c.execute("UPDATE guesses SET c_curr = ? WHERE username = ?", (c_curr, username))
    guesses.commit()

# Cleans up user info when they finish a game, updating statistics accordingly
def finishGame(username):
    guesses = sqlite3.connect(GUESS_FILE)
    c = guesses.cursor()
    newHint(username)
    # c_num++
    c.execute("SELECT c_num FROM guesses WHERE username = ?", (username,))
    old_c_num = c.fetchone()[0]
    c.execute("UPDATE guesses SET c_num = ? WHERE username = ?", (old_c_num+1, username))
    # update g_avg
    c.execute("SELECT g_total FROM guesses WHERE username = ?", (username,))
    g_total = c.fetchone()[0]
    c.execute("SELECT c_num FROM guesses WHERE username = ?", (username,))
    c_num = c.fetchone()[0]
    new_g_avg = g_total/c_num
    c.execute("UPDATE guesses SET g_avg = ? WHERE username = ?", (new_g_avg, username))
    c.execute("UPDATE guesses SET c_curr = ? WHERE username = ?", ("N/A", username))
    c.execute("UPDATE guesses SET hint_num = ? WHERE username = ?", (1, username))
    guesses.commit()

# Sets user info to values given for a new hint
def newHint(username):
    guesses = sqlite3.connect(GUESS_FILE)
    c = guesses.cursor()
    # g_total++
    c.execute("SELECT g_total FROM guesses WHERE username = ?", (username,))
    old_g_total = c.fetchone()[0]
    c.execute("UPDATE guesses SET g_total = ? WHERE username = ?", (old_g_total+1, username))
    # hint_num++
    c.execute("SELECT hint_num FROM guesses WHERE username = ?", (username,))
    old_hint_num = c.fetchone()[0]
    c.execute("UPDATE guesses SET hint_num = ? WHERE username = ?", (old_hint_num+1, username))
    guesses.commit()

# Triggered if user tries to "quit" or restart their game. Similar to finishGame
def restartGame(username):
    guesses = sqlite3.connect(GUESS_FILE)
    c = guesses.cursor()
    # get hint_num
    c.execute("SELECT hint_num FROM guesses WHERE username = ?", (username,))
    hint_num = c.fetchone()[0]
    # g_total+=7
    c.execute("SELECT g_total FROM guesses WHERE username = ?", (username,))
    old_g_total = c.fetchone()[0]
    c.execute("UPDATE guesses SET g_total = ? WHERE username = ?", (old_g_total+8-hint_num, username))
    # c_num++
    c.execute("SELECT c_num FROM guesses WHERE username = ?", (username,))
    old_c_num = c.fetchone()[0]
    c.execute("UPDATE guesses SET c_num = ? WHERE username = ?", (old_c_num+1, username))
    # update g_avg
    c.execute("SELECT g_total FROM guesses WHERE username = ?", (username,))
    g_total = c.fetchone()[0]
    c.execute("SELECT c_num FROM guesses WHERE username = ?", (username,))
    c_num = c.fetchone()[0]
    new_g_avg = g_total/c_num
    c.execute("UPDATE guesses SET g_avg = ? WHERE username = ?", (new_g_avg, username))
    c.execute("UPDATE guesses SET c_curr = ? WHERE username = ?", ("N/A", username))
    c.execute("UPDATE guesses SET hint_num = ? WHERE username = ?", (1, username))
    guesses.commit()

# Loads user info for profile
def profileArr(username):
    guesses = sqlite3.connect(GUESS_FILE)
    c = guesses.cursor()
    c.execute("SELECT * FROM guesses WHERE username = ?", (username,))
    arr = c.fetchone()
    return arr

# Loads top 10 user stats for leaderboard
def top10():
    guesses = sqlite3.connect(GUESS_FILE)
    c = guesses.cursor()
    c.execute("SELECT g_avg, username FROM guesses WHERE g_avg > 0")
    arr = c.fetchall()
    top10 = sorted(arr)[:10]
    return top10

# Update's users' unit preferences
def updateUnits(username, units):
    guesses = sqlite3.connect(GUESS_FILE)
    c = guesses.cursor()
    c.execute("UPDATE guesses SET unit = ? WHERE username = ?", (units, username))
    guesses.commit()

# Returns what units the user prefers
def getUnits(username):
    guesses = sqlite3.connect(GUESS_FILE)
    c = guesses.cursor()
    c.execute("SELECT unit FROM guesses WHERE username = ?", (username,) )
    curr_units = c.fetchone()
    return curr_units[0]

# Delete guesses table
def deleteGuesses():
    guesses = sqlite3.connect(GUESS_FILE)
    c = guesses.cursor()
    c = guesses.cursor()
    c.execute("DROP table guesses")

# Returns the current country the user is guessing
def getcurrCountry(username):
    guesses = sqlite3.connect(GUESS_FILE)
    c = guesses.cursor()
    c.execute("SELECT c_curr FROM guesses WHERE username = ?", (username,) )
    current_country = c.fetchone()
    return current_country[0]

# Returns the number hint the user is on
def numHints(username):
    guesses = sqlite3.connect(GUESS_FILE)
    c = guesses.cursor()
    c.execute("SELECT hint_num FROM guesses WHERE username = ?", (username,) )
    numhints = c.fetchone()
    return numhints[0]
