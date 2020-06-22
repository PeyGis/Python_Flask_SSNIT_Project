# Import flask dependencies
from flask import Blueprint, request, render_template, abort, \
                  flash, g, session, redirect, url_for, jsonify, make_response, send_file, make_response
import flask_excel as excel
import pyexcel_xls
from jinja2 import TemplateNotFound
# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash
# EXPLAIN_TEMPLATE_LOADING
# Import the database object from the main app module
#from app import db
from math import cos
import uuid
import json

from app import config
from app import language
from app.activities.services import activitiesServices

# Define the blueprint: 'auth', set its url prefix: app.url/auth
activities = Blueprint('activities', __name__, url_prefix='/activities', template_folder='templates')
#auth  = decorators.SessionAuth()
cookie_jar = config.COOKIE_VALUE

# Set language variable
lang = {}
lang = getattr(language, config.DEFAULT_LANG)


# Set the route and accepted methods
#@auth.requires_session
@activities.route('/', methods=['GET', 'POST'])
def activities_page():
    try:
        print("In bulkpay")
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
            data = svc.getAllActivities(request.form.to_dict())
            #return jsonify(**data)
            return json.dumps(data)

        data = svc.getAllActivities({ 'page': 0, 'fromdate': "", 'todate': ""})
        blacklist_data = svc.getAllBlacklist({ 'page': 0, 'fromdate': "", 'todate': ""})

        print(data)
        
        user_lang = lang

        if "lang" in session_details:
            user_lang = getattr(language, session_details['lang'])


        return render_template("activities/activities.html", lang=user_lang, mStyle=language.STYLE['trans_style'], userdata=session_details, data=data, blacklist_data=blacklist_data)
    except TemplateNotFound as e:
        raise e


# Set the route and accepted methods
@activities.route('/export', methods=['GET', 'POST'])
def activities_export():
    try:
        print("In bulkpay")
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

            response.headers['Content-Disposition'] = 'attachment; filename=siclife_activities.xls'
            response.headers['Content-Type'] = 'application/xls'
            
            return response

    except TemplateNotFound as e:
        raise e


@activities.route('/add', methods=['GET', 'POST'])
def activities_add():
    try:
        print("In bulkpay Add")
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
            data = svc.addCustomer(request.form.to_dict())
            return json.dumps(data)

        else:
            return json.dumps(code="01", msg="Wrong method used.")

    except TemplateNotFound as e:
        raise e


@activities.route('/update', methods=['GET', 'POST'])
def activities_update():
    try:
        print("In bulkpay Add")
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
            data = svc.updateCustomer(request.form.to_dict())
            return json.dumps(data)

        else:
            return json.dumps(code="01", msg="Wrong method used.")

    except TemplateNotFound as e:
        raise e


@activities.route('/request/details', methods=['GET', 'POST'])
def activities_request_details():
    try:
        print("In Customer Details")
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
            data = svc.getCustomerReqDetails(request.form.to_dict())
            print(data)
            return json.dumps(data)

        else:
            return json.dumps(code="01", msg="Wrong method used.")

    except TemplateNotFound as e:
        raise e


@activities.route('/details', methods=['GET', 'POST'])
def activities_details():
    try:
        print("In Customer Details")
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
            data = svc.getUserActivities(request.form.to_dict())
            print(data)
            return json.dumps(data)

        else:
            return json.dumps(code="01", msg="Wrong method used.")

    except TemplateNotFound as e:
        raise e

@activities.route('/details/<customer_id>', methods=['GET', 'POST'])
def activities_all_details(customer_id):
    try:
        print("In Customer All Details")
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
            data = svc.getUserActivities(customer_id)
            print(data)
            return json.dumps(data)

        data = svc.getUserActivities(customer_id)

        print(data)

        user_lang = lang

        if "lang" in session_details:
            user_lang = getattr(language, session_details['lang'])

        # print(user_lang)

        return render_template("activities/activities_detials.html", lang=user_lang, mStyle=language.STYLE['trans_style'], userdata=session_details, data=data)

    except TemplateNotFound as e:
        raise e


@activities.route('/block_customer', methods=['GET', 'POST'])
def activities_block():
    try:
        print("In Block Customer")
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
            data = svc.blockCustomerRequest(request.form.to_dict())
            print(data)
            return json.dumps(data)

        return {'code': '00', 'msg': 'Wrong method used'}

    except TemplateNotFound as e:
        raise e


@activities.route('/enable_customer', methods=['GET', 'POST'])
def activities_enable():
    try:
        print("In Enable Customer")
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
            data = svc.enableCustomerRequest(request.form.to_dict())
            print(data)
            return json.dumps(data)

        return {'code': '00', 'msg': 'Wrong method used'}

    except TemplateNotFound as e:
        raise e


@activities.route('/reset_pin', methods=['GET', 'POST'])
def activities_reset_pin_request():
    try:
        print("In Block Customer")
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
            data = svc.resetPinRequest(request.form.to_dict())
            print(data)
            return json.dumps(data)

        return {'code': '00', 'msg': 'Wrong method used'}

    except TemplateNotFound as e:
        raise e


@activities.route('/deactivate_customer_account', methods=['GET', 'POST'])
def deactivate_activities_account():
    try:
        print("In Deactivate Customer Account")
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
            data = svc.deactivateCustomerAccountRequest(request.form.to_dict())
            print(data)
            return json.dumps(data)

        return {'code': '00', 'msg': 'Wrong method used'}

    except TemplateNotFound as e:
        raise e


