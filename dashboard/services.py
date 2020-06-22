# werkzeug Imports Needed
# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Importing other dependencies
import uuid
import datetime
import hashlib, random
import base64

from passlib.hash import sha256_crypt

from app import config
from app import language
from app.dashboard.models import Dashboard
from app.libs.logger import Logger

class dashboardServices(object):
    """
        Class contains functions and attributes for authtentication
        Function: * getCampainge(sel)
    """
    def __init__(self, user):
        self.lang = {}
        self.lang = getattr(language, config.DEFAULT_LANG)
        self.user = user
        self.model = Dashboard(user)
        self.logger = Logger()


    def getAnalsis(self, request_data):
        """
            This function handles all logic related to login on the platform

            @Params : void
        """

        if request_data == {}:
            fromdate = ''
            todate = ''
            now_date = datetime.datetime.today().date()
                
            from_dat = datetime.datetime(now_date.year, now_date.month, 1)
            from_date = str(from_dat.year) +'-'+ str(from_dat.month) +'-'+ str(from_dat.day)
            
            to_dat = datetime.datetime(from_dat.year, from_dat.month+1, 1)
            # to_dat = datetime.datetime(from_dat.year, from_dat.month+1, 1) - datetime.timedelta (days = 1)
            to_date = str(to_dat.year) +'-'+ str(to_dat.month) +'-'+ str(to_dat.day)
            
            request_data = {'offset':0, 'records':1000000, 'fromdate': from_date, 'todate': to_date}
        else:
            if request_data['fromdate'] == "" or request_data['fromdate'] == None:
                now_date = datetime.datetime.today().date()
                
                from_dat = datetime.datetime(now_date.year, now_date.month, 1)
                from_date = str(from_dat.year) +'-'+ str(from_dat.month) +'-'+ str(from_dat.day)
                request_data['start_date'] = from_date
            else:               
                request_data['fromdate'] = request_data['fromdate'] + " 00:00:00"
                request_data['start_date'] = request_data['fromdate']

            if request_data['todate'] == None or request_data['todate'] == '':
                to_dat = datetime.datetime(from_dat.year, from_dat.month+1, 1)
                # to_dat = datetime.datetime(from_dat.year, from_dat.month+1, 1) - datetime.timedelta (days = 1)
                to_date = str(to_dat.year) +'-'+ str(to_dat.month) +'-'+ str(to_dat.day)
                request_data['end_date'] = to_date
            else:               
                request_data['todate'] = request_data['todate'] + " 23:59:59"
                request_data['end_date'] = request_data['todate']
            
            request_data['offset'] = 0
            request_data['records'] = 1000000

        print(request_data)
 
        self.logger.write_to_console("EVENT", "loading all bulkpay uploads for {0}".format(self.user['username']))
        
        # if self.user['name'] == "Administrator":
        dash_data = self.model.getAdminAnalysis(request_data)
        # else:
        #     dash_data = self.model.getBranchAnalysis(request_data)

        print(dash_data)

        self.logger.write_to_console("EVENT", "Administrators gotten | Success.")
        # return {"code":language.CODES['SUCCESS'], "msg":self.lang['data_retrived'], "data":dash_data}
        return dash_data


    def getAnalsisData(self, request_data):
        """
            This function handles all logic related to login on the platform

            @Params : void
        """

        if request_data == {}:
            fromdate = ''
            todate = ''
            now_date = datetime.datetime.today().date()
                
            from_dat = datetime.datetime(now_date.year, now_date.month, 1)
            from_date = str(from_dat.year) +'-'+ str(from_dat.month) +'-'+ str(from_dat.day) + " 00:00:00"
            
            to_dat = datetime.datetime(from_dat.year, from_dat.month+1, 1)
            # to_dat = datetime.datetime(from_dat.year, from_dat.month+1, 1) - datetime.timedelta (days = 1)
            to_date = str(to_dat.year) +'-'+ str(to_dat.month) +'-'+ str(to_dat.day) + " 00:00:00"
            
            request_data = {'start_date': from_date, 'end_date': to_date}
        else:
            if request_data['fromdate'] == "" or request_data['fromdate'] == None:
                now_date = datetime.datetime.today().date()
                
                from_dat = datetime.datetime(now_date.year, now_date.month, 1)
                from_date = str(from_dat.year) +'-'+ str(from_dat.month) +'-'+ str(from_dat.day) + " 00:00:00"
                request_data['fromdate'] = from_date
                request_data['start_date'] = request_data['fromdate']
            else:               
                request_data['fromdate'] = request_data['fromdate'] + " 00:00:00"
                request_data['start_date'] = request_data['fromdate']

            if request_data['todate'] == None or request_data['todate'] == '':
                to_dat = datetime.datetime(from_dat.year, from_dat.month+1, 1)
                # to_dat = datetime.datetime(from_dat.year, from_dat.month+1, 1) - datetime.timedelta (days = 1)
                to_date = str(to_dat.year) +'-'+ str(to_dat.month) +'-'+ str(to_dat.day) + " 23:59:59"
                request_data['todate'] = to_date
                request_data['end_date'] = request_data['todate'] 
            else:               
                request_data['todate'] = request_data['todate'] + " 23:59:59"
                request_data['end_date'] = request_data['todate']
            
            # request_data['offset'] = 0
            # request_data['records'] = 1000000

        print(request_data)
 
        self.logger.write_to_console("EVENT", "Getting analysis for {0}".format(self.user['username']))
        
        # if self.user['name'] == "Administrator":
        dash_data = self.model.getAdminAnalysis(request_data)
        # else:
        #     dash_data = self.model.getBranchAnalysis(request_data)
        
        return dash_data
