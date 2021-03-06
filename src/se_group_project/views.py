from flask import render_template,jsonify, g, json, Flask
from se_group_project import app
import sqlalchemy
import sqlite3
import pickle
import requests
import json
import pandas as pd
import math
import datetime
#app.config.from_object('config')

#from lecture notes
def connect_to_database():
    engine = sqlalchemy.create_engine('mysql+pymysql://teamforsoft:whocares1@teamforsoft.ci76dskzcb0m.us-west-2.rds.amazonaws.com:3306/SE_group_project')
    return engine

def connect_to_local_db():
    engine = sqlite3.connect('most_recent_station_data.db')
    return engine

def get_future_weather_info():
    """
    Function to retrieve prediction data 
    for Dublin Weather in JSON format.
    """
    response = requests.get('http://api.openweathermap.org/data/2.5/forecast?q=Dublin,ie&APPID=70ef396e3ce3949e0934b4428e41f453')
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

def num_map(num):
    if num%3==0:
        return num
    nums = [[0,3],[3,6],[6,9],[9,12],[12,15],[15,18],[18,21]]
    found=False

    for elem in nums:
        if num > elem[0]and num<elem[1]:
            if (num - elem[0])<=1.5:
                num=elem[0]
            else:
                num=elem[1]
            found=True
    if found:
        return num
    else:
        num=21
        return num
def to_datetime(date_time_string):
    date_time_list=date_time_string.split(' ')
    date=date_time_list[0].split()
    date_seperated = date[0].split('-')
    year = date_seperated[0]
    month = date_seperated[1]
    day = date_seperated[2]
    hour_list= date_time_list[1].split(':')
    hour_of_day= hour_list[0]
    date_list=date[0].split('-')
    dtObj = datetime.datetime(int(year),int(month),int(day),int(hour_of_day))
    return dtObj

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
    hour = num_map(hour)
    response = get_future_weather_info()
    index_to_use=-1
    for i in range(len(response['list'])):
        dt = to_datetime(response['list'][i]['dt_txt'])
        if dt.weekday()==day and dt.hour==hour:
            index_to_use=i
            i+=1
    if index_to_use >= 0:
        wind = response['list'][index_to_use]['wind']['speed']
        desc = response['list'][index_to_use]['weather'][0]['description']
        temp = response['list'][index_to_use]['main']['temp']-273.15
        with open("./analytics/"+str(station_id)+"/"+str(day)+"/"+str(hour)+"/model.pkl","rb") as input:
            model = pickle.load(input)
        df = pd.DataFrame([[wind,temp,1,0]],columns=['wind','temperature','rain_True','rain_False'])
        prediction = model.predict(df)
        if prediction[0]<0:
            prediction[0]=0
        return "Prediction is: " + str(math.ceil(prediction[0])) + " available bikes"
    else:
        return "Sorry, no data for that time"













#http://flask.pocoo.org/docs/0.12/patterns/errorpages/
#@app.errorhandler(404)
#def page_not_found(e):
#    return render_template('404.html'), 404


#@app.errorhandler(500)
#def internal_error(e):
#    return render_template('500.html'), 500
