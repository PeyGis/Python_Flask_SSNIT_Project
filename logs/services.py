# werkzeug Imports Needed
# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Importing other dependencies
import uuid
import datetime
import hashlib, random
import base64
import os

from passlib.hash import sha256_crypt

from app import config
from app import language
from app.logs.models import LogModel
from app.libs.logger import Logger
from app.config import ACCESS_LOG_PATH, EVENT_LOG_PATH, ERROR_LOG_PATH, CS_REQ_LOG_PATH, AD_REQ_LOG_PATH, USER_ACCESS_LOG_PATH, UPLOAD_LOG_PATH, PROCESS_UPLOAD_LOG_PATH

class logServices(object):
    """
        Class contains functions and attributes for authtentication
        Function: * getCampainge(sel)
    """
    def __init__(self, user):
        self.lang = {}
        self.lang = getattr(language, config.DEFAULT_LANG)
        self.user = user
        self.model = LogModel(user)
        self.logger = Logger()

        self.access_file = os.path.abspath(ACCESS_LOG_PATH)
        self.event_file = os.path.abspath(EVENT_LOG_PATH)
        self.error_file = os.path.abspath(ERROR_LOG_PATH)
        self.upload_file = os.path.abspath(UPLOAD_LOG_PATH)
        self.process_upload_file = os.path.abspath(PROCESS_UPLOAD_LOG_PATH)
        self.cs_req_file = os.path.abspath(CS_REQ_LOG_PATH)
        self.ad_req_file = os.path.abspath(AD_REQ_LOG_PATH)
        self.ad_access_file = os.path.abspath(USER_ACCESS_LOG_PATH)


    def getLogData(self, log_type, log_date):
        """
            This function gets user logs

            @Params : void
        """
        filename = ''
        if log_type == "user_access":
            filename = self.ad_access_file+ "/" +log_date +".log"
        elif log_type == "customers":
            filename = self.cs_req_file+ "/" +log_date +".log"
        elif log_type == "admins":
            filename = self.ad_req_file+ "/" +log_date +".log"
        elif log_type == "access":
            filename = self.access_file+ "/" +log_date +".log"
        elif log_type == "error":
            filename = self.error_file+ "/" +log_date +".log"
        elif log_type == "upload":
            filename = self.upload_file+ "/" +log_date +".log"
        elif log_type == "process_upload":
            filename = self.process_upload_file+ "/" +log_date +".log"
        else:
            return "No Logs found"

        print(filename)
        try:
            f = open(filename, "r")
            return f.read()
        except Exception as e:
            return "No Logs found"

    def getLogDataExport(self, log_type, log_date):
        """
            This function handles all logic related to login on the platform

            @Params : void
        """
        filename = ''
        if log_type == "user_access":
            filename = self.ad_access_file+ "/" +log_date +".log"
        elif log_type == "customers":
            filename = self.cs_req_file+ "/" +log_date +".log"
        elif log_type == "admins":
            filename = self.ad_req_file+ "/" +log_date +".log"
        elif log_type == "access":
            filename = self.access_file+ "/" +log_date +".log"
        elif log_type == "error":
            filename = self.error_file+ "/" +log_date +".log"
        elif log_type == "upload":
            filename = self.upload_file+ "/" +log_date +".log"
        elif log_type == "process_upload":
            filename = self.process_upload_file+ "/" +log_date +".log"
        else:
            return "No Logs found"

        print(filename)
        try:
            f = open(filename, "r")
            return f
        except Exception as e:
            return "No Logs found"
        
