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
from app.admins.services import adminServices
from app.libs.decorators import AccessLogger
from app.libs.logger import Logger

# Define the admin blueprint object
admins = Blueprint('admins', __name__, url_prefix='/admins', template_folder='templates')

# Set language variable
lang = {}
lang = getattr(language, config.DEFAULT_LANG)

# Initiate logger an decorators
log = Logger()
log_access = AccessLogger()

# Set the route and accepted methods for admin
@admins.route('/', methods=['GET', 'POST'])
@log_access.log_request
def admins_page():
    try:
        log.write_to_console(msg="In Administator Route")
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

        svc = adminServices(session_details)
        log.write_to_console(msg="Calling service: getAllAdministrators()")

        if request.method == 'POST':
            data = svc.getAllAdministrators(request.form.to_dict())
            log.write_to_console(msg="Returning POST Response: getAllAdministrators")
            return jsonify(**data)

        data = svc.getAllAdministrators({ 'page': 0, 'fromdate': "", 'todate': "", 'user_right_id': '', "branch": '','active': ''})
        user_lang = lang

        if "lang" in session_details:
            user_lang = getattr(language, session_details['lang'])

        log.write_to_console(msg="Returning GET Response: getAllAdministrators -> Rendering Page: admins/admins.html")
        return render_template("admins/admins.html", lang=user_lang,  mStyle=language.STYLE['admins_style'], userdata=session_details, data=data)
    except TemplateNotFound as e:
        log.write_log("ERROR", msg="Account: {}".format(e))
        return render_template('404.html'), 404
    except Exception as ee:
        log.write_log("ERROR", msg="Account: {}".format(ee))
        # raise ee
        return render_template('500.html'), 500


# Set the route and accepted methods
@admins.route('/export', methods=['GET', 'POST'])
@log_access.log_request
def admin_export():
    try:
        log.write_to_console(msg="In Administators Export Route")
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

        svc = adminServices(session_details)

        if request.method == 'GET':
            print("In GET")
            print(request.args.to_dict())
            data = svc.getAllAdministratorsExport(request.args.to_dict())
            print(data)

            response_data = excel.make_response_from_array(data, "xls")
        
            response = make_response(response_data) 

            response.headers['Content-Disposition'] = 'attachment; filename=BulkPay_Admins.xls'
            response.headers['Content-Type'] = 'application/xls'
            
            log.write_to_console(msg="Administrators export don retruning file")
            return response

    except TemplateNotFound as e:
        raise e


@admins.route('/login', methods=['GET', 'POST'])
@log_access.log_request
def admins_login():
    try:

        print("In Admin Login")
        # access session data (session['k']=v)
        # try:
        #     cookie_id = request.cookies.get('{0}'.format(config.COOKIE_VALUE))
        # except Exception as e:
        #     cookie_id = None
        #
        # if cookie_id != None:
        #     session_details = session['{0}'.format(cookie_id)]
        #     print("Session Data")
        #     print(session_details)
        # else:
        session_details = {}
        try_var = None 
        #
        print(session_details)

        request_data = request.form.to_dict()

        if 'trying_{0}'.format(request_data['username']) in session:
            try_var = session['trying_{0}'.format(request_data['username'])]

        svc = adminServices(session_details)
        result = svc.adminlogin(request_data, try_var)

        print(result)

        if result['code'] == '00':
            cookie_value = str(uuid.uuid4()).replace('-','')[:15] # Generate a session token value
            session['{0}'.format(cookie_value)] = dict(result['data'])
            session['trying_{0}'.format(result['username'])] = None
            # Render Response and browser cookie value
            expire_date = datetime.datetime.now()
            expire_date = expire_date + datetime.timedelta(days=1)
            response = make_response(jsonify(**result))
            response.set_cookie('{0}'.format(config.COOKIE_VALUE), cookie_value, expires=expire_date)
            # Return response for successful login
            return response
        elif result['code'] == '01' and result['data'] == 1:
            if 'trying_{0}'.format(result['username']) in session and session['trying_{0}'.format(result['username'])] is not None:
                session['trying_{0}'.format(result['username'])] = session['trying_{0}'.format(result['username'])] + 1
            else:
                session['trying_{0}'.format(result['username'])] = 1
        elif result['code'] == '01' and result['data'] == 2:
            session['trying_{0}'.format(result['username'])] = None

        return jsonify(**result)
    except TemplateNotFound as e:
        raise e


@admins.route('/language', methods=['GET', 'POST'])
@log_access.log_request
def admins_lang():
    try:

        print("In Admin Language")
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

        if request_data['language'] != '' or request_data['language'] != None:
            session_details['lang'] = request_data['language']
            session['{0}'.format(cookie_id)] = session_details
            return jsonify(code="00", msg="Success")
        else:
            return jsonify(code="01", msg="Failed")

    except TemplateNotFound as e:
        raise e


@admins.route('/signout', methods=['GET', 'POST'])
@log_access.log_request
def admins_signout():
    print("In Admin logout")

    try:
        cookie_id = request.cookies.get('{0}'.format(config.COOKIE_VALUE))
    

        if cookie_id != None:
            session_details = session['{0}'.format(cookie_id)]
            svc = adminServices(session_details)
            result = svc.adminLogout()
            log.write_log("USER_ACCESS", "Logout request | "+ session_details['username'] + " | Successful | Logout Successful")
        else:
            # return redirect(url_for("home.home_page"))
            pass

        # cookie_id = request.cookies.get('{0}'.format(config.COOKIE_VALUE)) # GET previous cookies
        # session_details = session['{0}'.format(cookie_id)]
        response = make_response(redirect(url_for("home.home_page")))
        if cookie_id != None:
            session.pop(cookie_id, None)  # Clear existing session data
            response.set_cookie('{0}'.format(config.COOKIE_VALUE), '', expires=0) # Expire existing cookie data

        return response

    except Exception as e:
        response = make_response(redirect(url_for("home.home_page")))
        response.set_cookie('{0}'.format(config.COOKIE_VALUE), '', expires=0) # Expire existing cookie data
        # cookie_id = None
        return response


