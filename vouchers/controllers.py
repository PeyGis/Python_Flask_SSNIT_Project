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
from math import cos, ceil
import uuid
import json

from app import config
from app import language
from app.vouchers.services import vouchersServices

# Define the blueprint: 'auth', set its url prefix: app.url/auth
vouchers = Blueprint('vouchers', __name__, url_prefix='/vouchers', template_folder='templates')
#auth  = decorators.SessionAuth()
cookie_jar = config.COOKIE_VALUE

# Set language variable
lang = {}
lang = getattr(language, config.DEFAULT_LANG)


# Set the route and accepted methods
#@auth.requires_session
@vouchers.route('/', methods=['GET', 'POST'])
def vouchers_page():
    try:
        print("In vouchers")
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

        svc = vouchersServices(session_details)

        if request.method == 'POST':
            print("In POST")
            data = svc.getAllVouchers(request.form.to_dict())
            #return jsonify(**data)
            return json.dumps(data)

        data = svc.getAllVouchers({ 'page': 0, 'fromdate': "", 'todate': ""})
        uploads_data = svc.getAllUploadsRequests({ 'page': 0, 'fromdate': "", 'todate': ""})
        history = svc.getVerificationHistory({'page': 0, 'fromdate': "", 'todate': "", "status": "All"})
        length = history["pages"]

        print("length is ", str(length))
        
        user_lang = lang

        if "lang" in session_details:
            user_lang = getattr(language, session_details['lang'])


        return render_template("vouchers/vouchers.html", length = length, lang=user_lang, mStyle=language.STYLE['mer_style'], userdata=session_details, data=data, up_data=uploads_data, history=history)
    except TemplateNotFound as e:
        raise e

# Set the route and accepted methods
#@auth.requires_session
@vouchers.route('/<bulk_id>', methods=['GET', 'POST'])
def vouchers_page_detatils(bulk_id):
    try:
        print("In vouchers")
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

        svc = vouchersServices(session_details)

        if request.method == 'POST':
            print("In POST")
            data = svc.getVoucherByBulkId(bulk_id, request.form.to_dict())
            return jsonify(data)

        data = svc.getVoucherByBulkId(bulk_id, {'page': 0, 'serial_status': "", 'branch_assigned': ""})

        print(data)
        
        user_lang = lang

        if "lang" in session_details:
            user_lang = getattr(language, session_details['lang'])

        return render_template("vouchers/vouchers_detail.html", lang=user_lang, mStyle=language.STYLE['mer_style'], userdata=session_details, data=data, bulkId = bulk_id)
    except TemplateNotFound as e:
        raise e


#bulk assign serials to branch
@vouchers.route('/assign', methods=['GET', 'POST'])
def assign_branch():
    try:
        # access session data (session['k']=v)
        print("In assign route")
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

        svc = vouchersServices(session_details)

        if request.method == 'POST':
            result = svc.updateBulkAssignSerialBranch(request.form.to_dict())
            print(result)
            return jsonify(result)
            
        else:
            return redirect(url_for("home.home_page"))
        
    except TemplateNotFound as e:
        raise e

#serial verification route
@vouchers.route('/verification', methods=['GET', 'POST'])
def serial_verification():
    try:
        # access session data (session['k']=v)
        print("In serial verification route")
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

        svc = vouchersServices(session_details)

        if request.method == 'POST':
            result = svc.getVerificationHistory(request.form.to_dict())
            print(result)
            return jsonify(result)
            
        else:
            return redirect(url_for("home.home_page"))
        
    except TemplateNotFound as e:
        raise e

# Set the route and accepted methods
@vouchers.route('/export', methods=['GET', 'POST'])
def vouchers_export():
    try:
        print("In Vouchers Export")
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

        svc = vouchersServices(session_details)

        if request.method == 'GET':
            print("In GET")
            print(request.args.to_dict())
            data = svc.getAllvouchersExport(request.args.to_dict())
            print(data)

            response_data = excel.make_response_from_array(data, "xls")
        
            response = make_response(response_data) 

            response.headers['Content-Disposition'] = 'attachment; filename=siclife_vouchers.xls'
            response.headers['Content-Type'] = 'application/xls'
            
            return response

    except TemplateNotFound as e:
        raise e


@vouchers.route('/add', methods=['GET', 'POST'])
def vouchers_add():
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

        svc = vouchersServices(session_details)

        if request.method == 'POST':
            print("In POST")
            data = svc.addCustomer(request.form.to_dict())
            return json.dumps(data)

        else:
            return json.dumps(code="01", msg="Wrong method used.")

    except TemplateNotFound as e:
        raise e


