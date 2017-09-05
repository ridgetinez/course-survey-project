from surveyapp import app
from flask import render_template

#placeholder
@app.route('/')
def index():
    return render_template('landing_page.html');