@activities.route('/activate_customer_account', methods=['GET', 'POST'])
def activate_activities_account():
    try:
        print("In Activate Customer Account")
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
            data = svc.activateCustomerAccountRequest(request.form.to_dict())
            print(data)
            return json.dumps(data)

        return {'code': '00', 'msg': 'Wrong method used'}

    except TemplateNotFound as e:
        raise e


@activities.route('/add_customer_account', methods=['GET', 'POST'])
def add_customer_account():
    try:
        print("In Add Customer Account")
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
            data = svc.addCustomerAccountRequest(request.form.to_dict())
            print(data)
            return json.dumps(data)

        return {'code': '00', 'msg': 'Wrong method used'}

    except TemplateNotFound as e:
        raise e


@activities.route('/approve_customer_request', methods=['GET', 'POST'])
def approve_customer_requests():
    try:
        print("In Approve Customer Request")
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
            data = svc.approveCustomerRequest(request.form.to_dict())
            print(data)
            return json.dumps(data)

        return {'code': '00', 'msg': 'Wrong method used'}

    except TemplateNotFound as e:
        raise e


@activities.route('/decline_customer_request', methods=['GET', 'POST'])
def decline_customer_requests():
    try:
        print("In Decline Customer Request")
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
            data = svc.declineCustomerRequest(request.form.to_dict())
            print(data)
            return json.dumps(data)

        return {'code': '00', 'msg': 'Wrong method used'}

    except TemplateNotFound as e:
        raise e


@activities.route('/search', methods=['GET', 'POST'])
def activities_search():
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

        print(session_details)

        request_data = request.form.to_dict()

        svc = activitiesServices(session_details)
        result = svc.searchactivities(request_data)

        return json.dumps(result)
    except TemplateNotFound as e:
        raise e


# Set the route and accepted methods
@activities.route('/record', methods=['GET', 'POST'])
def uploads_upload():
    try:
        print("In uploads")
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

        if request.method == 'POST':
            data = request.form.to_dict()
            print("Data")
            print(data)
            file_obl = request.files['file']
            print("File")
            print(file_obl.filename)

            svc = activitiesServices(session_details)
            data = svc.record_uploaded_file(file_obl)

            return redirect(url_for("activities.activities_page"))

    except TemplateNotFound as e:
        raise e

# Set the route and accepted methods
@activities.route('/uploads/approve', methods=['GET', 'POST'])
def uploads_approve():
    try:
        print("In uploads")
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

        if request.method == 'POST':

            svc = activitiesServices(session_details)
            data = svc.approve_uploaded_file(request.form.to_dict())

            return json.dumps(data)

    except TemplateNotFound as e:
        raise e


# Set the route and accepted methods
@activities.route('/uploads/decline', methods=['GET', 'POST'])
def uploads_decline():
    try:
        print("In uploads")
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

        if request.method == 'POST':

            svc = activitiesServices(session_details)
            data = svc.decline_uploaded_file(request.form.to_dict())

            return json.dumps(data)

    except TemplateNotFound as e:
        raise e

# Set the route and accepted methods
#@auth.requires_session
@activities.route('/uploads', methods=['GET', 'POST'])
def activities_reg_uploads():
    try:
        print("In Customer uploads")
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
            data = svc.getAllUploadsRequests(request.form.to_dict())
            #return jsonify(**data)
            return json.dumps(data)

        data = svc.getAllUploadsRequests({ 'page': 0, 'fromdate': "", 'todate': ""})
        request_data = svc.getAllCustomerRequests({ 'page': 0, 'fromdate': "", 'todate': "", "branch":"", "request_type":""})
        uploads_data = svc.getAllUploadsRequests({ 'page': 0, 'fromdate': "", 'todate': ""})

        print(data)
        print()
        print(request_data)

        user_lang = lang

        if "lang" in session_details:
            user_lang = getattr(language, session_details['lang'])

        # print(user_lang)

        return render_template("activities/activities.html", lang=user_lang, mStyle=language.STYLE['mer_style'], userdata=session_details, data=data, req_data=request_data, up_data=uploads_data)
    except TemplateNotFound as e:
        raise e


# Set the route and accepted methods
#@auth.requires_session
@activities.route('/requests', methods=['GET', 'POST'])
def activities_requests():
    try:
        print("In Customer uploads")
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
            data = svc.getAllCustomerRequests(request.form.to_dict())
            #return jsonify(**data)
            return json.dumps(data)

        data = svc.getAllUploadsRequests({ 'page': 0, 'fromdate': "", 'todate': ""})
        request_data = svc.getAllCustomerRequests({ 'page': 0, 'fromdate': "", 'todate': "", "branch":"", "request_type":""})
        uploads_data = svc.getAllUploadsRequests({ 'page': 0, 'fromdate': "", 'todate': ""})

        print(data)
        print()
        print(request_data)

        user_lang = lang

        if "lang" in session_details:
            user_lang = getattr(language, session_details['lang'])

        # print(user_lang)

        return render_template("activities/activities.html", lang=user_lang, mStyle=language.STYLE['mer_style'], userdata=session_details, data=data, req_data=request_data, up_data=uploads_data)
    except TemplateNotFound as e:
        raise e

@activities.route('/requests/search', methods=['GET', 'POST'])
def activities_req_search():
    try:

        print("In activities request search")
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

        print(session_details)

        request_data = request.form.to_dict()

        svc = activitiesServices(session_details)
        result = svc.searchactivitiesRequests(request_data)

        return json.dumps(result)
    except TemplateNotFound as e:
        raise e
