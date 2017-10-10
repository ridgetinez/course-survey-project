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
        if request.method == 'POST':
            if "close" in request.form:
                survey_list = request.form['close'].split(" ")
                modelcontrollers.SurveyController.close_survey(survey_list[0], survey_list[1])
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

    if request.method == 'POST':
        #catch cancel
        if 'cancel' in request.form:
            return redirect(url_for('admin_dashboard', sub_page='surveys'))
        result = controller.FormController.parse_create_survey(request.form)

        if result[0] == False:
            if result[1] == 'qerror':
                return render_template('admin_dashboard_create_survey.html', questions=modelcontrollers.QuestionController.get_all_questions(), course_list=modelcontrollers.CourseController.get_courses(), selection_error=True)
            if result[1] == 'terror':
                return render_template('admin_dashboard_create_survey.html', questions=modelcontrollers.QuestionController.get_all_questions(), course_list=modelcontrollers.CourseController.get_courses(), time_error=True)
            if result[1] == 'verror':
                return render_template('admin_dashboard_create_survey.html', questions=modelcontrollers.QuestionController.get_all_questions(), course_list=modelcontrollers.CourseController.get_courses(), value_error=True)
            if result[1] == 'rerror':
                return render_template('admin_dashboard_create_survey.html', questions=modelcontrollers.QuestionController.get_all_questions(), course_list=modelcontrollers.CourseController.get_courses(), redo_error=True)


        return redirect(url_for('admin_dashboard', sub_page='surveys'))

    return render_template('admin_dashboard_create_survey.html', questions=modelcontrollers.QuestionController.get_all_questions(), course_list=modelcontrollers.CourseController.get_courses())

@app.route('/survey/respond/<id>', methods=['POST', 'GET'])
def respond(id):
    if auth.UserAuthoriser.check_permission("student", id) == False:
        return redirect(url_for('invalid_permission'))

    if request.method == "POST":
        print(request.form)
        controller.FormController.parse_response(request.form, id)
        return redirect(url_for('student_dashboard', id=id))
    survey_list = session.pop('survey_to_complete').split(" ")
    return render_template("view_survey.html", survey=modelcontrollers.SurveyController.get_survey(survey_list[0], survey_list[1]), questions=modelcontrollers.SurveyController.get_survey_questions(survey_list[0], survey_list[1]))

@app.route('/studentdashboard/<id>', methods=['GET','POST'])
def student_dashboard(id):
    if auth.UserAuthoriser.check_permission("student", id) == False:
        return redirect(url_for('invalid_permission'))

    if request.method == 'POST':
        session['survey_to_complete'] = request.form['respond']
        return redirect(url_for('respond', id=id))
    return render_template("student_dashboard.html", surveys=modelcontrollers.UserController.get_user_survey(id))

@app.route('/staffdashboard/<id>', methods=['GET', 'POST'])
def staff_dashboard(id):
    if auth.UserAuthoriser.check_permission("staff", id) == False:
        return redirect(url_for('invalid_permission'))

    if request.method == 'POST':
        session['survey_to_review'] = request.form['review']
        return redirect(url_for('review_survey', id=id))
    return render_template("staff_dashboard.html", surveys=modelcontrollers.UserController.get_user_survey(id))

@app.route('/staffdashboard/<id>/review', methods=['GET', 'POST'])
def review_survey(id):
    if auth.UserAuthoriser.check_permission("staff", id) == False:
        return redirect(url_for('invalid_permission'))

    if request.method == 'POST':
        if 'accept' in request.form:
            survey_as_list = request.form['accept'].split(" ")
            modelcontrollers.SurveyController.set_survey_active(survey_as_list[0], survey_as_list[1])

            return redirect(url_for('staff_dashboard', id=id))

    try:
        survey = session.pop('survey_to_review')
    except KeyError:
        return redirect(url_for('invalid_permission'))
    survey_as_list = survey.split(" ");
    return render_template("review_survey.html", survey=modelcontrollers.SurveyController.get_survey(survey_as_list[0], survey_as_list[1]), questions=modelcontrollers.SurveyController.get_survey_questions(survey_as_list[0], survey_as_list[1]))

@app.route('/invalid_permission')
def invalid_permission():
    return render_template("invalid_permissions.html")

@app.route('/logout')
def logout():
    try:
        session.pop("user")
    except:
        pass
    return redirect(url_for("index"))
