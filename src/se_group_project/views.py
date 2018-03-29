from flask import render_template
from se_group_project import app
from flask import jsonify
from flask import json

name={'ClarendonRow':{'lat':53.340927,'lng':-6.262501},
'BlessingtonStreet':{'lat':53.35676899999999,
'lng':-6.26814},
'BoltonStreet':{'lat':53.351181999999994,
'lng':-6.269858999999999},
'GreekStreet':{'lat':53.346874,'lng':-6.272976},
'CharlemontStreet':{'lat':53.330662,'lng':-6.260177},
'ChristchurchPlace':{'lat':53.343368000000005,
'lng':-6.2701199999999995},
'HighStreet':{'lat':53.343565000000005,'lng':-6.275071},
'CustomHouseQuay':{'lat':53.34788399999999,
'lng':-6.248048000000001},
'ExchequerStreet':{'lat':53.343033999999996,
'lng':-6.263578}}

@app.route('/')
def weather(name=name):
    return render_template("weather.html",name=name)
