from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from collections import Counter
from urllib.request import urlopen
import sqlite3
import json
                                                                                                                                       
app = Flask(__name__)  
@app.route('/')
def hello_world():
    return render_template('hello.html')
                                                                                                                                       
@app.route("/contact/")
def MaPremiereAPI():
    return render_template('contact.html')
  
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
@app.route("/histogramme/")
def monhistp():
    return render_template("histogramme.html")
  
@app.route('/commits/')
def commits():
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    response = urlopen(url)
    data = json.loads(response.read().decode())  # Correction ici

    minute_list = []
    for item in data:
        date_str = item['commit']['author']['date']
        date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
        minute_list.append(date_obj.minute)

    commit_counts = Counter(minute_list)
    chart_data = [{"minute": str(minute), "count": count} for minute, count in sorted(commit_counts.items())]

    return jsonify(results=chart_data)

@app.route('/commits-graphique/')
def graph_commits():
    return render_template('commits.html')
  
if __name__ == "__main__":
  app.run(debug=True)
