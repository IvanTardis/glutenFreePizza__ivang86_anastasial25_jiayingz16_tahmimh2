# GlutenFreePizza: Anastasia, Ivan, Michelle, Tahmim
# P1: ArRESTed Development
# SoftDev
# Dec 2024

from flask import Flask, render_template, request, session, redirect, flash, url_for

import urllib.request
import pprint
import json
import os
import random
from user_db import *


# Load in a Dict of Countries
restCountriesLink = "https://restcountries.com/v3.1/independent?fields=name,cca2"
restCountriesURL = urllib.request.urlopen(restCountriesLink)
readCountries = restCountriesURL.read()
countryDict = json.loads(readCountries)

cleanerDict = {}
i = 0
for country in countryDict:
    # print(country)
    cleanerDict[i] = country['name']['common'], country['cca2']
    i+=1
# pprint.pp(cleanerDict)


# Returns the 2 letter code of a random country from our dict
def randomCountry():
    x = random.randint(0,193)
    code = cleanerDict[x][1]
    return code

def getCountryInfo(x):
