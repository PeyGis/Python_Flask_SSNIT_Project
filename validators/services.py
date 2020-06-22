# werkzeug Imports Needed
# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Importing other dependencies
import uuid
import datetime
import hashlib, random
import base64
import string
import random
import math

from passlib.hash import sha256_crypt

from app import config
from app import language
from app.validators.models import Validator
from app.libs.logger import Logger
from app.libs.utils import Utilites

class validatorServices(object):
    """
    Class contains functions and attributes for authtentication
    Function: * getCampainge(sel)
    """
    def __init__(self, user):
        self.lang = {}
        self.lang = getattr(language, config.DEFAULT_LANG)
        self.user = user
        self.model = Validator(user)
        self.logger = Logger()

    def getAllValidators(self, request_data):
        filter_data={}
        if request_data == {}:
            request_data = {'offset':0, 'records':10, 'branch':'None'}
        else:
            request_data['offset'] = int(request_data['page'])*10
            request_data['records'] = 10

        validator_data = self.model.getAllValidators(request_data)
        filter_data['validators'] = validator_data[0]
        filter_data['pages'] = math.ceil(validator_data[1][0]['count']/10)
        filter_data['branches'] =  self.model.getBranches()
        print(filter_data)
        return filter_data
        
    def getValidatorsHistory(self, request_data):

        self.logger.write_to_console("EVENT", "{0} Getting Validators History {1}".format(self.user['username'], str(request_data)))
        filter_data={}
        if request_data == {}:
            request_data = {'offset':0, 'records':10, 'user_type': 'validator'}
        else:
            request_data['offset'] = int(request_data['page'])*10
            request_data['records'] = 10
            request_data['user_type'] = 'validator'
        print(str(request_data))

        all_data =  self.model.getValidatorsHistory(request_data)    
        filter_data['history'] =  all_data[0]
        filter_data['pages'] = math.ceil(all_data[1][0]['count']/10)
        return filter_data
    
    def addValidator(self, request_data):
        """
            This function handles the adding of a new validator
            @Params : void
        """
        self.logger.write_to_console("EVENT", "{0} Adding Validator {1}".format(self.user['username'], str(request_data)))
        request_data['msisdn'] = "233" + request_data['msisdn'][-9:]
        request_data['email'] = request_data['email'].strip()
        
        admin_data = self.model.getValidatorByMsisdn(request_data['msisdn'])
        if admin_data == []:
            admin_data = self.model.getValidatorByEmail(request_data['email'])
            if admin_data == []:
                self.logger.write_to_console("EVENT", "Preparing data")

                res = self.model.addValidator(request_data) 
                if res == True:
                    #Utilites.send_mail(Utilites, "SSNIT PORTAL", "<p>Hi {0}</p><p>Welcome SSNIT, below are your login credentials.<br><br>Username: {1}<br>Password: {2}<br><br><br> Regards</p><p>FUSION PLATFORM</p>".format(request_data['first_name'], request_data['username'], raw_password), [request_data['email']])
                    return {"code":language.CODES['SUCCESS'], "msg":self.lang['validator_added'], "data":[]}
                else:
                    return {"code":language.CODES['FAIL'], "msg":self.lang['validator_add_fail'], "data":[]}
            else:
                self.logger.write_to_console("EVENT", "Existing validator email "+ request_data['email'] + " | Blocked User.")
                return {"code":language.CODES['FAIL'], "msg": "Email is already registered to another validator.", "data":[]}
        else:
            self.logger.write_to_console("EVENT", "Existing validator phone "+ request_data['msisdn'] + " | Blocked User.")
            return {"code":language.CODES['FAIL'], "msg": "Phone number is already registered to another validator.", "data":[]}

    def deleteValidator(self, request_data):
        self.logger.write_to_console("EVENT", "{0} Deleting Validator {1}".format(self.user['username'], str(request_data['validator_id'])))
        res = self.model.deleteValidator(request_data['validator_id'])
        if res == True:
            return {"code":language.CODES['SUCCESS'], "msg":self.lang['validator_deleted'], "data":[]}
        else:
            return {"code":language.CODES['FAIL'], "msg":self.lang['validator_delete_fail'], "data":[]}
    
    def getValidatorDetails(self, request_data):
       
        self.logger.write_to_console("EVENT", "Getting Details for "+ self.user['username'])
        
        validator_data = self.model.getValidatorByEmail(request_data['email'])
        if validator_data == []:
            self.logger.write_to_console("EVENT", "Failed to get validator "+ self.user['username'] + " | Non-Existing User.")
            return {"code":language.CODES['FAIL'], "msg":self.lang['wrong_username'], "data":[]}
        else:
            self.logger.write_to_console("EVENT", "Validator Data retreived successfully "+ self.user['username'] + " | Success.")
            return {"code":language.CODES['SUCCESS'], "msg":self.lang['record_successful'], "data":validator_data[0]}


    def updateValidator(self, request_data):

        self.logger.write_to_console("EVENT", "{0} Updating Validator {1}".format(self.user['username'], str(request_data)))
        
        request_data['msisdn'] = "233" + request_data['msisdn'][-9:]

        res = self.model.updateValidator(request_data)
        if res == True:
            return {"code":language.CODES['SUCCESS'], "msg":self.lang['validator_updated'], "data":[]}
        else:
            return {"code":language.CODES['FAIL'], "msg":self.lang['validator_update_fail'], "data":[]}

    def searchValidatoinHistory(self, request_data):
 
        self.logger.write_to_console("EVENT", "Searching vouchers for {0}".format(request_data['search_param']))
        request_data['user_type'] = 'validator'
        voucher_data = self.model.searchValidatoinHistory(request_data)
        print(voucher_data)
        for result in voucher_data:

            result["date_created"] = result["date_created"].strftime("%Y-%m-%d %H:%M:%S")
        
        return voucher_data

