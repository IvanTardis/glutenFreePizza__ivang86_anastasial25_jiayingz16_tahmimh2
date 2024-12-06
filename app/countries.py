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
    a = f"https://restcountries.com/v3.1/alpha/{x}"
    b = urllib.request.urlopen(a)
    c = b.read()
    d = json.loads(c)

    lst = []
    i=0
    for l in d[0]['languages']:
        for x in l:
            lst.append(x)
        # print("HELLO " + lst + "\n")
        i+=1

    info = {
        'name': d[0]['name']['common'],
        'unMember': d[0]['unMember'],
        'currency': (d[0]['currencies']['TMT']['name'], d['currencies']['symbol']),
        'capital': d[0]['capital'],
        'region': d[0]['region'],
        'subregion': d[0]['subregion'],
        'languages': d[0]['languages']
    }
    pprint.pp(info)


x = randomCountry()
getCountryInfo(x)
