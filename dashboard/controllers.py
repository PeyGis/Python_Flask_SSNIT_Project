# Import flask dependencies
from flask import Blueprint, request, render_template, abort, \
                  flash, g, session, redirect, url_for, jsonify
from jinja2 import TemplateNotFound
# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash
# EXPLAIN_TEMPLATE_LOADING
# Import the database object from the main app module
#from app import db
from math import cos
import json
import pygal
from app import config
from app import language
from app.dashboard.services import dashboardServices

# Define the blueprint: 'auth', set its url prefix: app.url/auth
dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard', template_folder='templates')
# auth  = decorators.SessionAuth()
cookie_jar = config.COOKIE_VALUE

# Set language variable
lang = {}
lang = getattr(language, config.DEFAULT_LANG)


# Set the route and accepted methods
@dashboard.route('/', methods=['GET', 'POST'])
def dashboard_page():
    try:
        print("In Dashboard")
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

        svc = dashboardServices(session_details)

        if request.method == 'POST':
            print("In POST")
            data = svc.getAnalsisData(request.form.to_dict())
            # return jsonify(**data)
            return json.dumps(data)

        data = svc.getAnalsisData({})
        print(data)

        # pie_chart = pygal.Pie()
        # pie_chart.title = 'Transactions Status Chart'
        # for result in data['trans_status']:
        #     pie_chart.add(result['msg_stat'], result['amount'])
        # pie_chart_full = pie_chart.render_data_uri()

        # line_chart = pygal.HorizontalBar()
        # line_chart.title = 'Total Amount Transafered (in GHS)'
        # for result in data['data']['bar_data']:
        #     line_chart.add(result['institution'], result['number'])
        # horz_line_chart = line_chart.render_data_uri()

        line_chart = pygal.Bar()
        line_chart.title = 'Transaction type chart'
        # line_chart.x_labels = map(str, range(2002, 2013))
        line_chart.x_labels = []
        line_number = []
        line_amount = []
        for result in data['sdata']:
            line_chart.x_labels.append(result['status'])
            line_number.append(result['num'])

        line_chart.add('Number', line_number)
        # line_chart.render()
        line_chart_full = line_chart.render_data_uri()

        user_lang = lang

        if "lang" in session_details:
            user_lang = getattr(language, session_details['lang'])

        # print(user_lang)

        return render_template("dashboard/dashboard.html", lang=user_lang, mStyle=language.STYLE['dashboard_style'], userdata=session_details, bar_chart_full=line_chart_full, data=data)

    except TemplateNotFound as e:
        raise e


# Set the route and accepted methods
@dashboard.route('/filter', methods=['GET', 'POST'])
def dashboard_filter():
    try:
        print("In Dashboard")
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

        data = {}
        svc = dashboardServices(session_details)

        if request.method == 'POST':
            print("In POST")
            data = svc.getAnalsis(request.form.to_dict())
            # return jsonify(**data)
            return json.dumps(data)
        elif request.method == 'GET':
            data = svc.getAnalsis(request.args.to_dict())

        #data = svc.getAnalsis({})
        print(data)

        # pie_chart = pygal.Pie()
        # pie_chart.title = 'Transactions Status Chart'
        # for result in data['trans_status']:
        #     pie_chart.add(result['msg_stat'], result['amount'])
        # pie_chart_full = pie_chart.render_data_uri()

        # line_chart = pygal.HorizontalBar()
        # line_chart.title = 'Total Amount Transafered (in GHS)'
        # for result in data['data']['bar_data']:
        #     line_chart.add(result['institution'], result['number'])
        # horz_line_chart = line_chart.render_data_uri()

        line_chart = pygal.Bar()
        line_chart.title = 'Transaction type chart'
        # line_chart.x_labels = map(str, range(2002, 2013))
        line_chart.x_labels = []
        line_number = []
        line_amount = []
        for result in data['sdata']:
            line_chart.x_labels.append(result['status'])
            line_number.append(result['num'])

        line_chart.add('Number', line_number)
        # line_chart.render()
        line_chart_full = line_chart.render_data_uri()

        user_lang = lang

        if "lang" in session_details:
            user_lang = getattr(language, session_details['lang'])

        # print(user_lang)

        return render_template("dashboard/dashboard.html", lang=user_lang, mStyle=language.STYLE['dashboard_style'], userdata=session_details, bar_chart_full=line_chart_full, data=data)

    except TemplateNotFound as e:
        raise e
