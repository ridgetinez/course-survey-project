from surveyapp import app
from flask import render_template, session, redirect, url_for, request
from surveyapp import authenticator

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        auth_success = authenticator.authenticate(request.form['email'], request.form['password'])
        if auth_success == True:
            return redirect(url_for('admin_dashboard', sub_page='surveys'))
        else:
            return render_template('landing_page.html', failedAuth=True)
    return render_template('landing_page.html');

#need to add auth
@app.route('/dashboard/<sub_page>')
def admin_dashboard(sub_page):
    #non-authenticated user attempts access
    if authenticator.checkAuthenticated() == False:
        return redirect(url_for('index'))

    if sub_page == 'surveys':
        return render_template('admin_dashboard_surveys.html');
    if sub_page == 'questions':
        return render_template('admin_dashboard_questions.html');
