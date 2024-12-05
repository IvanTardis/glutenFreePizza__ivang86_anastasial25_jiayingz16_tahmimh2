# GlutenFreePizza: Anastasia, Ivan, Michelle, Tahmim
# P1: ArRESTed Development
# SoftDev
# Dec 2024

from flask import Flask, render_template, request, session, redirect, flash, url_for

import urllib.request
import pprint
import json
import os
from user_db import *

app = Flask(__name__)    #create Flask object

# makin' a supa-secret key
app.secret_key = os.urandom(32)

createUsers()

restCountriesLink = "https://restcountries.com/v3.1/independent?fields=name"
restCountriesURL = urllib.request.urlopen(restCountriesLink)
reader = restCountriesURL.read()
countryDict = json.loads(reader)

cleanerDict = {}
i = 0
for country in countryDict:
    # print(country)
    cleanerDict[i] = country['name']['common']
    i+=1

# pprint.pp(cleanerDict)

@app.route(("/"), methods=['GET', 'POST'])
def home():
    if 'username' in session:
        return render_template("home.html", user = session['username'])
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
        if not (username and password):
            flash("One or more fields empty", 'error')
            return redirect('/login')
        message = checkLogin(username, password)
        if message:
            flash(message, 'error')
            return redirect('/login')
        session['username'] = username
        session['name'] = username
        return redirect('/')
    return redirect('/login')


# USER REGISTRATIONS
@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template("register.html")

@app.route('/auth_reg', methods=["GET", "POST"])
def auth_reg():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if not (username and password):
            flash("One or more fields empty", 'error')
            return redirect('/register')
        message = addUser(username, password)
        if message:
            flash(message, 'error')
            return redirect('/register')
        session['username'] = username
        session['password'] = password
        return redirect('/')
    return redirect('/register')


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
