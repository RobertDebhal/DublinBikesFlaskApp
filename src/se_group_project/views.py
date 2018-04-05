from flask import render_template,jsonify, g, json, Flask
from se_group_project import app
import sqlalchemy
import sqlite3

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
	engine = get_db()
	data = []
	rows = engine.execute('SELECT * FROM static s, dynamic d where  s.number = d.number AND ( s.number,d.last_update) IN (SELECT dy.number, MAX(dy.last_update) FROM dynamic dy group by dy.number) ')
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














#http://flask.pocoo.org/docs/0.12/patterns/errorpages/
#@app.errorhandler(404)
#def page_not_found(e):
#    return render_template('404.html'), 404


#@app.errorhandler(500)
#def internal_error(e):
#    return render_template('500.html'), 500
