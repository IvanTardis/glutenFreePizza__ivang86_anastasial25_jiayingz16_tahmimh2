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

    # There was an issue with Python crashing because of the symbol of the currency breaking it, i suspect this is not unique to Turkey, so maybe we will get to that
    # a = f"https://restcountries.com/v3.1/alpha/TR"

    # print(a)
    b = urllib.request.urlopen(a)
    c = b.read()
    d = json.loads(c)

    langLst = []
    for l in d[0]['languages']:
        # for x in d[0]['languages'][l]:
        langLst.append(d[0]['languages'][l])
        # print("HELLO " + lst + "\n")
    # print(langLst)

    currencyLst = []
    for i in d[0]['currencies']:
        # for x in d[0]['currencies'][i]:
        currencyLst.append(d[0]['currencies'][i]['name'])
    # print(currencyLst)

    coords = []
    for i in d[0]['capitalInfo']['latlng']:
        # print(i)
        # coords.append(d[0]['latlng'][i])
        coords.append(i)

    bordering = []
    if 'borders' in d[0]:
        for i in d[0]['borders']:
            # print(i)
            bordering.append(i)

    info = {
        'name': [d[0]['name']['common'], x],
        'unMember': d[0]['unMember'],
        'currency': currencyLst,
        'capital': d[0]['capital'],
        'region': d[0]['region'],
        'subregion': d[0]['subregion'],
        'languages': langLst,
        'LatLong': coords,
        'landlocked': d[0]['landlocked'],
        'borderingCountries': bordering,
        'area': d[0]['area'],
        'population': d[0]['population'],
        'continents': d[0]['continents'],
        'coatOfArms': d[0]['coatOfArms']['png']
    }
    # pprint.pp(info)
    return info

def getWeather(lat, long):
    try:
        file = open("keys/key_openWeatherMap.txt")
    except:
        print("Key File Not Found")
    else:
        weatherKey = file.readline()
        restWeatherLink = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&appid={weatherKey}"
        # print(restWeatherLink)
        try:
            restWeatherURL = urllib.request.urlopen(restWeatherLink)
        except:
            print("Weather API key not found")
        else:
            readWeather = restWeatherURL.read()
            weatherDict = json.loads(readWeather)
            # pprint.pp(weatherDict)
    return weatherDict

def getRandomHints():
    dict = getCountryInfo(randomCountry())
    weatherInfo = getWeather(dict['LatLong'][0],dict['LatLong'][1])
    return 0

# x = randomCountry()
# getCountryInfo(x)
getRandomHints()
