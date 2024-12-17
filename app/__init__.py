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
createUsers() #creates Users database   
createGuesses() #creates Guesses database

# Home Route
@app.route("/", methods=['GET', 'POST'])
def home():
    """Redirects to the home page if logged in, otherwise redirects to login page."""
    if 'username' in session:
        return render_template("home.html")  # Renders home page
    else:
        return redirect("/login")  # Redirect to login if not logged in


# USER LOGIN
@app.route('/login', methods=['GET','POST'])
def login():
    """Renders login page"""
    return render_template("login.html")

@app.route('/auth_login', methods=["GET", "POST"])
def auth_login():
    """Authenticates the login"""
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # Check for empty fields
        if not (username and password):
            flash("One or more fields empty", 'danger')
            return redirect('/login')

        # Validate login
        message = checkLogin(username, password)
        if message:
            flash(message, 'danger')  # Show error message
            return redirect('/login')
        else:
            session['username'] = username  # Set session for logged-in user
            addUserG(session['username'])  # Add user to game state
            return redirect('/')  # Redirect to home page

    return redirect('/')

# USER REGISTRATIONS
@app.route('/register', methods=['GET', 'POST'])
def register():
    """Renders the registration page."""
    return render_template("register.html")

@app.route('/auth_reg', methods=["GET", "POST"])
def auth_reg():
    """Handles new user registration."""
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # Check for empty fields
        if not (username and password):
            flash("One or more fields empty", 'danger')
            return redirect('/register')

        # Add user to database
        message = addUser(username, password)
        if message:
            flash(message, "danger")  # Show error if registration fails
            return redirect("/register")

        flash("Registration successful!", 'success')  # Success message
        return redirect('/login')  # Redirect to login
    return redirect('/login')

# USER LOGOUTS
@app.route('/logout', methods=["GET", "POST"])
def logout():
    """Logs out the user by clearing the session."""
    session.clear() #clears session
    flash("Logged out successfully", 'info')
    return redirect("/login")

#GAME FUNCTIONALITY
@app.route('/description', methods=["GET"])
def description():
    """Renders the game description page."""
    return render_template('description.html')

@app.route('/game', methods=["GET", "POST"])
def game():
    """Handles the main game logic."""
    if 'username' in session:
        username = session['username']
    else:
        return redirect('/login')  # Redirect to login if not logged in

    inProgress = True
    country = getcurrCountry(username)  # Get current country for the user
    hintnum = numHints(username)  # Retrieve the number of hints used

    # Start a new game if no current country
    if country == "N/A":
        hints = getHints("")
        country = hints[6][1]
        newGame(username, country)  # Initialize new game
    else:
        hints = getHints(country)

    guess_result = None

    # Check user's guess
    if request.method == 'POST':
        newguess = request.form['guess']

        if newguess.lower() == country.lower():
            # Player guessed correctly
            if hintnum > 1:
                winMSG = "Congratulations! You guessed " + country + " correctly after " + str(hintnum) + " hints."
            else:
                winMSG = "Congratulations! You guessed " + country + " correctly after " + str(hintnum) + " hint."
            flash(winMSG, 'success')
            finishGame(username)
            inProgress = False
        else:
            guess_result = "incorrect"
            newHint(username)  # Provide a new hint
            hintnum = numHints(username)

    # If max hints(7) reached, game over
    if hintnum >= 7:
        flash("You failed to guess the country correctly.", 'danger')
        restartGame(username)
        inProgress = False

    sender = hints[:hintnum]  # Collect hints to display
    sender.reverse()
    countryLst = sorted(nameLst())  # List of countries for guessing

    if inProgress:
        return render_template('game.html', hints=sender, guess_result=guess_result, countries=countryLst)
    else:
        return render_template('gameDone.html', hints=sender)

@app.route('/restart', methods=["POST"])
def restart():
    """Restarts the current game."""
    if 'username' in session:
        username = session['username']
        restartGame(username) #Restarting game is same as getting max hints (7)
        flash("Game restarted!", 'info')
        return redirect('/game')
    else:
        flash("You must log in to restart the game.", 'danger')
        return redirect('/login')

@app.route('/leaderboard', methods=["GET"])
def leaderboard():
    """Displays the top players' leaderboard."""
    num = []
    for i in range(len(top10())):
        num.append(i)
    return render_template('leaderboard.html', arr=top10(), num=num)

@app.route('/profile', methods=["GET", "POST"])
def profile():
    """Handles user profile page."""
    if 'username' in session:
        username = session['username']
        if request.method == 'POST':
            units = request.form['units']
            updateUnits(username, units)  # Update user settings
        return render_template('profile.html', arr=profileArr(username))
    return render_template('profile.html', message="Log in to see profile")

# RUN FLASK APP
if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
