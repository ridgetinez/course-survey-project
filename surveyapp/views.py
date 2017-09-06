from surveyapp import app, authenticator, models
from flask import render_template, session, redirect, url_for, request

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        
        #attempt to authenticate user using information from login form
        auth_success = authenticator.authenticate(request.form['email'], request.form['password'])

        if auth_success == True:    #if authenticated redirect to admin dashboard (user will have cookie marking as auth'd)
            return redirect(url_for('admin_dashboard', sub_page='surveys'))
        else:                       #render landing page again with notification of invalid login credentials
            return render_template('landing_page.html', failedAuth=True)

    return render_template('landing_page.html')

@app.route('/dashboard/<sub_page>')
def admin_dashboard(sub_page):
    #non-authenticated user attempts access
    if authenticator.checkAuthenticated() == False:
        return redirect(url_for('index'))

    if sub_page == 'surveys':
        return render_template('admin_dashboard_surveys.html')
    if sub_page == 'questions':
        return render_template('admin_dashboard_questions.html')

@app.route('/dashboard/add/<add_type>', methods=['GET', 'POST'])
def admin_dashboard_add(add_type):
    if request.method == 'POST':
        #catch these first
        if 'add_answer' in request.form:
            session['n_answers'] += 1
            return render_template('admin_dashboard_create_q.html', n_answers=session['n_answers'])    
        if 'remove_answer' in request.form:
            session['n_answers'] -= 1
            return render_template('admin_dashboard_create_q.html', n_answers=session['n_answers'])

        #otherwise write question and redirect
        question_text = request.form['question_text']
        answers = []
        for i in range(session['n_answers']):
            answers.append(request.form['answer' + str(i)])
        new_question = models.Question(question_text, answers)
        session.pop('n_answers')
        print(new_question) #THIS IS THE COMPLETED QUESTION TO BE WRITTEN
        return redirect(url_for('admin_dashboard', sub_page='questions'))

    #if first time form reached
    session['n_answers'] = 4
    if add_type == "question":
        return render_template('admin_dashboard_create_q.html', n_answers=session['n_answers'])
