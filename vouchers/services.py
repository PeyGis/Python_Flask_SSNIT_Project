# werkzeug Imports Needed
# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Importing other dependencies
import uuid
import datetime
import hashlib, random
import base64
import string
import json
import math
import os
import re
from threading import Thread
import unicodecsv

from passlib.hash import sha256_crypt

from app import config
from app import language
from app.vouchers.models import Vouchers
from app.activities.models import Activities
from app.libs.logger import Logger
from app.libs.utils import Utilites

class vouchersServices(object):
    """
        Class contains functions and attributes for authtentication
        Function: * getCampainge(sel)
    """
    def __init__(self, user):
        self.lang = {}
        self.lang = getattr(language, config.DEFAULT_LANG)
        self.user = user
        self.model = Vouchers(user)
        self.logger = Logger()


    def getAllVouchers(self, request_data):
        """
            This function handles all logic related to login on the platform

            @Params : void
        """

        if request_data == {}:
            request_data = {'page': 0, 'fromdate': '', 'todate': ''}
        else:
            pass

        print(request_data)
 
        self.logger.write_to_console("EVENT", "loading all vouchers for {0}".format(self.user['username']))
        
        if request_data == {}:
            request_data = {'offset':0, 'records':10, 'fromdate':'', 'todate':'', 'status':''}
        else:
            request_data['offset'] = int(request_data['page'])*10
            request_data['records'] = 10

        if self.user.get('branch_code',"").lower()!='all':
            request_data['branch']=self.user.get('branch')
        customer_data = self.model.getAllVouchers(request_data)
        print(customer_data)

        branch_data = self.model.getBranches()

        for result in customer_data[0]:

            result["date_uploaded"] = result["date_uploaded"].strftime("%Y-%m-%d %H:%M:%S")

            # if result["status"] == 1:
            #     result["status"] = self.lang["active"]
            # else:
            #     result["status"] = self.lang["inactive"]

        pages = math.ceil(customer_data[1][0]['count']/12)
        print(pages)

        self.logger.write_to_console("EVENT", "Administrators gotten | Success.")
        return {"code":language.CODES['SUCCESS'], "msg":self.lang['data_retrived'], "data":customer_data[0], "pages": pages, "branches": branch_data}
        return customer_data

    def getAllvouchersExport(self, request_data):
        """
            This function handles all logic related to login on the platform

            @Params : void
        """

        request_data['offset'] = 0
        request_data['records'] = 1000000

        print(request_data)
 
        self.logger.write_to_console("EVENT", "loading all bulkpay uploads for {0}".format(self.user['username']))
        
        export_list = [['ACCOUNT', 'FIRST NAME', 'LAST NAME', 'MIDDLE NAME','GENDER','PHONE NUMBER', 'BRANCH', 'STATUS', 'DATE REGISTERED']]

        # if self.user['access_level_id'] == 4:
        merchant_data = self.model.getAllvouchers(request_data)
        # else:
        #     merchant_data = self.model.getAllvouchersByBranch(request_data)

        print(merchant_data)
        for result in merchant_data[0]:

            result["join_date"] = result["join_date"].strftime("%Y-%m-%d %H:%M:%S")

            if result["status"] == 1:
                result["status"] = self.lang["active"]
            else:
                result["status"] = self.lang["inactive"]

            export_list.append([result['id'], result['first_name'], result['last_name'], result['middle_name'], result['gender'], result['status'], result['join_date']])

        print(export_list)
        return export_list


    def addVoucher(self, request_data):
        """
            This function handles all logic related to login on the platform

            @Params : void
        """
        self.logger.write_to_console("EVENT", "{0} Adding Customer {1}".format(self.user['username'], str(request_data)))

        request_data['requested_by'] = self.user['username']
        request_data['branch'] = request_data['customer_account'][:3]

        print(request_data)
        result = self.model.addNewRegistrationRequest(request_data)
        result = self.model.addCustomerRequest({'requested_by': self.user['username'], 'request_type': '0', 'customer_msisdn': request_data['customer_msisdn'], 'customer_account': request_data['customer_account'], 'branch': self.user['branch_id'] })
        self.logger.write_log("CUSTOMER", "Customer registration Request | {} | {} | {} | ".format(request_data['customer_msisdn'], request_data['customer_account'], self.user['username']))
        # return customer_data
        return {'code': '00', 'msg': 'Customer registration request sent successfully'}

    def getVoucherDetials(self, request_data):
        """
            This function handles all logic related to login on the platform
            @Params : void
        """       
        self.logger.write_to_console("EVENT", "Getting voucher details: {}".format(request_data))
        # print(request_data.get('msisdn'))
        request_keys  = request_data.keys()
        validation_keys = ["mno","msisdn","apikey","serial_no"]
        for item in validation_keys: 
            if item  not in request_data:
               return {'code': '01', 'msg': 'Wrong parameters sent.', 'data':[]}

        if request_data['apikey'] != "500cdd1b531d83e00a5a4":
            return {'code': '01', 'msg': 'Unauthorised request.', 'data':[]}

        # if 'serial_no' not in request_data or 'sticker_no' not in request_data or 'msisdn' not in request_data or 'mno' not in request_data:
        #     return {'code': '01', 'msg': 'Wrong parameters sent.', 'data':[]}

        # vhash = hashlib.sha256((request_data['serial_no'] +":"+ request_data['sticker_no']).encode())
        vhash = hashlib.sha256((request_data['serial_no']).encode())
        vhash = vhash.hexdigest()
        print(vhash)

        voucher_data = self.model.getVoucherByHash(vhash)
        for result in voucher_data:
            result["date_uploaded"] = result["date_uploaded"].strftime("%Y-%m-%d %H:%M:%S")
            if result["date_validated"] != None:
                result["date_validated"] = result["date_validated"].strftime("%Y-%m-%d %H:%M:%S")

        if voucher_data == []:
            return {'code': '01', 'msg': 'Serial number is invalid.', 'data':[]}
        else:
            return {'code': '00', 'msg': 'Serial number is valid.', 'data':[]}

    def getVoucherDetialsValidate(self, request_data):
        """
            This function handles all logic related to login on the platform
            @Params : void
        """       
        self.logger.write_to_console("EVENT", "Getting voucher details: {}".format(request_data))

        if request_data['apikey'] != "500cdd1b531d83e00a5a4":
            return {'code': '01', 'msg': 'Unauthorised request.', 'data':[]}

        if 'serial_no' not in request_data or 'sticker_no' not in request_data or 'msisdn' not in request_data or 'mno' not in request_data:
            return {'code': '01', 'msg': 'Wrong parameters sent.', 'data':[]}

        vhash = hashlib.sha256((request_data['serial_no'] +":"+ request_data['sticker_no']).encode())
        vhash = vhash.hexdigest()
        print(vhash)

        voucher_data = self.model.getVoucherByHash(vhash)
        for result in voucher_data:
            result["date_uploaded"] = result["date_uploaded"].strftime("%Y-%m-%d %H:%M:%S")
            if result["date_validated"] != None:
                result["date_validated"] = result["date_validated"].strftime("%Y-%m-%d %H:%M:%S")

        if voucher_data == []:
            use_data = { "user_msisdn": request_data['msisdn'], "serial_no": request_data['serial_no'], "sticker_no": request_data['sticker_no'], 'status': "NON-EXISTENT", 'status_details': "Sticker does not exist.", 'user_mno': request_data['mno'], }
            self.model.add_user_activity(use_data)
            blacklist_res = self.report_user(use_data)
            return {'code': '02', 'msg': 'Voucher is invalid.', 'data':[], "blacklisted": blacklist_res}
        else:
            if voucher_data[0]['is_used'] == "USED":
                use_data = { "user_msisdn": request_data['msisdn'], "serial_no": request_data['serial_no'], "sticker_no": request_data['sticker_no'], 'status': "USED STICKER", 'status_details': "Sticker already used.", 'user_mno': request_data['mno'], }
                self.model.add_user_activity(use_data)
                blacklist_res = self.report_user(use_data)
                return {'code': '01', 'msg': 'Voucher is used', 'data': voucher_data[0], "blacklisted": blacklist_res}
            elif voucher_data[0]['is_used'] == "UNUSED":
                use_data = { "user_msisdn": request_data['msisdn'], "serial_no": request_data['serial_no'], "sticker_no": request_data['sticker_no'], 'status': "VALID STICKER", 'status_details': "Sticker is valid.", 'user_mno': request_data['mno'], }
                self.model.add_user_activity(use_data)
                return {'code': '00', 'msg': 'Voucher is not used', 'data':[]}
            else:
                use_data = { "user_msisdn": request_data['msisdn'], "serial_no": request_data['serial_no'], "sticker_no": request_data['sticker_no'], 'status': "NON-EXISTENT", 'status_details': "Sticker does not exist.", 'user_mno': request_data['mno'], }
                self.model.add_user_activity(use_data)
                blacklist_res = self.report_user(use_data)
                return {'code': '02', 'msg': 'Voucher is invalid.', 'data':[], "blacklisted": blacklist_res}

    def getSerialDetialsValidate(self, request_data):
        """
            This function handles all logic related to login on the platform
            @Params : void
        """       
        self.logger.write_to_console("EVENT", "Getting voucher details: {}".format(request_data))

        if request_data['apikey'] != "500cdd1b531d83e00a5a4":
            return {'code': '01', 'msg': 'Unauthorised request.', 'data':[]}

        if 'serial_no' not in request_data or 'msisdn' not in request_data or 'mno' not in request_data:
            return {'code': '01', 'msg': 'Wrong parameters sent.', 'data':[]}


        escaped_serial_no = re.sub("\ |\?|\.|\!|\/|\;|\:|\%|\@|\#|\*|\)|\(", '', request_data['serial_no'])
        vhash = hashlib.sha256((escaped_serial_no.encode()))
        vhash = vhash.hexdigest()
        print(vhash)

        voucher_data = self.model.getSerialByHash(vhash)
        validators = self.model.getValidatorByMsisdn(request_data['msisdn'])

        
        if voucher_data == []:
            if validators == []:
                use_data = { "user_msisdn": request_data['msisdn'], "user_type": "gen_public", "user_name": "unknown", "serial_no": request_data['serial_no'], 'status': "NON EXISTENT", 'status_details': "Serial does not exist", 'user_mno': request_data['mno'], }
                self.model.add_user_activity(use_data)
            else:
                use_data = { "user_msisdn": request_data['msisdn'], "user_type": "validator", "user_name": validators[0]["first_name"], "user_branch": validators[0]["branch"], "serial_no": request_data['serial_no'], 'status': "FAILED", 'status_details': "Serial does not exist", 'user_mno': request_data['mno'], }
                self.model.add_user_activity(use_data)
            return {'code': '02', 'msg': 'Your serial is invalid.', 'data':[]}
        else:
            #identify who is initiating the validation (a user or a validator)
            #validators = self.model.getValidatorByMsisdn(request_data['msisdn'])

            if validators == []:
                #if no validator data is found, then user is a public user
                if voucher_data[0]['serial_status'] == "NOT VALIDATED":
                    use_data = { "user_msisdn": request_data['msisdn'], "user_type": "gen_public", "user_name": "unknown", "serial_no": request_data['serial_no'], 'status': "NOT VALIDATED", 'status_details': "Serial is not validated", 'user_mno': request_data['mno'], }
                    self.model.add_user_activity(use_data)
                    return {'code': '01', 'msg': 'Your serial is not validated', 'data': []}
                elif voucher_data[0]['serial_status'] == "VALIDATED":
                    voucher_data[0]["expiry_date"] = voucher_data[0]["expiry_date"].strftime("%Y-%m-%d")
                    expiry_date = voucher_data[0]["expiry_date"]
                    use_data = { "user_msisdn": request_data['msisdn'], "user_type": "gen_public", "user_name": "unknown", "serial_no": request_data['serial_no'], 'status': "VALIDATED", 'status_details': 'Serial is validated but expires on ' + voucher_data[0]["expiry_date"], 'user_mno': request_data['mno'], }
                    self.model.add_user_activity(use_data)
                    return {'code': '00', 'msg': 'Your serial is valid but expires on ' + voucher_data[0]["expiry_date"], 'data':[]}
                else:
                    use_data = { "user_msisdn": request_data['msisdn'], "user_type": "gen_public", "user_name": "unknown", "serial_no": request_data['serial_no'], 'status': "NO ACTION", 'status_details': "No action performed", 'user_mno': request_data['mno'], }
                    self.model.add_user_activity(use_data)
                    return {'code': '02', 'msg': 'No action to perform', 'data':[]}

            else:
                    #ok now we know its a validator, lets proceed to validate a serial number if not validated yet
                if voucher_data[0]['serial_status'] == "NOT VALIDATED":
                    #All serials must be assigned to branch before validation can be successful so check here
                    if voucher_data[0]['branch_assigned'] == "None":
                        use_data = { "user_msisdn": request_data['msisdn'], "user_type": "validator", "user_name": validators[0]["first_name"], "user_branch": validators[0]["branch"], "serial_no": request_data['serial_no'], 'status': "FAILED", 'status_details': "Serial not assigned to a branch", 'user_mno': request_data['mno'], }
                        self.model.add_user_activity(use_data)
                        return {'code': '01', 'msg': 'Serial must be assigned to a branch', 'data': []}

                    else:
                        expiry_date = self.addDaysToDate(addDays = 90)
                        update_params = {
                            "serial_id": voucher_data[0]['serial_id'],
                            "serial_status": "VALIDATED",
                            "validator_msisdn": validators[0]["msisdn"],
                            "date_validated": "NOW()",
                            "expiry_date": expiry_date
                        }
                        update_response = self.model.updateSerial(update_params)
                        if update_response == True:
                            use_data = { "user_msisdn": request_data['msisdn'], "user_type": "validator", "user_name": validators[0]["first_name"], "user_branch": validators[0]["branch"], "serial_no": request_data['serial_no'], 'status': "SUCCESS", 'status_details': "Successful serial validation", 'user_mno': request_data['mno'], }
                            self.model.add_user_activity(use_data)
                            return {'code': '00', 'msg': 'Serial successfully validated', 'data': []}
                        else:
                            use_data = { "user_msisdn": request_data['msisdn'], "user_type": "validator", "user_name": validators[0]["first_name"], "user_branch": validators[0]["branch"], "serial_no": request_data['serial_no'], 'status': "FAILED", 'status_details': "Failed to validate serial ", 'user_mno': request_data['mno'], }
                            self.model.add_user_activity(use_data)
                            return {'code': '01', 'msg': 'Failed to validate Serial', 'data': []}

                elif voucher_data[0]['serial_status'] == "VALIDATED":
                    use_data = { "user_msisdn": request_data['msisdn'], "user_type": "validator", "user_name": validators[0]["first_name"], "user_branch": validators[0]["branch"], "serial_no": request_data['serial_no'], 'status': "DUPLICATE", 'status_details': "Serial already validated", 'user_mno': request_data['mno'], }
                    self.model.add_user_activity(use_data)
                    return {'code': '00', 'msg': 'Serial is already validated', 'data':[]}

                else:
                    use_data = { "user_msisdn": request_data['msisdn'], "user_type": "validator", "user_name": validators[0]["first_name"], "user_branch": validators[0]["branch"], "serial_no": request_data['serial_no'], 'status': "NO ACTION", 'status_details': "No action performed", 'user_mno': request_data['mno'], }
                    self.model.add_user_activity(use_data)
                    return {'code': '02', 'msg': 'Nothing for admin to perform', 'data':[]}

    def report_user(self, use_data):
        today_start = str(datetime.datetime.today().date())+' 00:00:00'
        today_end = str(datetime.datetime.today().date())+' 23:59:59'

        request_data = {'offset':0, 'records':1000, 'fromdate': today_start, 'todate': today_end, 'status':'', 'user_msisdn': use_data["user_msisdn"]}
        act = Activities({})
        vdata = act.getAllActivities(request_data)
        print(vdata)
        if len(vdata[0]) >=3:
            self.model.addBlacklist({"msisdn": use_data["user_msisdn"], "reason": "Too many wrong tries"})
            return True
        else:
            return False

    def useVoucher(self, request_data):
        """
            This function handles all logic related to login on the platform
            @Params : void
        """       
        self.logger.write_to_console("EVENT", "Getting voucher details: {}".format(request_data))

        if request_data['apikey'] != "500cdd1b531d83e00a5a4":
            return {'code': '01', 'msg': 'Unautorised request.', 'data':[]}

        if 'serial_no' not in request_data or 'sticker_no' not in request_data or 'msisdn' not in request_data or 'mno' not in request_data or 'car_no' not in request_data:
            return {'code': '01', 'msg': 'Wrong parameters sent.', 'data':[]}

        vhash = hashlib.sha256((request_data['serial_no'] +":"+ request_data['sticker_no']).encode())
        vhash = vhash.hexdigest()
        print(vhash)

        voucher_data = self.model.getVoucherByHash(vhash)
        if voucher_data == []:
            return {'code': '01', 'msg': 'Voucher is invalid.', 'data':[]}
        else:
            if voucher_data[0]['is_used'] == "USED":
                return {'code': '01', 'msg': 'Voucher is already used', 'data': []}
            elif voucher_data[0]['is_used'] == "UNUSED":
                vcode = ''.join(random.SystemRandom().choice(string.digits) for _ in range(8))
                sms_status = 'SENT'
                use_data = {
                            "unique_id": voucher_data[0]['unique_id'],
                            "is_used": "USED",
                            "car_no": request_data['car_no'],
                            'user_msisdn': request_data['msisdn'],
                            'user_mno': request_data['mno'],
                            'serial_no': request_data['serial_no'],
                            'sticker_no': request_data['sticker_no'],
                            'sms_status': sms_status,
                            'verification_code': vcode,
                            'date_validated': 'NOW()'
                            }
                print(use_data)
                result = self.model.updateVoucher(use_data)
                if result == True:
                    return {'code': '00', 'msg': 'Voucher validation completed.', 'data':{"car_no": request_data['car_no'], 'use_msisdn': request_data['msisdn'],'serial_no': request_data['serial_no'], 'sticker_no': request_data['sticker_no'], 'verification_code': vcode }}
                else:
                    return {'code': '01', 'msg': 'Failed: Kindly try again.', 'data':[]}
            else:
                return {'code': '01', 'msg': 'Voucher is invalid.', 'data':[]}


    def updateVoucher(self, request_data):
        """
            This function handles all logic related to login on the platform

            @Params : void
        """
        self.logger.write_to_console("EVENT", "{0} Customer Reset Pin {1}".format(self.user['username'], str(request_data)))

        pending_requests = self.model.getCustomerRequests(request_data['id'])

        if request_data['msisdn'] != request_data['id']:     
            if len(pending_requests) > 0:
                for reques in pending_requests:
                    if reques['request_type'] == 2:
                        return {'code': '01', 'msg': 'Change phone number request for customer is already pending.'}
                    else:
                        result = self.model.addCustomerRequest({'requested_by': self.user['username'], 'request_type': '2', 'customer_msisdn': request_data['id'], 'customer_account': request_data['id'], 'branch': self.user['branch_id'], 'change_from': request_data['id'], 'change_to': request_data['msisdn'] })
                        self.logger.write_log("CUSTOMER", "Change Customer Phone Number Request | {} | {} | {} ".format(request_data['customer_id'], request_data['id'], self.user['username']))
                        break

        result = self.model.updatevouchers({ 'id': request_data['id'], 'first_name': request_data['first_name'], 'middle_name': request_data['middle_name'], 'last_name': request_data['last_name'], 'gender': request_data['gender'] })
        
        self.logger.write_log("CUSTOMER", "Update Customer Details | {} | {} ".format(request_data['id'], self.user['username']))
        
        return {'code': '00', 'msg': 'Request sent.'}


    def searchvouchers(self, request_data):
        """
            This function handles all logic related to login on the platform

            @Params : void
        """
        print(request_data)
 
        self.logger.write_to_console("EVENT", "Searching vouchers for {0}".format(request_data['search_param']))

        customer_data = self.model.searchvouchers(request_data)

        for result in customer_data:

            result["join_date"] = result["join_date"].strftime("%Y-%m-%d %H:%M:%S")

            # if result["status"] == 1:
            #     result["status"] = self.lang["active"]
            # else:
            #     result["status"] = self.lang["inactive"]
        
        return customer_data

    def getAllUploadsRequests(self, request_data):
        """
            This function handles all logic related to login on the platform

            @Params : void
        """

        if request_data == {}:
            request_data = {'page': 0, 'fromdate': '', 'todate': ''}
        else:
            pass

        print(request_data)
 
        self.logger.write_to_console("EVENT", "loading all uploads for {0}".format(self.user['username']))
        
        if request_data == {}:
            request_data = {'offset':0, 'records':10, 'fromdate':'', 'todate':'', 'request_type':''}
        else:
            request_data['offset'] = int(request_data['page'])*10
            request_data['records'] = 10
            
        if self.user.get('branch_code',"").lower()!='all':
                request_data['branch']=self.user.get('branch_code')
                print("branch ##################{}".format(self.user))

        customer_data = self.model.getAllUploads(request_data)
        print(customer_data)

        for result in customer_data[0]:

            result["upload_date"] = result["upload_date"].strftime("%Y-%m-%d %H:%M:%S")

            if result["processed_date"] != None:
                result["processed_date"] = result["processed_date"].strftime("%Y-%m-%d %H:%M:%S")

            if result["approved_date"] != None:
                result["approved_date"] = result["approved_date"].strftime("%Y-%m-%d %H:%M:%S")


        pages = math.ceil(customer_data[1][0]['count']/10)
        print(pages)

        self.logger.write_to_console("EVENT", "Administrators gotten | Success.")
        return {"code":language.CODES['SUCCESS'], "msg":self.lang['data_retrived'], "data":customer_data[0], "pages": pages}
        return customer_data


    def record_uploaded_file(self, file_obl):
        self.logger.write_to_console("EVENT", "Recording Uploaded file | {}".format(file_obl.filename))


        file_extension = file_obl.filename.split(".")
        # filetype = file_extension[-1]
        if file_extension[-1] != "csv":
            return {"code":language.CODES['FAIL'], "msg":self.lang['wrong_file_format'], "data":[]}
        
        bulk_id = self.generate_id(self.user['branch_code'])
        # file_obl.save(secure_filename(file_obl.filename))
        file_obl.save(os.path.join(config.UPLOAD_DIRECTORY, bulk_id+".csv"))
        # fileChecksum = self.md5Checksum(bulk_id+".csv")
        fileSize = os.stat(os.path.join(config.UPLOAD_DIRECTORY, bulk_id+".csv")).st_size

        fields = {"bulk_id":bulk_id,
                      "filename": file_obl.filename,
                      "filesize": fileSize,
                      "fileType": file_extension[-1],
                      # "file_checksum": fileChecksum,
                      "branch": self.user['branch_code'],
                      "uploaded_by": self.user['username']
                }

        self.logger.write_to_console("EVENT", "Uploaded File Details | {}".format(fields))
        result = self.model.insertBulkUpload(fields)
        print(result)
        if result == True:
            # self.logger.write_to_console("EVENT", "Starting processing Thread for | {}".format(file_obl.filename))
            # processing_thread = Thread(target=self.process_csv, args=(os.path.join(config.UPLOAD_DIRECTORY, bulk_id+".csv"), file_obl.filename, self.user['username']))
            # processing_thread.start()
            # self.logger.write_to_console("EVENT", "Thread started for | {}".format(file_obl.filename))
            self.logger.write_log("UPLOAD", "Uploaded Bulk Serials | {} | {} ".format(fields['bulk_id'] + ".csv", self.user['username']) + " | Successful")
            return {"code":language.CODES['SUCCESS'], "msg":self.lang['file_recorded'], "data":[]}
        else:
            self.logger.write_log("UPLOAD", "Uploaded Bulk Serials | {} | {} ".format(fields['bulk_id']+ ".csv", self.user['username']) + " | Failed")
            return {"code":language.CODES['FAIL'], "msg":self.lang['wrong_file_format'], "data":[]}

    def approve_uploaded_file(self, request_data):
        self.logger.write_to_console("EVENT", "Recording Uploaded file | {}".format(request_data['bulk_id']))

        #bulk_details = self.model.getBulkUploadDetails(request_data['bulk_id'])

        fields = {"bulk_id": request_data['bulk_id'],
                  # "file_checksum": fileChecksum,
                  "approval_status": "Approved",
                  "processing_status": "Processing",
                  "approved_by": self.user['username'],
                  "approved_date": "NOW()"
                }

        self.logger.write_to_console("EVENT", "Uploaded File Details | {}".format(fields))

        result = self.model.updateBulkUpload(fields)
        print(result)
        if result == True:
            bulk_details = self.model.getBulkUploadDetails(request_data['bulk_id'])
            self.logger.write_to_console("EVENT", "Starting processing Thread for | {}".format(request_data['bulk_id']))
            processing_thread = Thread(target=self.process_csv_new, args=(os.path.join(config.UPLOAD_DIRECTORY, request_data['bulk_id']+".csv"), bulk_details[0]['approved_date'],self.user['username'],bulk_details[0]['branch'], request_data['bulk_id']))
            processing_thread.start()
            self.logger.write_to_console("EVENT", "Thread started for | {}".format(request_data['bulk_id']))

            self.logger.write_log("PROCESS_UPLOAD", "Approve Bulk Serials | {} | {} ".format(request_data['bulk_id']+ ".csv", self.user['username']) + " | Successful")
            return {"code":language.CODES['SUCCESS'], "msg": "File processing approved.", "data":[]}

        else:
            self.logger.write_log("PROCESS_UPLOAD", "Approve Bulk Serials | {} | {} ".format(request_data['bulk_id']+ ".csv", self.user['username']) + " | Failed")
            return {"code":language.CODES['FAIL'], "msg":self.lang['wrong_file_format'], "data":[]}


    def decline_uploaded_file(self, request_data):
        self.logger.write_to_console("EVENT", "Recording Uploaded file | {}".format(request_data['bulk_id']))

        fields = {"bulk_id": request_data['bulk_id'],
                  # "file_checksum": fileChecksum,
                  "approval_status": "Declined",
                  "processing_status": "Processing",
                  "approved_by": self.user['username'],
                  "approved_date": "NOW()"
                }

        self.logger.write_to_console("EVENT", "Uploaded File Details | {}".format(request_data['bulk_id']))

        result = self.model.updateBulkUpload(fields)
        print(result)
        if result == True:
            self.logger.write_log("PROCESS_UPLOAD", "Decline Bulk Serials | {} | {} ".format(request_data['bulk_id']+ ".csv", self.user['username']) + " | Successful")
            return {"code":language.CODES['SUCCESS'], "msg": "File processing declined.", "data":[]}
        else:
            self.logger.write_log("PROCESS_UPLOAD", "Decline Bulk Serials | {} | {} ".format(request_data['bulk_id']+ ".csv", self.user['username']) + " | Failed")
            return {"code":language.CODES['FAIL'], "msg":self.lang['wrong_file_format'], "data":[]}


    def process_csv(self, filename, uploaded_by,approved_by,branch, bulk_id):

        try:
            res=[]
            unique_id = ""
            voucher_hash = ""
            print("processing csv")

            with open(filename, "rb") as f:
                reader= unicodecsv.DictReader(f)
                #file upload is being read in a group in a dictionary{}
                print(reader)
                res=[x for x in reader]
            #     self.log.write_to_file(msg="In process_csv_reader {}".format(res),filename="event")
            # print(res)

            #reading the file in a format way for processing
            counter=1
            for trans in res:
                try:
                    #Converting the data in a dictionary form
                    trans = dict(trans)
                    self.logger.write_to_console("EVENT", "Processing: {}".format(trans))
                    print(trans)
                    #Converting the header of the file in lowercase for processing in key-value pair
                    for key, value in trans.items():

                        try:

                            print(key)
                            print(value)

                            if key.lower() == "id":
                                unique_id = bulk_id +"--"+ value

                            if key.lower() == "serial":
                                vhash = hashlib.sha256((value.encode()))
                                vhash = vhash.hexdigest()
                                voucher_hash = vhash

                        except Exception as e:
                            raise e
                            print(e)
                            error = str(e)
                            return error
                    
                    #sending request to the tups_portal(etienee' portal)
                    request_data = {
                          "unique_id": unique_id,
                          "voucher_hash": voucher_hash,
                          "uploaded_by":uploaded_by,
                          "approved_by":approved_by,
                          "branch":branch
                        }

                    self.logger.write_to_console("EVENT", "Adding voucher | {}".format(request_data))
                    api_response = self.model.add_voucher_new(request_data)
                    print(api_response)
                    # api_response = {"code": "00", "msg": "Response"}
                    self.logger.write_to_console("EVENT", "Adding serials response | {}".format(api_response))
                    #response from tups portal(etienne's portal) successfully save to tbl_bulk_transaction
                    
                    if api_response == True:
                        self.logger.write_to_console("EVENT", "Serial Adding Successful | {}".format(request_data))

                    #api_response from tups portal(etienne's portal) failed to be processed which is save to tbl_bulk_transaction
                    else:
                        self.logger.write_to_console("EVENT", "Registration Failed | {}".format(request_data))
                
                except Exception as e:
                    raise e
                    print(e)
                    error = str(e)
                    self.log.write_to_file(msg="In process_csv_error_exception {}".format(error),filename="error")
                    return error

            data = {"processing_status": "Completed", "processed_date": "NOW()", "bulk_id": bulk_id}
            result = self.model.updateBulkUpload(data)

            #####
            # Send Mail 
            #####
        

        except Exception as e:
            raise e
            error = "Processing of file failed"
            self.log.write_to_file(msg="In process_csv_exeception_raised_error {}".format(error),filename="error")
            return error


    def process_csv_new(self, filename, date_approved,approved_by,branch, bulk_id):

        try:
            res=[]
            unique_id = ""
            voucher_hash = ""
            print("processing csv")

            with open(filename, "rb") as f:
                reader= unicodecsv.DictReader(f)
                #file upload is being read in a group in a dictionary{}
                print(reader)
                res=[x for x in reader]
            #     self.log.write_to_file(msg="In process_csv_reader {}".format(res),filename="event")
            # print(res)

            #reading the file in a format way for processing
            counter=1
            for trans in res:
                try:
                    #Converting the data in a dictionary form
                    trans = dict(trans)
                    self.logger.write_to_console("EVENT", "Processing: {}".format(trans))
                    print(trans)
                    #Converting the header of the file in lowercase for processing in key-value pair
                    for key, value in trans.items():

                        try:

                            print(key)
                            print(value)

                            if key.lower() == "id":
                                unique_id = bulk_id +"--"+ value

                            if key.lower() == "serial":
                                vhash = hashlib.sha256((value.encode()))
                                vhash = vhash.hexdigest()
                                voucher_hash = vhash

                        except Exception as e:
                            raise e
                            print(e)
                            error = str(e)
                            return error
                    
                    #sending request to the tups_portal(etienee' portal)
                    request_data = {
                          "bulk_id": bulk_id,
                          "hashed_serial_number": voucher_hash,
                          "date_approved":date_approved,
                          "approved_by":approved_by,
                          "raw_serial_number":value,
                          "serial_status": "NOT VALIDATED",
                          "batch_id": counter
                        }
                    counter+=1

                    self.logger.write_to_console("EVENT", "Adding voucher | {}".format(request_data))
                    api_response = self.model.add_voucher_new(request_data)
                    print(api_response)
                    # api_response = {"code": "00", "msg": "Response"}
                    self.logger.write_to_console("EVENT", "Adding serials response | {}".format(api_response))
                    #response from tups portal(etienne's portal) successfully save to tbl_bulk_transaction
                    
                    if api_response == True:
                        self.logger.write_to_console("EVENT", "Serial Adding Successful | {}".format(request_data))

                    #api_response from tups portal(etienne's portal) failed to be processed which is save to tbl_bulk_transaction
                    else:
                        self.logger.write_to_console("EVENT", "Registration Failed | {}".format(request_data))
                
                except Exception as e:
                    raise e
                    print(e)
                    error = str(e)
                    self.log.write_to_file(msg="In process_csv_error_exception {}".format(error),filename="error")
                    return error

            data = {"processing_status": "Completed", "processed_date": "NOW()", "bulk_id": bulk_id}
            result = self.model.updateBulkUpload(data)

            #####
            # Send Mail 
            #####
        

        except Exception as e:
            raise e
            error = "Processing of file failed"
            self.log.write_to_file(msg="In process_csv_exeception_raised_error {}".format(error),filename="error")
            return error


    def searchvouchersRequests(self, request_data):
        """
            This function handles all logic related to login on the platform

            @Params : void
        """
        print(request_data)
 
        self.logger.write_to_console("EVENT", "Searching vouchers for {0}".format(request_data['search_param']))

        customer_data = self.model.searchvouchersReq(request_data)

        for result in customer_data:

            result["request_date"] = result["request_date"].strftime("%Y-%m-%d %H:%M:%S")

            # if result["status"] == 1:
            #     result["status"] = self.lang["active"]
            # else:
            #     result["status"] = self.lang["inactive"]
        
        return customer_data


    def generate_id(self, preamb):
        """
        Generate unique id
        Parameters: preamb => string to be used at the start of the id
        """
        t_id = preamb + str(hash(str(uuid.uuid1())) % 100000000000)
        return t_id


    def md5Checksum(self, fileName):
        filePath = os.path.join(config.UPLOAD_DIRECTORY, fileName)

        with open(filePath, 'rb') as fh:
            m = hashlib.md5()
            while True:
                data = fh.read()
                if not data:
                    break
                m.update(data)
        return m.hexdigest()
    
    def getVoucherByBulkId(self, bulk_id, request_data):
        if request_data == {}:
            request_data = {'offset':0, 'records':10}
        else:
            request_data['offset'] = int(request_data['page'])*10
            request_data['records'] = 10

        filter_data={}
        voucher_bulk_data = self.model.getVoucherByBulkId(bulk_id, request_data)
        filter_data['voucher_details'] = voucher_bulk_data[0]
        filter_data['pages'] = math.ceil(voucher_bulk_data[1][0]['count']/10)
        filter_data['branches'] = branch_data = self.model.getBranches()
        print(filter_data)
        return filter_data
    
    def updateBulkAssignSerialBranch(self, data):
        request_data = {
            "branch_assigned": data["branch_assigned"]
        }
        result = self.model.updateBulkAssignSerialBranch(request_data, data["bulk_id"], data["minRange"], data["maxRange"])
        if result == True:
            return {"code":language.CODES['SUCCESS'], "msg":"Serials successfully assigned to branch", "data":[]}
        else:
            return {"code":language.CODES['FAIL'], "msg":"Failed to assign serials to branch", "data":[]}
    
    def addDaysToDate(self, dateFormat="%Y-%m-%d %H:%M:%S", addDays=0):
        timeNow = datetime.datetime.now()
        anotherTime = timeNow + datetime.timedelta(days=addDays)
        return anotherTime.strftime(dateFormat)
    
    def getVerificationHistory(self, request_data):
        filter_data = {}

        if request_data == {}:
            request_data = {'offset':0, 'records':10, 'user_type': 'gen_public'}
        else:
            request_data['offset'] = int(request_data['page'])*10
            request_data['records'] = 10
            request_data['user_type'] = 'gen_public'
            print(str(request_data))

        all_data =  self.model.getVerificationHistory(request_data)    
        filter_data['history'] =  all_data[0]
        filter_data['pages'] = math.ceil(all_data[1][0]['count']/10)

        return filter_data

    def searchVerifiedVouchers(self, request_data):
        self.logger.write_to_console("EVENT", "Searching vouchers for {0}".format(request_data['search_param']))
        request_data['user_type'] = 'gen_public'
        voucher_data = self.model.searchVerifiedVouchers(request_data)
        print(voucher_data)
        
        return voucher_data

