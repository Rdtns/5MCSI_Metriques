from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from flask import requests
from datetime import datetime
from urllib.request import urlopen
import sqlite3
import urlib.request
                                                                                                                                       
app = Flask(__name__)

@app.route("/contact/")
def MaPremiereAPI():
    return "<h2>Ma page de contact</h2>"

@app.route("/contacts/")
def moncontact():
    return render_template("contact.html")

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)
  
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/Histogramme/")
def mongraphique2():
    return render_template("Histogramme.html")

@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minutes = date_object.minute
        return jsonify({'minutes': minutes})
                                                                                                                               
@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/commits')
def get_commits():
    # URL de l'API GitHub
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    
    # Effectuer une requête GET à l'API GitHub
    with urlopen(url) as response:
        data = response.read()
    
    # Convertir les données JSON en Python dict
    commits_data = json.loads(data)
    
    # Extraire la quantité de commits (nombre total de commits)
    total_commits = len(commits_data)
    
    return jsonify({'total_commits': total_commits})

if __name__ == "__main__":
  app.run(debug=True)
