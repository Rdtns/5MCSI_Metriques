from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from flask import requests
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
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

@app.route('/commits/')
def get_commits():
    # URL de l'API GitHub pour récupérer les commits
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    
    try:
        # Récupération des données depuis l'API GitHub
        response = urlopen(url)
        raw_data = response.read()
        commits_data = json.loads(raw_data)

        # Extraction des informations pertinentes (date et auteur) pour chaque commit
        commits = [{'date': commit['commit']['author']['date'], 'author': commit['commit']['author']['name']} for commit in commits_data]

        return jsonify({'commits': commits})
    except Exception as e:
        return str(e), 500  # Retourne une erreur 500 en cas d'erreur lors de la récupération des données

if __name__ == "__main__":
  app.run(debug=True)
