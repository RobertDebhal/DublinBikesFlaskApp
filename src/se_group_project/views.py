from flask import render_template,jsonify, g, json, Flask
from se_group_project import app
import sqlalchemy
import sqlite3
import pickle
import requests
import pandas as pd
import datetime

#app.config.from_object('config')

#from lecture notes
def connect_to_database():
    engine = sqlalchemy.create_engine('mysql+pymysql://teamforsoft:whocares1@teamforsoft.ci76dskzcb0m.us-west-2.rds.amazonaws.com:3306/SE_group_project')
    return engine

def connect_to_local_db():
    engine = sqlite3.connect('most_recent_station_data.db')
    return engine

#@app.before_request
#def before_request():
#    g.db = connect_to_database()

#@app.teardown_request
#def teardown_request(exception):
#    db = getattr(g, '_database', None)
#    if db is not None:
#        db.close()
		
		
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

#Need to figure out
#@app.teardown_appcontext
#def close_connection(exception):
#    db = getattr(g, '_database', None)
#    if db is not None:
#        db.close()

#with app.app_context():
    #print(get_db())
    #print(g.get('_database', None))
name={}
@app.route('/')
def weather(name=name):
    return render_template("weathero.html",name=name)

@app.route('/orlaJSON')
def JSONo():
	engine = connect_to_local_db()
	engine.row_factory=sqlite3.Row
	cur = engine.cursor()
	rows=cur.execute('SELECT s.number,s.lat,s.lng,o.available_bikes,o.bike_stands FROM static s, occupancy o where s.number = o.number')
	data = []
	for row in rows: 
		data.append(dict(row))
	return jsonify(data) 

@app.route("/available/<int:station_id>")
def get_stations(station_id):
	engine = connect_to_local_db()
	engine.row_factory=sqlite3.Row
	cur = engine.cursor()
	rows=cur.execute('SELECT * FROM occupancy WHERE number ={} ;'.format(station_id))
	data = []
	for row in rows: 
		data.append(dict(row))
	return jsonify(data) 

@app.route("/rain/<int:station_id>")
def get_rain(station_id):
	engine = connect_to_local_db()
	engine.row_factory=sqlite3.Row
	cur = engine.cursor()
	cur2 = engine.cursor()
	rows=cur.execute('SELECT AVG(available_bikes) as average_available_rain, number, rain_status, hours FROM rain_occupancy WHERE number ={} and rain_status="Raining" GROUP BY hours;'.format(station_id))
	rows2=cur2.execute('SELECT AVG(available_bikes) as average_available_no_rain, number, rain_status, hours FROM rain_occupancy WHERE number ={} and rain_status="Not Raining" GROUP BY hours;'.format(station_id))
	print(rows2)
	data = []
	for row in rows: 
		data.append(dict(row))
	for row in rows2:
		data.append(dict(row))
	return jsonify(data) 

@app.route("/<int:station_id>/<int:day>/<int:hour>")
def predict(station_id,day,hour):
    engine = connect_to_database()
    conn = engine.connect() 
    rows=conn.execute('SELECT last_update, AVG(available_bikes) FROM dynamic WHERE number ={};'.format(station_id))
    data = []
    for row in rows:
        #dt = datetime.datetime(last_update)
        data.append(dict(row))
        #data.append(dt)
    return jsonify(data)
  



#http://flask.pocoo.org/docs/0.12/patterns/errorpages/
#@app.errorhandler(404)
#def page_not_found(e):
#    return render_template('404.html'), 404


#@app.errorhandler(500)
#def internal_error(e):
#    return render_template('500.html'), 500
