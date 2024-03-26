from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
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
def commits():
    # Récupérer les données des commits depuis l'API GitHub
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    response = requests.get(url)
    commits_data = response.json()
    
    # Initialiser un dictionnaire pour stocker le nombre de commits par minute
    commits_per_minute = {}
    
    # Parcourir les données des commits
    for commit in commits_data:
        # Extraire la date et l'heure du commit
        commit_date_str = commit['commit']['author']['date']
        commit_date = datetime.strptime(commit_date_str, '%Y-%m-%dT%H:%M:%SZ')
        
        # Récupérer la minute du commit
        minute = commit_date.minute
        
        # Incrémenter le nombre de commits pour cette minute
        if minute in commits_per_minute:
            commits_per_minute[minute] += 1
        else:
            commits_per_minute[minute] = 1
    
    # Convertir le dictionnaire en listes de minutes et de nombre de commits
    minutes = list(commits_per_minute.keys())
    commits_count = list(commits_per_minute.values())
    
    # Rendre les données disponibles pour le rendu HTML
    return render_template('commits.html', minutes=minutes, commits_count=commits_count)

if __name__ == "__main__":
  app.run(debug=True)
