from surveyapp import app
from flask import render_template, session

@app.route('/')
def index():
    if "admin_flag" not in session:
        session["admin_flag"] = False
    return render_template('landing_page.html');

#need to add auth
@app.route('/dashboard/<sub_page>')
def admin_dashboard(sub_page):
    if sub_page == 'surveys':
        return render_template('admin_dashboard_surveys.html');
    if sub_page == 'questions':
        return render_template('admin_dashboard_questions.html');
