from flask import render_template
from se_group_project import app
from flask import jsonify
from flask import json
import QueryDatabase
import sqlalchemy
import f, o, r

from API_scraper import api_token, api_url_base
engine = sqlalchemy.create_engine('mysql+pymysql://teamforsoft:whocares1@teamforsoft.ci76dskzcb0m.us-west-2.rds.amazonaws.com:3306/SE_group_project')
conn = engine.connect()
name = QueryDatabase.getStaticInfo(engine, conn)
# print (name)

@app.route('/')
def weather(name=name):
    return render_template("weather.html",name=name)

@app.route('/fatima')
def weatherf(name=f.name):
    return render_template("weatherf.html",name=name)

@app.route('/orla')
def weathero(name=o.name):
    return render_template("weathero.html",name=name)

@app.route('/robbie')
def weatherr(name=f.name):
    return render_template("weatherr.html",name=name)

@app.route('/robbieJSON')
def JSONr(json=f.json
):
    return jsonify(json)

@app.route('/fatimaJSON')
def JSONf(json=f.json):
    return jsonify(json)

@app.route('/orlaJSON')
def JSONo(json=o.json):
    return jsonify(json)

