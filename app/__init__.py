# GlutenFreePizza: Anastasia, Ivan, Michelle, Tahmim
# P1: ArRESTed Development
# SoftDev
# Dec 2024

import urllib.request
import json
import os
import random
import sqlite3
from flask import Flask, render_template, request, session, redirect, flash, url_for
from countries import *
from user_db import *
from guess_db import *
from countries import *

app = Flask(__name__)    #create Flask object

# makin' a supa-secret key
app.secret_key = os.urandom(32)

#getHints()
createUsers()
createGuesses()

# GETTING A RANDOM FLAG URL
# x = randomCountry()
# print(x)
# getCountryInfo(x)

# restFlagsLink = f"https://flagsapi.com/{code}/flat/64.png"
# print(restFlagsLink)

# GETTING SOME WEATHER DATA ON IT
# a = f"https://restcountries.com/v3.1/alpha/{code}"
# b = urllib.request.urlopen(a)
# c = b.read()
# d = json.loads(c)
# # pprint.pp(d)
#
# lat = d['capitalInfo']['latlng'][0]
# lon = d['capitalInfo']['latlng'][1]
# file = open("key_openWeatherMap.txt")
# weatherKey = file.readline()
# restWeatherLink = f"https://pro.openweathermap.org/data/2.5/forecast/climate?lat={lat}&lon={lon}&appid={weatherKey}"
# restWeatherURL = urllib.request.urlopen(restWeatherLink)
# readWeather = restWeatherURL.read()
# weatherDict = json.loads(readWeather)
# pprint.pp(weatherDict)

@app.route("/", methods=['GET', 'POST'])
def home():
    if 'username' in session:
        return render_template("home.html")
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

        if not (username and password):
            flash("One or more fields empty", 'danger')
            return redirect('/login')

        message = checkLogin(username, password)
        if message:
            flash(message, 'danger')
            return redirect('/login')

        else:
            session['username'] = username
            addUserG(session['username'])
            return redirect('/')

    return redirect('/')

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
            flash("One or more fields empty", 'danger')
            return redirect('/register')

        message = addUser(username, password)
        if message:
            flash(message, "danger")
            return redirect("/register")

        flash("Registration successful!", 'success')
        return redirect('/login')
    return redirect('/login')

# USER LOGOUTS
@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.clear()
    flash("Logged out successfully", 'info')
    return redirect("/login")

@app.route('/description', methods=["GET"])
def description():
    return render_template('description.html')

@app.route('/game', methods=["GET", "POST"])
def game():
    if 'username' in session:
        username = session['username']
    else:
        return redirect('/login')
    country = getcurrCountry(username)
    hintnum = numHints(username)

    if country == "N/A":
        hints = getHints("")
        country = hints[6][1]
        newGame(username, country)
    else:
        hints = getHints(country)
    newguess = request.form['guess']
    if newguess.lower() == country.lower():
        finishGame(username)
    else:
        newHint(username)
    return render_template('game.html', hints, hintnum)

@app.route('/leaderboard', methods=["GET"])
def leaderboard():
    return render_template('leaderboard.html')

@app.route('/profile', methods=["GET"])
def profile():
    if 'username' in session:
        username = session['username']
        print(profileArr(username))
        return render_template('profile.html', username = username)
    return render_template('profile.html', username = "login to see profile") #temporary

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
