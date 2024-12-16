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
        c.execute("INSERT INTO guesses (username, g_total, c_num, g_avg, c_curr, hint_num) VALUES (?, ?, ?, ?, ?, ?)", (username, 0, 0, 0, "N/A", 1))
        guesses.commit()
        return
    return "Username taken"

def newGame(username, c_curr):
    guesses = sqlite3.connect(GUESS_FILE)
    c = guesses.cursor()
    # hint_num = 1
    c.execute("UPDATE guesses SET hint_num = ? WHERE username = ?", (1, username))
    # c_curr = new current country
    c.execute("UPDATE guesses SET c_curr = ? WHERE username = ?", (c_curr, username))
    guesses.commit()

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

def restartGame(username):
    guesses = sqlite3.connect(GUESS_FILE)
    c = guesses.cursor()
    # g_total+=7
    c.execute("SELECT g_total FROM guesses WHERE username = ?", (username,))
    old_g_total = c.fetchone()[0]
    c.execute("UPDATE guesses SET g_total = ? WHERE username = ?", (old_g_total+7, username))
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
    

def profileArr(username):
    guesses = sqlite3.connect(GUESS_FILE)
    c = guesses.cursor()
    c.execute("SELECT * FROM guesses WHERE username = ?", (username,))
    arr = c.fetchone()
    return arr

def top10():
    guesses = sqlite3.connect(GUESS_FILE)
    c = guesses.cursor()
    c.execute("SELECT g_avg, username FROM guesses WHERE g_avg > 0")
    arr = c.fetchall()
    top10 = sorted(arr)[:10]
    return top10

def deleteGuesses():
    guesses = sqlite3.connect(GUESS_FILE)
    c = guesses.cursor()
    c = guesses.cursor()
    c.execute("DROP table guesses")

def getcurrCountry(username):
    guesses = sqlite3.connect(GUESS_FILE)
    c = guesses.cursor()
    c.execute("SELECT c_curr FROM guesses WHERE username = ?", (username,) )
    current_country = c.fetchone()
    return current_country[0]

def numHints(username):
    guesses = sqlite3.connect(GUESS_FILE)
    c = guesses.cursor()
    c.execute("SELECT hint_num FROM guesses WHERE username = ?", (username,) )
    numhints = c.fetchone()
    return numhints[0]
