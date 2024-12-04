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
        c.execute("INSERT INTO users (username, password, viewable) VALUES (?, ?, ?)", (username, password, "1"))
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
    if (password != res[0]):
        return "Invalid login; please try again."
    return

def newStory(username, id):
    users = sqlite3.connect(USER_FILE)
    c = users.cursor()
    c.execute("SELECT viewable FROM users WHERE username = ?", (username,))
    viewable = c.fetchone()[0]
    if viewable:
        newV = f"{viewable},{id}"
    else:
        newV = str(id)
    c.execute("UPDATE users SET viewable = ? WHERE username = ?", (newV, username))
    users.commit()

def makeViewList(username):
    users = sqlite3.connect(USER_FILE)
    c = users.cursor()
    c.execute("SELECT viewable FROM users WHERE username = ?", (username,))
    viewable = c.fetchone()[0]
    if not viewable:
        return
    id_list = str(viewable).split(',')
    viewList = []
    for id in id_list:
        list = [id, returnStoryTitle(id), returnChapters(id), returnAuthor(id)]
        viewList.append(list)
    return viewList

def makeEditList(username):
    users = sqlite3.connect(USER_FILE)
    c = users.cursor()
    c.execute("SELECT viewable FROM users WHERE username = ?", (username,))
    viewable = c.fetchone()[0]
    storydb = sqlite3.connect("stories.db")
    cStory = storydb.cursor()
    cStory.execute("SELECT story_id FROM stories")
    allStories = []
    for tuple in cStory.fetchall():
        allStories.append(int(str(tuple)[1:-2]))
    editable = []
    for id in allStories:
        if str(id) not in str(viewable).split(","):
            editable.append(id)
    if not editable:
        return
    editList = []
    for id in editable:
        list = [id, returnStoryTitle(id), returnChapters(id), returnAuthor(id)]
        editList.append(list)
    c.execute("UPDATE users SET editable = ? WHERE username = ?", (','.join(str(h) for h in editList), username))
    users.commit()
    return editList

def editStory(id, content, username):
    users = sqlite3.connect(USER_FILE)
    c = users.cursor()
    addChapter(id, content, username)
    c.execute("SELECT editable FROM users WHERE username = ?", (username,))
    editStr = c.fetchone()[0]
    print(editStr)
    editList = editStr.split(',')

    if (id in editList):
        editList.remove(id)
        updList = ','.join(str(h) for h in editList)
        c.execute("UPDATE users SET editable = ? WHERE username = ?", (updList, username))

    c.execute("SELECT viewable FROM users WHERE username = ?", (username,))
    view = c.fetchone()[0]
    if view:
        nview = f"{view},{id}"
    else:
        nview = str(id)
        
    c.execute("UPDATE users SET viewable = ? WHERE username = ?", (nview, username))
    users.commit()

def deleteUsers():
    db = sqlite3.connect(USER_FILE) 
    c = db.cursor()
    c.execute("DROP table users")
