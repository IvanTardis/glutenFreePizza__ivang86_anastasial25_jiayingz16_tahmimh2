'''
Gluten Free Pizza - Tawab Berri, Ivan Gontchar, Nia Lam, Alex Luo
SoftDev
2024-12-04
p01 - ArRESTed Development - Globle
time spent:
'''
from flask import Flask, render_template, request, session, redirect, url_for

import urllib.request
import pprint
import json
import sqlite3
import os

app = Flask(__name__)    #create Flask object
DB_FILE = "database.db" #create a database for private keys storage

# makin' a supa-secret key
app.secret_key = os.urandom(32)

db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
c = db.cursor()  #facilitate db ops -- you will use cursor to trigger db events

@app.route(("/"), methods=['GET', 'POST'])
def home():
    if 'username' in session:
        return render_template("home.html", user = session['username'])
    else:
        return redirect("/login")


# USER LOGIN
@app.route('/login', methods=['GET','POST'])
def login():
    return render_template("login.html")

@app.route('/auth_login', methods=["GET", "POST"])
def auth_login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        app.secret_key = os.urandom(32)
        if dbx.verify_user(username, password):
            session['username'] = username
            session['name'] = username
            return redirect('/')
        else:
            flash("Incorrect username or password.", 'error')
            return redirect("/login")


# USER REGISTRATIONS
@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template("register.html")

@app.route('/auth_reg', methods=["GET", "POST"])
def auth_reg():
    if request.method == "POST":
        new_username = request.form['new_user']
        new_password = request.form['new_pass']
        elif new_password != request.form['confirm_pass']:
            flash("Passwords do not match.", 'error')
            return render_template("register.html")
        else:
            try:
                dbx.create_user(new_username, new_password)
                flash("You are now registered! Please log in.", 'success')
                return render_template("login.html")
            except sqlite3.IntegrityError:
                flash("Username already exists.", 'error')
                return render_template("register.html")


# USER LOGOUTS
@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.pop('username', None)
    session.pop('name', None)
    return redirect("/")


if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()

# session.pop('username', None)

# close it up
db.close()
