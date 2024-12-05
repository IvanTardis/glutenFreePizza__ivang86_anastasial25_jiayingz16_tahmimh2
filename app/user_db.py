# GlutenFreePizza: Anastasia, Ivan, Michelle, Tahmim
# P1: ArRESTed Development
# SoftDev
# Dec 2024

import sqlite3

USER_FILE = "users.db"

def createUsers():
    users = sqlite3.connect(USER_FILE)
    c = users.cursor()
    command = "CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)"
    c.execute(command)
    users.commit()

def addUser(username, password):
    users = sqlite3.connect(USER_FILE)
    c = users.cursor()
    if (c.execute("SELECT 1 FROM users WHERE username=?", (username,))).fetchone() == None:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        users.commit()
        return
    return "Username taken"

def checkLogin(username, password):
    users = sqlite3.connect(USER_FILE)
    c = users.cursor()
    if (c.execute("SELECT 1 FROM users WHERE username=?", (username,))).fetchone() == None:
        return "Username does not exist; please register before logging in."
    c.execute("SELECT password FROM users WHERE username=?", (username,))
    res = c.fetchone()
    if (password == res[0]):
        return
    return "Invalid login; please try again."

def deleteUsers():
    db = sqlite3.connect(USER_FILE) 
    c = db.cursor()
    c.execute("DROP table users")
