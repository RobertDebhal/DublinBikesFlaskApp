from flask import render_template,jsonify, g, json, Flask
from se_group_project import app
import sqlalchemy
import f, o, r

app.config.from_object('config')
name={}

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
def JSONr(json=f.json):
    return jsonify(json)

@app.route('/fatimaJSON')
def JSONf(json=f.json):
    return jsonify(json)

@app.route('/orlaJSON')
def JSONo(json=o.json):
    return jsonify(json)

#http://flask.pocoo.org/docs/0.12/patterns/errorpages/
#@app.errorhandler(404)
#def page_not_found(e):
#    return render_template('404.html'), 404


#@app.errorhandler(500)
#def internal_error(e):
#    return render_template('500.html'), 500
