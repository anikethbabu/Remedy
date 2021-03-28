# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 09:37:05 2021

@author: Anike_2pan514
"""
from flask import Flask, render_template, request
import requests
import pgeocode
import json

def getlatlong(zipcode):
    nomi = pgeocode.Nominatim('us')
    result = nomi.query_postal_code(zipcode)
    return result.latitude, result.longitude

def getValues(zipcode):
     lat, longitude= getlatlong(zipcode)
     headers = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0; Touch)'}
     api = 'https://api.us.castlighthealth.com/vaccine-finder/v1/provider-locations/search?medicationGuids=779bfe52-0dd8-4023-a183-457eb100fccc,a84fb9ed-deb4-461c-b785-e17c782ef88b,784db609-dc1f-45a5-bad6-8db02e79d44f&lat={}&long={}&radius=10'.format(lat,longitude)
     response = requests.get(api, headers = headers)
     jsonvalues = response.json()
     return [(values['name'], values['distance'], values['address1'], values['phone']) for values in jsonvalues['providers']]

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('htmlthing.html')

@app.route('/zip', methods = ["GET", "POST"])
def zip():
    zipval = request.form.get("zip")
    result = getValues(zipval)
    return render_template("zip.html",result = result)

if __name__ == "__main__":
    app.run(debug=True)
    