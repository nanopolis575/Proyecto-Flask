from flask import Flask,render_template, session, redirect
import pygal
from pygal.style import Style
import json
import time
import pandas as pd
app = Flask(__name__)

custom_style = Style(
        colors=('#991515','#1cbc7c'),
        background='#d2ddd9'
        )


#@app.route("/")
#def hello():
#    return render_template("index.html")

df = pd.read_csv("datos.csv")

@app.route("/",methods=("POST", "GET"))
def html_table():
    return  render_template('index.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)
# -------------------------------------------
# Charting route which displays the bar chart
# -------------------------------------------

@app.route("/graficabar")
def bar():
    with open('bar.json','r') as bar_file:
        data = json.load(bar_file)
    chart = pygal.Bar(style = custom_style)
    intentos_list = [x['intentos'] for x in data]
    puntaje_list = [x['puntaje'] for x in data]
    chart.add('Puntaje',puntaje_list)
    chart.add('intentos',intentos_list)
    chart.x_labels = [x['name'] for x in data]
    chart.render_to_file('static/images/Grafica.svg')
    img_url = 'static/images/grafica.svg?cache=' + str(time.time())
    return render_template('nano.html',image_url = img_url)

if __name__=="__main__":
    app.run()
