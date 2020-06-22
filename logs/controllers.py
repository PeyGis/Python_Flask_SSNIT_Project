# Import flask dependencies
from flask import Blueprint, request, render_template, abort, \
                  flash, g, session, redirect, url_for, jsonify, send_file, make_response
import flask_excel as excel
import pyexcel_xls
from jinja2 import TemplateNotFound
# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash
# EXPLAIN_TEMPLATE_LOADING
# Import the database object from the main app module
#from app import db
from math import cos
import json
from app import config
from app import language
from app.logs.services import logServices


# Define the blueprint: 'auth', set its url prefix: app.url/auth
logs = Blueprint('logs', __name__, url_prefix='/logs', template_folder='templates')
cookie_jar = config.COOKIE_VALUE

# Set language variable
lang = {}
lang = getattr(language, config.DEFAULT_LANG)

# Set the route and accepted methods
@logs.route('/', methods=['GET', 'POST'])
def logs_page():
    try:
        print("In Transactions")
        # access session data (session['k']=v)
        try:
            cookie_id = request.cookies.get('{0}'.format(cookie_jar))
        except Exceptionsvc as e:
            cookie_id = None

        if cookie_id != None:
            session_details = session['{0}'.format(cookie_id)]
            print("Session Data")
            print(session_details)
        else:
            return redirect(url_for("home.home_page"))

        svc = logServices(session_details)

        user_lang = lang

        if "lang" in session_details:
            user_lang = getattr(language, session_details['lang'])

        # print(user_lang)

        return render_template("logs/logs.html", lang=user_lang, mStyle=language.STYLE['logs_style'], userdata=session_details, data="")
    except TemplateNotFound as e:
        raise e


# Set the route and accepted methods
@logs.route('/<log_type>/<log_date>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def logs_get_data(log_type, log_date):
    try:
        print("In get log data")
        # access session data (session['k']=v)
        try:
            cookie_id = request.cookies.get('{0}'.format(cookie_jar))
        except Exception as e:
            cookie_id = None

        if cookie_id != None:
            session_details = session['{0}'.format(cookie_id)]
            print("Session Data")
            print(session_details)
        else:
            return redirect(url_for("home.home_page"))

        svc = logServices(session_details)
        data = svc.getLogData(log_type, log_date)
        print(data)

        if request.method == "GET":
            return data

        user_lang = lang

        if "lang" in session_details:
            user_lang = getattr(language, session_details['lang'])

        # print(user_lang)

        return render_template("logs/logs.html", lang=user_lang, mStyle=language.STYLE['logs_style'], userdata=session_details, data=data)
    except TemplateNotFound as e:
        raise e


# Set the route and accepted methods
@logs.route('/export/<log_type>/<log_date>', methods=['GET', 'POST'])
def logs_export(log_type, log_date):
    try:
        print("In Log Export")
        # access session data (session['k']=v)
        try:
            cookie_id = request.cookies.get('{0}'.format(cookie_jar))
        except Exception as e:
            cookie_id = None

        if cookie_id != None:
            session_details = session['{0}'.format(cookie_id)]
            print("Session Data")
            print(session_details)
        else:
            return redirect(url_for("home.home_page"))

        svc = logServices(session_details)

        if request.method == 'GET':
            print("In GET")
            print(request.args.to_dict())
            data = svc.getLogData(log_type, log_date)
            print(data)
        
            response = make_response(data) 

            response.headers['Content-Disposition'] = 'attachment; filename=SICLIFE.txt'
            response.headers['Content-Type'] = 'application/text'
            
            return response

    except TemplateNotFound as e:
        raise e
