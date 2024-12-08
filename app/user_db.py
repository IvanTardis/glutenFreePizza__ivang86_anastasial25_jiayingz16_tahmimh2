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
    # Check if the username already exists
    if c.execute("SELECT 1 FROM users WHERE username=?", (username,)).fetchone() is None:
        # Insert the new user
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        users.commit()
        return None  # Registration successful
    return "Username already exists"  # Registration failed

def checkLogin(username, password):
    users = sqlite3.connect(USER_FILE)
    c = users.cursor()
    # Check if the username exists
    if c.execute("SELECT 1 FROM users WHERE username=?", (username,)).fetchone() is None:
        return "Username does not exist; please register below before logging in."
    # Check if the password matches
    c.execute("SELECT password FROM users WHERE username=?", (username,))
    res = c.fetchone()
    if password == res[0]:
        return None  # Login successful
    return "Invalid login; please try again."  # Login failed

def deleteUsers():
    db = sqlite3.connect(USER_FILE) 
    c = db.cursor()
    c.execute("DROP table users")