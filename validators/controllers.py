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
from flask import send_file
import flask_excel as excel
import pyexcel_xls
from jinja2 import TemplateNotFound

# Import standard lib dependencies
import uuid
import json
import datetime

# Import project dependencies
from app import config
from app import language
from app.validators.services import validatorServices
from app.libs.decorators import AccessLogger
from app.libs.logger import Logger

# Define the admin blueprint object
validators = Blueprint('validators', __name__, url_prefix='/validators', template_folder='templates')

# Set language variable
lang = {}
lang = getattr(language, config.DEFAULT_LANG)

# Initiate logger an decorators
log = Logger()
log_access = AccessLogger()

# Set the route and accepted methods for admin
@validators.route('/', methods=['GET', 'POST'])
@log_access.log_request
def validators_page():
    try:
        log.write_to_console(msg="In Validators Route")
        try:
            cookie_id = request.cookies.get('{0}'.format(config.COOKIE_VALUE))
        except Exception as e:
            cookie_id = None

        if cookie_id != None:
            session_details = session['{0}'.format(cookie_id)]
            log.write_to_console(msg="Account-User-Session: {}".format(session_details))
        else:
            log.write_to_console(msg="Account-User-Session: No session Redirecting")
            return redirect(url_for("home.home_page"))

        svc = validatorServices(session_details)
        log.write_to_console(msg="Calling service: getAllValidators()")

        if request.method == 'POST':
            data = svc.getAllValidators(request.form.to_dict())
            log.write_to_console(msg="Returning POST Response: getAllValidators")
            return jsonify(**data)

        data = svc.getAllValidators({'page': 0, 'branch': 'None'})
        history = svc.getValidatorsHistory({'page': 0, 'fromdate': "", 'todate': "", "user_branch": "Non"})
        print(data)
        user_lang = lang

        if "lang" in session_details:
            user_lang = getattr(language, session_details['lang'])

        log.write_to_console(msg="Returning GET Response: getAllValidators -> Rendering Page: validators/validator.html")
        return render_template("validators/validators.html", lang=user_lang,  mStyle=language.STYLE['validators_style'], userdata=session_details, data=data, history=history)
    except TemplateNotFound as e:
        log.write_log("ERROR", msg="Account: {}".format(e))
        return render_template('404.html'), 404
    except Exception as ee:
        log.write_log("ERROR", msg="Account: {}".format(ee))
        # raise ee
        return render_template('500.html'), 500


@validators.route('/add', methods=['GET', 'POST'])
@log_access.log_request
def validators_add():
    try:

        print("In Validator Add")
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

        print(session_details)

        request_data = request.form.to_dict()

        svc = validatorServices(session_details)
        result = svc.addValidator(request_data)

        return jsonify(**result)
    except TemplateNotFound as e:
        raise e

@validators.route('/delete', methods=['GET', 'POST'])
@log_access.log_request
def validators_delete():
    try:

        print("In Validator delete")
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

        print(session_details)

        if request.method == 'POST':

            request_data = request.form.to_dict()
            print(request_data)
            svc = validatorServices(session_details)
            result = svc.deleteValidator(request_data)
            print(result)
            return jsonify(**result)
        else:
            return jsonify({"mesaage": "invalid request"})

    except TemplateNotFound as e:
        raise e

@validators.route('/getValidator', methods=['GET', 'POST'])
@log_access.log_request
def validators_get():
    try:

        print("In Validator getone")
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

        print(session_details)

        request_data = request.form.to_dict()

        svc = validatorServices(session_details)
        result = svc.getValidatorDetails(request_data)

        return jsonify(**result)
    except TemplateNotFound as e:
        raise e


@validators.route('/search', methods=['GET', 'POST'])
@log_access.log_request
def admins_search():
    try:

        print("In Admin getone")
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

        print(session_details)

        request_data = request.form.to_dict()

        svc = adminServices(session_details)
        result = svc.searchAdmins(request_data)

        return json.dumps(result)
    except TemplateNotFound as e:
        raise e


@validators.route('/update', methods=['GET', 'POST'])
@log_access.log_request
def admins_update():
    try:

        print("In validator update")
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

        print(session_details)

        request_data = request.form.to_dict()

        svc = validatorServices(session_details)
        result = svc.updateValidator(request_data)

        return jsonify(result)
    except TemplateNotFound as e:
        raise e

@validators.route('/validations', methods=['GET', 'POST'])
@log_access.log_request
def serial_validations():
    try:

        print("In Validation History ")
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

        print(session_details)

        if request.method == 'POST':

            svc = validatorServices(session_details)
            result = svc.getValidatorsHistory(request.form.to_dict())
            print(result)
            return jsonify(**result)
        else:
            return jsonify({"mesaage": "invalid request sent"})

    except TemplateNotFound as e:
        raise e

@validators.route('/validation/search', methods=['GET', 'POST'])
def validation_history_search():
    try:
        print("In search validation")
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
            session_details = {}

        svc = validatorServices(session_details)

        if request.method == 'POST':
            print("In POST")
            data = svc.searchValidatoinHistory(request.form.to_dict())
            # print(data)
            return jsonify(data)

        else:
            return json.dumps(code="01", msg="Wrong method used.")

    except TemplateNotFound as e:
        raise e 
