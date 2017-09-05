from surveyapp import app, auth
from flask import render_template
from flask import Flask, flash, redirect, render_template, request, session, abort

@app.route('/')



def home():
    if not session.get('logged_in'):
        return render_template('login_page.html')
    else:
        return render_template('admin_dashboard_surveys.html');
@app.route('/login', methods=['GET', 'POST'])



def login():
	user_list = UserAuthenticator(__name__)
	username = request.form['username']
	password = request.form['password']
	if user_list.authenticate(username, password) == True:
		session['logged_in'] = True
	else:
		flash('wrong password!')
	return home()

#need to add auth
@app.route('/dashboard/<sub_page>')
def admin_dashboard(sub_page):
	if sub_page == 'surveys':
		return render_template('admin_dashboard_surveys.html');
	if sub_page == 'questions':
		return render_template('admin_dashboard_questions.html');
		return home()