@vouchers.route('/update', methods=['GET', 'POST'])
def vouchers_update():
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

        svc = vouchersServices(session_details)

        if request.method == 'POST':
            print("In POST")
            data = svc.updateCustomer(request.form.to_dict())
            return json.dumps(data)

        else:
            return json.dumps(code="01", msg="Wrong method used.")

    except TemplateNotFound as e:
        raise e


@vouchers.route('/validate', methods=['GET', 'POST'])
def vouchers_details():
    try:
        print("In verify")
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

        svc = vouchersServices(session_details)

        if request.method == 'POST':
            print("In POST")
            data = svc.getVoucherDetials(request.form.to_dict())
            # print(data)
            return jsonify(data)

        else:
            return json.dumps(code="01", msg="Wrong method used.")

    except TemplateNotFound as e:
        raise e

@vouchers.route('/verify/search', methods=['GET', 'POST'])
def vouchers_verify_search():
    try:
        print("In search verify")
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

        svc = vouchersServices(session_details)

        if request.method == 'POST':
            print("In POST")
            data = svc.searchVerifiedVouchers(request.form.to_dict())
            # print(data)
            return jsonify(data)

        else:
            return json.dumps(code="01", msg="Wrong method used.")

    except TemplateNotFound as e:
        raise e   

#process first time validation
@vouchers.route('/verify', methods=['GET','POST'])
def check_vouch():
    if request.method == 'POST':
        request_data = request.form.to_dict()
        svc = vouchersServices({})
        data = svc.getSerialDetialsValidate(request_data)
        print(data)
        return jsonify(data)
        
    else:
        return json.dumps({"error": "invalid request sent"})

@vouchers.route('/verify/customer', methods=['GET', 'POST'])
def vouchers_customer_details():
    try:
        print("In verify")
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

        svc = vouchersServices(session_details)

        if request.method == 'POST':
            print("In POST")
            req_data = request.form.to_dict()
            data = svc.getVoucherDetialsValidate(request.form.to_dict())
            print(data)
            return json.dumps(data)

        else:
            return json.dumps(code="01", msg="Wrong method used.")

    except TemplateNotFound as e:
        raise e

@vouchers.route('/use', methods=['GET', 'POST'])
def vouchers_use():
    try:
        print("In use voucher")
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

        svc = vouchersServices(session_details)

        if request.method == 'POST':
            print("In POST")
            data = svc.useVoucher(request.form.to_dict())
            print(data)
            return json.dumps(data)

        else:
            return json.dumps(code="01", msg="Wrong method used.")

    except TemplateNotFound as e:
        raise e

@vouchers.route('/search', methods=['GET', 'POST'])
def vouchers_search():
    try:

        print("In vouchers search")
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

        svc = vouchersServices(session_details)
        result = svc.searchvouchers(request_data)

        return json.dumps(result)
    except TemplateNotFound as e:
        raise e


# Set the route and accepted methods
@vouchers.route('/record', methods=['GET', 'POST'])
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
            # data = request.form.to_dict()
            # print("Data")
            # print(data)
            # file_obl = request.files['file']
            # print("File")
            # print(file_obl.filename)

            #check if request has file object
            if 'file' not in request.files:
                return redirect(url_for("vouchers.vouchers_page"))
            file_obl = request.files['file']
            #if user submit empty form part without filename
            if file_obl.filename == '':
                return redirect(url_for("vouchers.vouchers_page"))

            svc = vouchersServices(session_details)
            data = svc.record_uploaded_file(file_obl)

            return redirect(url_for("vouchers.vouchers_page"))

    except TemplateNotFound as e:
        raise e

# Set the route and accepted methods
@vouchers.route('/uploads/approve', methods=['GET', 'POST'])
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

            svc = vouchersServices(session_details)
            data = svc.approve_uploaded_file(request.form.to_dict())

            return json.dumps(data)

    except TemplateNotFound as e:
        raise e


# Set the route and accepted methods
@vouchers.route('/uploads/decline', methods=['GET', 'POST'])
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

            svc = vouchersServices(session_details)
            data = svc.decline_uploaded_file(request.form.to_dict())

            return json.dumps(data)

    except TemplateNotFound as e:
        raise e

# Set the route and accepted methods
#@auth.requires_session
@vouchers.route('/uploads', methods=['GET', 'POST'])
def vouchers_reg_uploads():
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

        svc = vouchersServices(session_details)

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

        return render_template("vouchers/vouchers.html", lang=user_lang, mStyle=language.STYLE['mer_style'], userdata=session_details, data=data, req_data=request_data, up_data=uploads_data)
    except TemplateNotFound as e:
        raise e
