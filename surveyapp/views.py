from surveyapp import app, authenticator, models, readers, writers
from flask import render_template, session, redirect, url_for, request

#TEMPORARY
global questions
questions = models.QuestionStore([])
global surveys
surveys = []
#TEMPORARY

@app.route('/', methods=['GET', 'POST'])
def index():
    """ Returns/renders the admin dashboard page (if access authorised) or the landing page (if access not authorised) """
    if request.method == 'POST':
        #for search button
        if 'search' in request.form:
            return redirect(request.form['search'])
        #attempt to authenticate user using information from login form
        auth_success = authenticator.authenticate(request.form['email'], request.form['password'])

        if auth_success == True:    #if authenticated redirect to admin dashboard (user will have cookie marking as auth'd)
            return redirect(url_for('admin_dashboard', sub_page='surveys'))
        else:                       #render landing page again with notification of invalid login credentials
            return render_template('landing_page.html', failedAuth=True)

    return render_template('landing_page.html')

@app.route('/dashboard/<sub_page>')
def admin_dashboard(sub_page):
    """ Returns/renders the survey/questions creation page or an index page (if unauthorised user access URL) """
    
    #non-authenticated user attempts access
    if authenticator.checkAuthenticated() == False:
        return redirect(url_for('index'))

    if sub_page == 'surveys':
        return render_template('admin_dashboard_surveys.html', surveys=surveys)
    if sub_page == 'questions':
        return render_template('admin_dashboard_questions.html', questions=questions.get_all_questions())


@app.route('/dashboard/add/question', methods=['GET', 'POST'])
def admin_dashboard_add_q():
    if request.method == 'POST':
        #catch these first
        if 'add_answer' in request.form:
            session['n_answers'] += 1
            return render_template('admin_dashboard_create_q.html', n_answers=session['n_answers'])    
        if 'remove_answer' in request.form:
            session['n_answers'] -= 1
            return render_template('admin_dashboard_create_q.html', n_answers=session['n_answers'])
        if 'cancel' in request.form:
            session.pop('n_answers')
            return redirect(url_for('admin_dashboard', sub_page='questions'))

        #otherwise write question and redirect
        question_text = request.form['question_text']
        answers = []
        for i in range(session['n_answers']):
            answers.append(request.form['answer' + str(i)])
        
        #catch form input errors
        if question_text == "":
            return render_template('admin_dashboard_create_q.html', question_error=True, n_answers=session['n_answers'])
        if "" in answers:
            return render_template('admin_dashboard_create_q.html', answer_error=True, n_answers=session['n_answers'])
         #check unique answers
        if len(set(answers)) < len(answers):
            return render_template('admin_dashboard_create_q.html', answer_error=True, n_answers=session['n_answers'])       
 
        #create and save question
        new_question = models.Question(question_text, answers)

        session.pop('n_answers')
        questions.add_question(new_question) 
        return redirect(url_for('admin_dashboard', sub_page='questions'))

    #if first time form reached
    session['n_answers'] = 4
    return render_template('admin_dashboard_create_q.html', n_answers=session['n_answers'])

@app.route('/dashboard/add/survey', methods=['GET', 'POST'])
def admin_dashboard_add_s():
    #create course list
    course_list = []
    for course in readers.CourseReader.read(None, "surveyapp/static/courses.csv"):
        course_list.append("".join(course))
    
    if request.method == 'POST':
        #catch cancel
        if 'cancel' in request.form:
            return redirect(url_for('admin_dashboard', sub_page='surveys'))
        selected_questions = []
        course_name = request.form["course_name"]
        for i in range(len(questions.get_all_questions())):
            if str(i) in request.form:
                selected_questions.append(questions.get_all_questions()[i])
        if len(selected_questions) == 0:
            return render_template('admin_dashboard_create_survey.html', questions=questions.get_all_questions(), course_list=course_list, selection_error=True)
        surveys.append(models.Survey(selected_questions, course_name))
        return redirect(url_for('admin_dashboard', sub_page='surveys'))

    return render_template('admin_dashboard_create_survey.html', questions=questions.get_all_questions(), course_list=course_list)

@app.route('/survey/respond/<course_id>/<survey_id>', methods=['POST', 'GET'])
def respond(course_id, survey_id):
    try:
        survey = surveys[int(survey_id)]
    except IndexError: #survey doesn't exist
        return '<h1>Error Survey Doesn\'t exist</h1>'

    if request.method == 'POST':
        #check all answered
        if len(request.form) < len(survey.get_all_questions()):
            return render_template("view_survey.html", survey=survey, error_not_answered=True)
        writer = writers.ResponseWriter(survey)
        #for question_id, answer_id in request.form.items(): UNCOMMENT WHEN WRITER IS DONE
            #writer.update_row(question_id, answer_id) UNCOMMENT WHEN WRITER IS DONE
        return render_template("view_survey.html", survey=survey, notif_success=True)
    return render_template("view_survey.html", survey=survey)   
