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
restCountriesLink = "https://restcountries.com/v3.1/independent?fields=name,cca2,cca3"
restCountriesURL = urllib.request.urlopen(restCountriesLink)
readCountries = restCountriesURL.read()
countryDict = json.loads(readCountries)


cleanerDict = {}
i = 0
# Only keep countries' names and other useful identifying codes for them.
for country in countryDict:
    cleanerDict[i] = country['name']['common'], country['cca2'], country['cca3']
    i+=1

# Get a list of all full names of valid countries
def nameLst():
    rcLink = "https://restcountries.com/v3.1/independent?fields=name,cca2,cca3"
    rcURL = urllib.request.urlopen(restCountriesLink)
    readRC = restCountriesURL.read()
    loader = json.loads(readCountries)

    names = []
    i = 0
    for country in loader:
        names.append(country['name']['common'])
        i+=1
    return names

# Returns the 2 letter code of a random country from our dict
def randomCountry():
    x = random.randint(0,193)
    code = cleanerDict[x][1]
    return code

# Loads info on given country from API, and stores wanted information
def getCountryInfo(x):
    a = f"https://restcountries.com/v3.1/alpha/{x}"
    b = urllib.request.urlopen(a)
    c = b.read()
    d = json.loads(c)

    # Languages
    langLst = []
    for l in d[0]['languages']:
        langLst.append(d[0]['languages'][l])

    # Currencies
    currencyLst = []
    for i in d[0]['currencies']:
        currencyLst.append(d[0]['currencies'][i]['name'])

    # Coordinates
    coords = []
    for i in d[0]['capitalInfo']['latlng']:
        coords.append(i)

    # Bordering countries
    bordering = []
    if 'borders' in d[0]:
        for i in d[0]['borders']:
            bordering.append(i)

    # Compile all most relevant info
    info = {
        'name': [d[0]['name']['common'], x],
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
    return info

# Get weather info from API, on given coords
def getWeather(lat, long, units):
    try:
        # Can we open the key?
        file = open("./keys/key_openWeatherMap.txt")
    except:
        # NO?!?!?!
        print("Key File Not Found")
    else:
        # Load API info
        weatherKey = file.readline()
        weatherKey = weatherKey[:-1]
        restWeatherLink = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&appid={weatherKey}&units={units}"
        try:
            restWeatherURL = urllib.request.urlopen(restWeatherLink)
        except:
            print("Weather API key not found")
        else:
            readWeather = restWeatherURL.read()
            weatherDict = json.loads(readWeather)
            return weatherDict

# Get the full name of a country based on cca3 code
def getCountryFullName(cca3):
    for i in cleanerDict:
        if cca3 in cleanerDict[i]:
            return cleanerDict[i][0]
    return ""

# Get the cca2 code of a country based on its full name
def getCountryCCA2(full):
    for i in cleanerDict:
        if full in cleanerDict[i]:
            return cleanerDict[i][1]
    return ""

# Compile all user hints in a nice list to be used.
def getHints(x, units):
    # Load info on a country, random or preset, depends
    if x == "":
        x = randomCountry()
    x = getCountryCCA2(x)
    countryInfo = getCountryInfo(x)
    weatherInfo = getWeather(countryInfo['LatLong'][0],countryInfo['LatLong'][1], units)

    hints = []
    # First Hint: Uses weather data
    if units == 'metric':
        hints.append(["Temperature: " + str(weatherInfo['main']['temp']) + "°C" , "Feels Like: " + str(weatherInfo['main']['feels_like']) + "°C" , "Weather Description: " + weatherInfo['weather'][0]['main'] + "; " + weatherInfo['weather'][0]['description']])
    if units == 'imperial':
        hints.append(["Temperature: " + str(weatherInfo['main']['temp']) + "°F" , "Feels Like: " + str(weatherInfo['main']['feels_like']) + "°F" , "Weather Description: " + weatherInfo['weather'][0]['main'] + "; " + weatherInfo['weather'][0]['description']])

    # Second Hint: Continets it lies on, area, and population
    continents = countryInfo['continents']
    x = len(continents)
    if x > 1:
        contStr = "Continents: "
    else if x == 1:
        contStr = "Continent: "
    for i in continents:
        contStr += i + "; "
    pop = '{:,}'.format(countryInfo['population'])
    area = countryInfo['area']
    if units == 'metric':
        area = '{:,}'.format(area)
        hints.append([contStr, "Area: " + area + " km²", "Population: " + pop])
    if units == 'imperial':
        area *= 0.386102
        area = round(area)
        area = '{:,}'.format(area)
        hints.append([contStr, "Area: " + area + " mi²", "Population: " + pop])

    # Third Hint: Subregion, coat of arms image, and is it land locked
    coaIMG = f"<img src=\"{countryInfo['coatOfArms']}\" alt=\"Coat of Arms\" width=\"100\" height=\"150\">"
    hints.append(["Subregion: " + countryInfo['subregion'], coaIMG, "Land Locked?: " + str(countryInfo['landlocked'])])

    # Fourth Hint: The capital, and bordering countries
    bord = "Bordering Countries: "
    for i in countryInfo['borderingCountries']:
        x = getCountryFullName(i)
        bord += x
        if len(x) > 0:
            bord += "; "
    if len(countryInfo['borderingCountries']) == 0:
        bord += "None"
    hints.append(["Captial: " + countryInfo['capital'][0], bord])

    # Fifth Hint: All the country's currency, and languages
    if len(countryInfo['currency']) > 1:
        currencyStr = "Currencies: "
    else:
        currencyStr = "Currency: "
    for i in countryInfo['currency']:
        currencyStr += i + "; "
    if len(countryInfo['languages']) > 1:
        langStr = "Languages: "
    else:
        langStr = "Language: "
    for i in countryInfo['languages']:
        langStr += i + "; "
    hints.append([currencyStr, langStr])

    # Sixth Hint: Image of flag
    flagIMG = f"<img src=\"https://flagsapi.com/{countryInfo['name'][1]}/flat/64.png\" alt=\"Flag\" width=\"200\" height=\"200\">"
    hints.append([flagIMG])

    # Added at the end, not really a hint, but the Anwser
    hints.append(["The country was: ", countryInfo['name'][0]])

    return hints
