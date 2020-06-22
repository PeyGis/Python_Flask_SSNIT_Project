"""
This file contains all application Configurations
"""

# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# config for running application on host and port
APP_IP="0.0.0.0"
APP_PORT = 8021

# MYSQL Connection variables
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWD= ''
MYSQL_DATABASE='ssnit_innolink_db'

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "secret_key"

# Secret key for signing cookies
SECRET_KEY = "A0Zr08j/3yX Y~XHH!jmN]LWX/,?RT"
# Flask-session configs
SESSION_TYPE = 'filesystem'
COOKIE_VALUE = 'sess'
#COOKIE_VALUE = '饼干'

# Multi-Language Configurations
DEFAULT_LANG = "en"


UPLOAD_DIRECTORY = "./app/static/uploads/"
DOWN_DIRECTORY = "static/uploads/"

# UPLOAD_DIRECTORY = "/var/web/web.app/public_html/api/fusion_dev/services/bulkpay/v1_0/logs/upload/"
# DOWN_DIRECTORY = "/var/web/web.app/public_html/api/fusion_dev/services/bulkpay/v1_0/logs/upload/"

SOCKET_IP = "192.168.0.221"
SOCKET_PORT = 12099
API_URL = ""

FUSION_URL = ""
VA_URL = ""
EMAIL_URL = "http://45.79.139.232:7474/sendmail"

# FUSION SETTING
FS_INST_APIKEY = ""
FS_INST_ID = ""

DEF_HEADER = {'Content-Type':'application/json'}
MAIL_HEADER = {}

ACCESS_LOG_PATH = "log/access"
UPLOAD_LOG_PATH = "log/upload"
PROCESS_UPLOAD_LOG_PATH = "log/process_upload"
EVENT_LOG_PATH = "log/event"
ERROR_LOG_PATH = "log/error"
CS_REQ_LOG_PATH = "log/cs_requests"
AD_REQ_LOG_PATH = "log/ad_requests"
USER_ACCESS_LOG_PATH = "log/user_access"
SMARTDOG_URL = ""
ALERT_LIST = ""
