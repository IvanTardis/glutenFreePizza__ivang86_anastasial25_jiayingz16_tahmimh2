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


if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()

# session.pop('username', None)

# close it up
db.close()
