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
from app.activities.services import activitiesServices

# Define the blueprint: 'auth', set its url prefix: app.url/auth
activities = Blueprint('activities', __name__, url_prefix='/activities', template_folder='templates')
cookie_jar = config.COOKIE_VALUE

# Set language variable
lang = {}
lang = getattr(language, config.DEFAULT_LANG)

# Set the route and accepted methods
@activities.route('/', methods=['GET', 'POST'])
def activities_page():
    try:
        print("In activities")
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

        svc = activitiesServices(session_details)

        if request.method == 'POST':
            print("In POST")
            data = svc.getAllactivities(request.form.to_dict())
            #return jsonify(**data)
            return json.dumps({'code':'00', 'data':data})

        data = svc.getAllactivities({'page': 1, 'fromdate': '', 'todate': '', 'status': '', 'branch': '', 'destination': '', 'tag': '', 'type': ''})

        print(data)

        user_lang = lang

        if "lang" in session_details:
            user_lang = getattr(language, session_details['lang'])

        # print(user_lang)

        return render_template("activities/activities.html", lang=user_lang, mStyle=language.STYLE['trans_style'], userdata=session_details, data=data)
    except TemplateNotFound as e:
        raise e


# Set the route and accepted methods
@activities.route('/search', methods=['GET', 'POST'])
def activities_serach():
    try:
        print("In activities search")
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

        svc = activitiesServices(session_details)

        if request.method == 'POST':
            print("In POST")
            data = svc.searchactivities(request.form.to_dict())
            #return jsonify(**data)
            return json.dumps([data])

        data = svc.getAllactivities({ 'page': 1, 'fromdate': "", 'todate': "", 'status': ""})

        print(data)

        user_lang = lang

        if "lang" in session_details:
            user_lang = getattr(language, session_details['lang'])

        print(user_lang)

        return render_template("activities/activities.html", lang=user_lang, mStyle=language.STYLE['trans_style'], userdata=session_details, data=data)
    except TemplateNotFound as e:
        raise e


# Set the route and accepted methods
@activities.route('/export', methods=['GET', 'POST'])
def transaction_export():
    try:
        print("In Transaction Export")
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

        svc = activitiesServices(session_details)

        if request.method == 'GET':
            print("In GET")
            print(request.args.to_dict())
            data = svc.getAllactivitiesExport(request.args.to_dict())
            print(data)

            response_data = excel.make_response_from_array(data, "xls")
        
            response = make_response(response_data) 

            response.headers['Content-Disposition'] = 'attachment; filename=BulkPay_activities.xls'
            response.headers['Content-Type'] = 'application/xls'
            
            return response

    except TemplateNotFound as e:
        raise e


# Set the route and accepted methods
@activities.route('/filteroptions', methods=['GET', 'POST'])
def activities_filter():
    try:
        print("In activities filter")
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

        svc = activitiesServices(session_details)

        print("In POST")
        data = svc.getactivitiesfilter()
        print(data)
        #return jsonify(**data)
        return json.dumps(data)

    except TemplateNotFound as e:
        raise e