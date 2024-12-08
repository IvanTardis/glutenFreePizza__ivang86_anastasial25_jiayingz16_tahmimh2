# GlutenFreePizza: Anastasia, Ivan, Michelle, Tahmim
# P1: ArRESTed Development
# SoftDev
# Dec 2024

from flask import Flask, render_template, request, session, redirect, flash, url_for

import urllib.request
import json
import os
import random
import sqlite3
from user_db import createUsers, addUser, checkLogin, deleteUsers
#from countries import *
#from user_db import *

app = Flask(__name__)    #create Flask object

# makin' a supa-secret key
app.secret_key = os.urandom(32)

createUsers()

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
        
        session['username'] = username
        flash("Login successful", "success")
    return redirect('/home')

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
        
        flash("Registration successful!")
    return redirect('/login')

# USER LOGOUTS
@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.pop('username', None)
    #session.pop('name', None)
    flash("You have been logged out.", "info")
    return redirect("/login")

'''
@app.route('/profile', methods=["GET"])
def profile():
    return render_template('profile.html', username='username')
'''

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()