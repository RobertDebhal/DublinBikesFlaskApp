from flask import render_template
from se_group_project import app
from flask import jsonify
from flask import json
import QueryDatabase
import sqlalchemy
import f

from API_scraper import api_token, api_url_base
engine = sqlalchemy.create_engine('mysql+pymysql://teamforsoft:whocares1@teamforsoft.ci76dskzcb0m.us-west-2.rds.amazonaws.com:3306/SE_group_project')
conn = engine.connect()
name = QueryDatabase.getStaticInfo(engine, conn)
# print (name)

@app.route('/')
def weather(name=name):
    return render_template("weather.html",name=name)

@app.route('/fatima')
def weather(name=f.name):
    return render_template("weatherf.html",name=name)

@app.route('/')
def weather(name=name):
    return render_template("weather.html",name=name)

@app.route('/')
def weather(name=name):
    return render_template("weather.html",name=name)
