from flask import render_template,jsonify, g, json, Flask
from se_group_project import app
import sqlalchemy

#app.config.from_object('config')

#from lecture notes
def connect_to_database():
    engine = sqlalchemy.create_engine('mysql+pymysql://teamforsoft:whocares1@teamforsoft.ci76dskzcb0m.us-west-2.rds.amazonaws.com:3306/SE_group_project')
    return engine


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
	engine = get_db()
	data = []
	rows = engine.execute('SELECT * FROM static')
	for row in rows:
		data.append(dict(row))
	return jsonify(data) 

@app.route("/available/<int:station_id>")
def get_stations(station_id):
	engine = get_db()
	data = []
	rows = engine.execute('SELECT * FROM dynamic d, static s WHERE d.number=s.number and d.number = {} and d.last_update = (SELECT max(last_update) FROM dynamic d WHERE d.number={} ) ;'.format(station_id,station_id))
	for row in rows:  # last_update,available_bikes, available_bike_stands, bike_stands, number,status,latest_weather
		data.append(dict(row))
	return jsonify(data) 



#http://flask.pocoo.org/docs/0.12/patterns/errorpages/
#@app.errorhandler(404)
#def page_not_found(e):
#    return render_template('404.html'), 404


#@app.errorhandler(500)
#def internal_error(e):
#    return render_template('500.html'), 500