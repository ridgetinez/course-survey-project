from surveyapp import app, readers, modelcontrollers, auth, controller
from flask import render_template, session, redirect, url_for, request

@app.route('/', methods=['GET', 'POST'])
def index():
    """ Returns/renders the admin dashboard page (if access authorised) or the landing page (if access not authorised) """
    if request.method == 'POST':
        #attempt to authenticate user using information from login form
        auth_success = auth.AuthController.login(request.form["user-type"], request.form["id"], request.form["password"])

        if auth_success == True:    #if authenticated redirect to admin dashboard (user will have cookie marking as auth'd)
            if request.form["user-type"] == "admin":
                return redirect(url_for("admin_dashboard", sub_page="surveys"))
            else:
                return redirect(url_for("{}_dashboard".format(request.form["user-type"]), id=request.form["id"]))
        else:                       #render landing page again with notification of invalid login credentials
            return render_template('landing_page.html', failedAuth=True)

    return render_template('landing_page.html')

@app.route('/dashboard/<sub_page>', methods=['GET', 'POST'])
def admin_dashboard(sub_page):
    """ Returns/renders the survey/questions creation page or an index page (if unauthorised user access URL) """

    #non-authenticated user attempts access
    if auth.UserAuthoriser.check_permission("admin", "") == False:
        return redirect(url_for('invalid_permission'))

    if sub_page == 'surveys':
        return render_template('admin_dashboard_surveys.html', surveys=modelcontrollers.SurveyController.get_all_surveys())
    if sub_page == 'questions':
        if request.method == 'POST':
            if "delete" in request.form:
                modelcontrollers.QuestionController.delete_question(request.form["delete"])
        return render_template('admin_dashboard_questions.html', questions=modelcontrollers.QuestionController.get_all_questions())


@app.route('/dashboard/add/question/<qtype>', methods=['GET', 'POST'])
def admin_dashboard_add_q(qtype):
    #non-authenticated user attempts access
    if auth.UserAuthoriser.check_permission("admin", "") == False:
        return redirect(url_for('invalid_permission'))

    if request.method == 'POST':
        #catch these first
        print(request.form)
        if 'add_answer' in request.form:
            session['n_answers'] += 1
            return render_template('admin_dashboard_create_q.html', n_answers=session['n_answers'], qtype=qtype)
        if 'remove_answer' in request.form:
            session['n_answers'] -= 1
            return render_template('admin_dashboard_create_q.html', n_answers=session['n_answers'], qtype=qtype)
        if 'cancel' in request.form:
            session.pop('n_answers')
            return redirect(url_for('admin_dashboard', sub_page='questions', qtype=qtype))

        #otherwise write question and redirect
        result = controller.FormController.parse_create_q(request.form)

        #catch form input errors
        if result[0] == False:
            if result[1] == 'qerror':
                return render_template('admin_dashboard_create_q.html', question_error=True, n_answers=session['n_answers'], qtype=qtype)
            elif result[1] == 'aerror':
                return render_template('admin_dashboard_create_q.html', answer_error=True, n_answers=session['n_answers'], qtype=qtype)
            else:
                print('error: unexpected error thrown when parsing add_q form')


        session.pop('n_answers')
        return redirect(url_for('admin_dashboard', sub_page='questions', qtype=qtype))

    #if first time form reached
    if qtype == 'mcq':
        session['n_answers'] = 4
    if qtype == 'textans':
        session['n_answers'] = 0
    return render_template('admin_dashboard_create_q.html', n_answers=session['n_answers'], qtype=qtype)

@app.route('/dashboard/add/survey', methods=['GET', 'POST'])
def admin_dashboard_add_s():
    #non-authenticated user attempts access
    if auth.UserAuthoriser.check_permission("admin", "") == False:
        return redirect(url_for('invalid_permission'))
    #create course list
    course_list = modelcontrollers.CourseController.get_courses()
    for course in readers.CourseReader.read(None, "surveyapp/static/courses.csv"):
        course_list.append("".join(course))

    if request.method == 'POST':
        #catch cancel
        if 'cancel' in request.form:
            return redirect(url_for('admin_dashboard', sub_page='surveys'))
        controller.FormController.parse_create_survey(request.form)

        return redirect(url_for('admin_dashboard', sub_page='surveys'))

    return render_template('admin_dashboard_create_survey.html', questions=modelcontrollers.QuestionController.get_all_questions(), course_list=course_list)

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
        print(request.form.items())
        for question_id, answer_id in request.form.items():
            writer.update_row(question_id, answer_id)
        return render_template("view_survey.html", survey=survey, notif_success=True)
    return render_template("view_survey.html", survey=survey)

@app.route('/studentdashboard/<id>')
def student_dashboard(id):
    if auth.UserAuthoriser.check_permission("student", id) == False:
        return redirect(url_for('invalid_permission'))

    return render_template("student_dashboard.html")

@app.route('/staffdashboard/<id>')
def staff_dashboard(id):
    if auth.UserAuthoriser.check_permission("staff", id) == False:
        return redirect(url_for('invalid_permission'))

    return render_template("staff_dashboard.html", surveys=modelcontrollers.UserController.get_staff_survey(id))

@app.route('/invalid_permission')
def invalid_permission():
    return render_template("invalid_permissions.html")
