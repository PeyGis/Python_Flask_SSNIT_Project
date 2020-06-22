"""
These file contains all the initialisations and configurations for the application
"""

# Import flask and template dependencies
from flask import Flask 
from flask import render_template
from flask import session
from flask import request
from flask import redirect
from flask import url_for
from flask_session import Session
from flask_socketio import SocketIO
from flask_socketio import send, emit

import flask_excel as excel

# Standard Library Dependencies
import time

# Import project dependencies
from app import config
from app.libs.utils import Utilites
from app.libs.logger import Logger
from app.libs.decorators import AccessLogger

# Import a module / component using its blueprint handler variable
from app.home.controllers import home
from app.dashboard.controllers import dashboard
from app.activities.controllers import activities
from app.admins.controllers import admins
from app.vouchers.controllers import vouchers
from app.validators.controllers import validators
from app.logs.controllers import logs

log = Logger()
log_access = AccessLogger()

# Creating flask application instance
app      = Flask(__name__)
socketio = SocketIO(app,async_mode=None)
excel.init_excel(app)
# Configurations
app.config['SESSION_TYPE'] = config.SESSION_TYPE
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['PROPAGATE_EXCEPTIONS'] = True
Session(app)
app.config.from_object(__name__)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
  return render_template('404.html'), 404

# Sample HTTP error handling
@app.errorhandler(500)
def server_error(error):
  return render_template('500.html'), 500

@socketio.on('connected')
@log_access.log_request
def handle_message(connected):
    print(request)
    for x in range(1,10):
        time.sleep(2)
        socketio.emit('dashboard', "Hurrray it works", broadcast=True)

@socketio.on('dashboard_sock')
@log_access.log_request
def dashboard_sock(dashboard_sock):
    socketio.emit('dashboard_sock', "Broadcasting", broadcast=True)

@app.route('/' , methods=['GET', 'POST'])
@log_access.log_request
def root_route():
    return redirect(url_for('home.home_page'))

# Registering blueprints
app.register_blueprint(home)
app.register_blueprint(dashboard)
app.register_blueprint(activities)
app.register_blueprint(admins)
app.register_blueprint(vouchers)
app.register_blueprint(validators)
app.register_blueprint(logs)

# decor = """
#         #################################################################
#         ## ╔═╗╦╔═╗╦  ╦╔═╗╔═╗  ╔═╗╔═╗╦═╗╔╦╗╔═╗╦    ╔═╗╔═╗╦═╗╦  ╦╔═╗╦═╗  ##
#         ## ╚═╗║║  ║  ║╠╣ ║╣   ╠═╝║ ║╠╦╝ ║ ╠═╣║    ╚═╗║╣ ╠╦╝╚╗╔╝║╣ ╠╦╝  ##
#         ## ╚═╝╩╚═╝╩═╝╩╚  ╚═╝  ╩  ╚═╝╩╚═ ╩ ╩ ╩╩═╝  ╚═╝╚═╝╩╚═ ╚╝ ╚═╝╩╚═  ##
#         #################################################################
#         """
decor = "SSNIT INNOLINK PORTAL"
log.write_log(msg=decor)
