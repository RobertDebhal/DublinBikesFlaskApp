from flask import render_template
from SE_group_project import app

@app.route('/')
def weather():
    return render_template("weather.html")