@admins.route('/add', methods=['GET', 'POST'])
@log_access.log_request
def admins_add():
    try:

        print("In Admin Add")
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
        result = svc.addAdmin(request_data)

        return jsonify(**result)
    except TemplateNotFound as e:
        raise e


@admins.route('/group/add', methods=['GET', 'POST'])
@log_access.log_request
def admins_add_group():
    try:

        print("In Admin Group Add")
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
        result = svc.addAdminGroup(request_data)

        return jsonify(**result)
    except TemplateNotFound as e:
        raise e


@admins.route('/group/update', methods=['GET', 'POST'])
@log_access.log_request
def admins_update_group():
    try:

        print("In Admin Group Update")
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
        result = svc.updateAdminGroup(request_data)

        return jsonify(**result)
    except TemplateNotFound as e:
        raise e


@admins.route('/getadmin', methods=['GET', 'POST'])
@log_access.log_request
def admins_get():
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
        result = svc.getAdmin(request_data)

        return jsonify(**result)
    except TemplateNotFound as e:
        raise e


@admins.route('/search', methods=['GET', 'POST'])
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


@admins.route('/inst_details/', methods=['GET', 'POST'])
@log_access.log_request
def admins_get_inst():
    try:

        print("In Admin inst details")
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
        result = svc.getAdminInstDetails()

        return jsonify(**result)
    except TemplateNotFound as e:
        raise e


@admins.route('/update', methods=['GET', 'POST'])
@log_access.log_request
def admins_update():
    try:

        print("In Admin Add")
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
        result = svc.updateAdmin(request_data)

        return jsonify(result)
    except TemplateNotFound as e:
        raise e


@admins.route('/forgotpass', methods=['GET', 'POST'])
@log_access.log_request
def admins_reset_password():
    try:

        print("In Admin forgot Password")
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
            session_details = {}

        print(session_details)

        request_data = request.form.to_dict()

        svc = adminServices(session_details)
        result = svc.resetAdminPassword(request_data)

        return jsonify(**result)
    except TemplateNotFound as e:
        raise e


@admins.route('/changepassword', methods=['GET', 'POST'])
@log_access.log_request
def admins_change_password():
    try:

        print("In Admin Add")
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
        result = svc.changeAdminPassword(request_data)
        if result['code'] == '00':
            session['{0}'.format(cookie_id)] = dict(result['data'])

        return jsonify(**result)
    except TemplateNotFound as e:
        raise e



@admins.route('/branches', methods=['GET', 'POST'])
@log_access.log_request
def branches_page():
    try:
        log.write_to_console(msg="In Branches Route")
        

        # svc = adminServices(session_details)
        # log.write_to_console(msg="Calling service: getAllBranches()")

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

        svc = adminServices(session_details)

        if request.method == 'POST':
            data = svc.getAllBranches(request.form.to_dict())
            log.write_to_console(msg="Returning POST Response: getBranches()")
            print(data)
            return jsonify(data)

        data = svc.getAllBranches({ 'page': 0})
        user_lang = lang

        if "lang" in session_details:
            user_lang = getattr(language, session_details['lang'])

        log.write_to_console(msg="Returning GET Response: getAllAdministrators -> Rendering Page: admins/admins.html")
        return render_template("admins/admins.html", lang=user_lang,  mStyle=language.STYLE['admins_style'], userdata=session_details, data=data)
    except TemplateNotFound as e:
        log.write_log("ERROR", msg="Account: {}".format(e))
        return render_template('404.html'), 404
    except Exception as ee:
        log.write_log("ERROR", msg="Account: {}".format(ee))
        # raise ee
        return render_template('500.html'), 500


# Set the route and accepted methods
@admins.route('/branches/export', methods=['GET', 'POST'])
@log_access.log_request
def branches_export():
    try:
        log.write_to_console(msg="In Branches Export Route")
        
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

        svc = adminServices(session_details)

        if request.method == 'GET':
            print("In GET")
            data = svc.getAllBranchesExport()
            print(data)

            response_data = excel.make_response_from_array(data, "csv")
        
            response = make_response(response_data) 

            response.headers['Content-Disposition'] = 'attachment; filename=SSNIT_Branches_list.csv'
            response.headers['Content-Type'] = 'application/csv'
            
            log.write_to_console(msg="Administrators export done returning file")
            return response

    except TemplateNotFound as e:
        raise e

@admins.route('/branches/search', methods=['GET', 'POST'])
@log_access.log_request
def branches_search():
    try:

        print("In Branches Search")
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
        result = svc.searchBranches(request_data)

        return json.dumps(result)
    except TemplateNotFound as e:
        raise e


@admins.route('/branches/add', methods=['GET', 'POST'])
@log_access.log_request
def branches_add():
    try:

        print("In Branches Add")
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
        result = svc.addBranch(request_data)

        return jsonify(result)
    except TemplateNotFound as e:
        raise e

@admins.route('/branches/remove', methods=['GET', 'POST'])
@log_access.log_request
def branches_remove():
    try:

        print("In Branches Remove")
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
        result = svc.removeBranch(request_data)

        return jsonify(result)
    except TemplateNotFound as e:
        raise e
