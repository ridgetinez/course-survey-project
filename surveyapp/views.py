from surveyapp import app
from flask import render_template
from flask import Flask, flash, redirect, render_template, request, session, abort

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login_page.html')
    else:
        return render_template('admin_page.html')

@app.route('/login', methods=['POST'])
def login():
	global user_list = UserAuthenticator
	username = request.form['username']
	password = request.form['password']
	if user_list.authenticate(username, password):
		session['logged_in'] = True
	else:
		flash('wrong password!')
	return home()


