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

@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minutes = date_object.minute
        return jsonify({'minutes': minutes})
@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})

@app.route('/commits')
def get_commits():
    # URL de l'API GitHub pour récupérer les commits
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    
    # Effectuer une requête GET à l'API GitHub
    response = requests.get(url)
    
    # Vérifier si la requête a réussi
    if response.status_code == 200:
        # Convertir la réponse en format JSON
        commits_data = response.json()
        
        # Traiter les données pour obtenir le nombre de commits par minute
        commits_per_minute = {}
        for commit in commits_data:
            # Extraire la date du commit et le convertir en objet datetime
            commit_date = datetime.strptime(commit['commit']['author']['date'], '%Y-%m-%dT%H:%M:%SZ')
            
            # Extraire la minute du commit
            minute = commit_date.minute
            
            # Mettre à jour le nombre de commits pour cette minute
            if minute in commits_per_minute:
                commits_per_minute[minute] += 1
            else:
                commits_per_minute[minute] = 1
        
        # Retourner les données au format JSON
        return jsonify(commits_per_minute)
    else:
        # Si la requête a échoué, retourner un message d'erreur
        return jsonify({'error': 'Failed to fetch commits data'})

@app.route('/')
def index():
    return render_template('index.html')
  
if __name__ == "__main__":
  app.run(debug=True)
