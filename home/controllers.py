# Import flask dependencies
from flask import Blueprint
from flask import request
from flask import render_template
from flask import abort              
from flask import flash
from flask import g
from flask import session
from flask import redirect
from flask import url_for
from flask import jsonify
from flask import make_response
from jinja2 import TemplateNotFound
import datetime

# Importing Project dependencies
from app import config
from app import language
from app.libs.decorators import AccessLogger
from app.home.services import DashboardServices
from app.libs.logger import Logger

# Define the account blueprint object
home = Blueprint('home', __name__, url_prefix='/home', template_folder='templates')

# Set language variable
lang = {}
lang = getattr(language, config.DEFAULT_LANG)

# Initiate logger an decorators
log = Logger()
log_access = AccessLogger()

# Set the route and accepted methods
@home.route('/', methods=['GET', 'POST'])
@log_access.log_request
def home_page():
    try:
        print("In login page")
        # access session data (session['k']=v)
        try:
            cookie_id = request.cookies.get('{0}'.format(config.COOKIE_VALUE))  # GET previous cookies
        except Exception as e:
            cookie_id = None

        # if cookie_id != None:
        #     session_details = session['{0}'.format(cookie_id)]
        #     print("Session Data")
        #     print(session_details)
        # else:
        #     session_details = {}



        # svc = adminServices(session_details)
        # result = svc.adminSignout(request_data)

        response = make_response(render_template("home/index.html"))
        if cookie_id != None:
            session.pop(cookie_id, None)  # Clear existing session data
            response.set_cookie('{0}'.format(config.COOKIE_VALUE), '', expires=0)  # Expire existing cookie data
        return response
    except TemplateNotFound as e:
        raise e

@home.route('/new_user', methods=['GET', 'POST'])
def user_change_pass():
    try:
        print("In new user change password")
        # access session data (session['k']=v)
        try:
            cookie_id = request.cookies.get('{0}'.format(config.COOKIE_VALUE))
        except Exception as e:
            cookie_id = None

        if cookie_id != None:
            session_details = session['{0}'.format(cookie_id)]
            print("Session Data")
            print(session_details)
        else:
            return redirect(url_for("home.home_page"))

        user_lang = lang

        if "lang" in session_details:
            user_lang = getattr(language, session_details['lang'])

        print(user_lang)

        return render_template("home/change_pass.html", lang=user_lang, mStyle=language.STYLE['home_style'], userdata=session_details)
    except TemplateNotFound as e:
        raise e


@home.route('/expired_pass', methods=['GET', 'POST'])
def user_change_pass_monthly():
    try:
        print("In monthly change password")
        # access session data (session['k']=v)
        try:
            cookie_id = request.cookies.get('{0}'.format(config.COOKIE_VALUE))
        except Exception as e:
            cookie_id = None

        if cookie_id != None:
            session_details = session['{0}'.format(cookie_id)]
            print("Session Data")
            print(session_details)
        else:
            return redirect(url_for("home.home_page"))

        user_lang = lang

        if "lang" in session_details:
            user_lang = getattr(language, session_details['lang'])

        print(user_lang)

        return render_template("home/month_pass.html", lang=user_lang, mStyle=language.STYLE['home_style'], userdata=session_details)
    except TemplateNotFound as e:
        raise e


@home.route('/user', methods=['GET', 'POST'])
def user_home_page():
    try:
        print("In user home") 
        # access session data (session['k']=v)
        try:
            cookie_id = request.cookies.get('{0}'.format(config.COOKIE_VALUE))
        except Exception as e:
            cookie_id = None

        if cookie_id != None:
            session_details = session['{0}'.format(cookie_id)]
            print("Session Data")
            print(session_details)
        else:
            return redirect(url_for("home.home_page"))

        # if session_details['pass_date'] == None:
        #     return redirect(url_for("home.user_change_pass"))

        # today_date = datetime.datetime.now()
        # days_diff = today_date - session_details['pass_date']
        # print(days_diff.days)
        # if session_details['pass_date'] == None:
        #     return redirect(url_for("home.user_change_pass"))
        # elif days_diff.days > 30:
        #     return redirect(url_for("home.user_change_pass_monthly"))
        #GET STATISTICS
        svc = DashboardServices(session_details)
        statistic = svc.getValidationInfo()
        verification_report = svc.generateSerialsReport({"get_chart": "gen_public"})
        validation_report = svc.generateSerialsReport({"get_chart": "validator"})
        user_lang = lang

        if "lang" in session_details:
            user_lang = getattr(language, session_details['lang'])

        print(user_lang)

        return render_template("home/home.html", lang=user_lang, mStyle=language.STYLE['home_style'], verification_report = verification_report, validation_report=validation_report, userdata=session_details, statistic=statistic)
    except TemplateNotFound as e:
        raise e

@home.route('/report', methods=['GET', 'POST'])
def user_report_page():
    try:
        print("In report route") 
        try:
            cookie_id = request.cookies.get('{0}'.format(config.COOKIE_VALUE))
        except Exception as e:
            cookie_id = None

        if cookie_id != None:
            session_details = session['{0}'.format(cookie_id)]
            print("Session Data")
            print(session_details)
        else:
            return redirect(url_for("home.home_page"))
        
        #check for POST requests
        if request.method == 'POST':
            svc = DashboardServices(session_details)
            report = svc.generateSerialsReport(request.form.to_dict())
            print(report)
            return jsonify(report)
        else:
            svc = DashboardServices(session_details)
            report = svc.generateSerialsReport({})
            print(report)
            return jsonify(report)

    except TemplateNotFound as e:
        raise e
