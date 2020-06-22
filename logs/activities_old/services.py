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
from app.activities.models import Activities
from app.libs.logger import Logger

class activitiesServices(object):
    """
        Class contains functions and attributes for authtentication
        Function: * getCampainge(sel)
    """
    def __init__(self, user):
        self.lang = {}
        self.lang = getattr(language, config.DEFAULT_LANG)
        self.user = user
        self.model = Activities(user)
        self.logger = Logger()


    def getAllactivities(self, request_data):
        """
            This function handles all logic related to login on the platform

            @Params : void
        """

        request_data['page'] = int(request_data['page'])-1
        if request_data == {}:
            request_data = {'offset':0, 'records':12, 'fromdate':'', 'todate':'', 'status': '', 'branch': '', 'destination': '', 'tag': '', 'type': ''}
        else:
            request_data['offset'] = int(request_data['page'])*12
            request_data['records'] = 12

        print(request_data)
 
        self.logger.write_to_console("EVENT", "loading all transactions for {0}".format(self.user['username']))
        
        if request_data['fromdate'] != "":
            request_data['start_date'] = request_data['fromdate'] + " 00:00:00"

        if request_data['todate'] != "":
            request_data['end_date'] = request_data['todate'] + " 23:59:59"

        # transaction_data = api_calls.request_api_json(api_calls, request)
        # if self.user['name'] == "Administrator":
        transaction_data = self.model.getAllTransactions(request_data)
        # else:
        #     transaction_data = self.model.getAllTransactionsByBranch(request_data)

        for transaction in transaction_data[0]:
            transaction['amount'] = str(transaction['amount'])
            transaction['request_time'] = str(transaction['request_time'])
            transaction['response_time'] = str(transaction['response_time'])

        transaction_data[1][0]['count'] = int(round(transaction_data[1][0]['count']/12))

        return transaction_data

    def searchActivities(self, request_data):
        """
            This function handles all logic related to login on the platform

            @Params : void
        """
        print(request_data)
 
        self.logger.write_to_console("EVENT", "Searching Activities for {0}".format(request_data['search_param']))

        transaction_data = self.model.searchTransactions(request_data)

        # print(transaction_data)

        for transaction in transaction_data:
            transaction['amount'] = str(transaction['amount'])
            transaction['request_time'] = str(transaction['request_time'])
            transaction['response_time'] = str(transaction['response_time'])
        
        return transaction_data

    def getAllActivitiesExport(self, request_data):
        """
            This function handles all logic related to login on the platform

            @Params : void
        """

        if request_data == {}:
            request_data = {'offset':0, 'records':12, 'fromdate':'', 'todate':'', 'status': '', 'branch': '', 'destination': '', 'tag': '', 'type': ''}
        else:
            request_data['offset'] = 0
            request_data['records'] = 100000

        print(request_data)
 
        self.logger.write_to_console("EVENT", "Exporting transactions for {0}".format(self.user['username']))
        
        if self.user['name'] == 'Administrator':
            transaction_data = self.model.getAllTransactions(request_data)
        else:
            transaction_data = self.model.getAllTransactions(request_data)

        export_list = [['TRANSACTION ID', 'REFERENCE', 'SOURCE ACCOUNT', 'BRANCH','DESTINATION ACCOUNT','DESTINATION', 'MSISDN', 'AMOUNT', 'TYPE', 'TAG', 'STATUS', 'REQUEST DATE', 'RESPONSE DATE']]

        for result in transaction_data[0]:
            result["request_time"] = result["request_time"].strftime("%Y-%m-%d %H:%M:%S")
            result["response_time"] = result["response_time"].strftime("%Y-%m-%d %H:%M:%S")
            
            result["amount"] = str(result["amount"])

            export_list.append([result['xref'], result['reference'], result['account_number'], result['account_branch'], result['des_act'], result['destination'], result['msisdn'], result['amount'], result['type'], result['fusion_tag'], result['msg_stat'], result['request_time'], result['response_time']])

        print(export_list)
        return export_list


    def getActivitiesfilter(self):
        """
            This function handles all logic related to login on the platform

            @Params : void
        """
 
        self.logger.write_to_console("EVENT", "loading all transaction filter options for {0}".format(self.user['username']))

        # transaction_data = api_calls.request_api_json(api_calls, request)
        if self.user['branch_code'] == "All":
            filter_data = self.model.getAllTransactionsfilter()
        else:
            filter_data = self.model.getAllTransactionsfilter()

        return filter_data




    def getUploadDetails(self, request_data):
        """
            This function handles all logic related to login on the platform

            @Params : void
        """
        self.logger.write_to_console("EVENT", "Getting details for {0}".format(request_data['bulk_id']))
        
        detailed_data = self.model.getBulkUploadDetailsByBulkId(request_data['bulk_id'])

        print(detailed_data)
        for result in detailed_data:
            result["date_processed"] = result["date_processed"].strftime("%Y-%m-%d %H:%M:%S")
            result["date_upload"] = result["date_upload"].strftime("%Y-%m-%d %H:%M:%S")

            if result["approval_status"] == 0:
                result["approval_status"] = self.lang["not_submitted"]
            elif result["approval_status"] == 1:
                result["approval_status"] = self.lang["submitted"]
            elif result["approval_status"] == 2:
                result["approval_status"] = self.lang["Declined"]
            elif result["approval_status"] == 3:
                result["approval_status"] = self.lang["approved"]
            elif result["approval_status"] == 4:
                result["approval_status"] = self.lang["corrupt_file"]
            else:
                result["processing_status"] = self.lang["unknown"]

            if result["processing_status"] == 0:
                result["processing_status"] = self.lang["not_processed"]
            elif result["processing_status"] == 1:
                result["processing_status"] = self.lang["initiated"]
            elif result["processing_status"] == 2:
                result["processing_status"] = self.lang["failed"]
            elif result["processing_status"] == 3:
                result["processing_status"] = self.lang["success"]
            else:
                result["processing_status"] = self.lang["unknown"]
            pass

        self.logger.write_to_console("EVENT", "BulkPay Uploads gotten | Success.")
        return {"code":language.CODES['SUCCESS'], "msg":self.lang['data_retrived'], "data":detailed_data}


    def record_uploaded_file(self, file_obl):
        self.logger.write_to_console("EVENT", "BulkPay Recording Uploaded file | {}".format(file_obl.filename))

        file_extension = file_obl.filename.split(".")
        # filetype = file_extension[-1]
        if file_extension[-1] != "csv":
            return {"code":language.CODES['FAIL'], "msg":self.lang['wrong_file_format'], "data":[]}
        
        bulk_id = self.generate_id(self.user['institution_shortName'])
        # file_obl.save(secure_filename(file_obl.filename))
        file_obl.save(os.path.join(config.UPLOAD_DIRECTORY, bulk_id+".csv"))
        fileChecksum = self.md5Checksum(bulk_id+".csv")
        fileSize = os.stat(os.path.join(config.UPLOAD_DIRECTORY, bulk_id+".csv")).st_size

        fields = {"bulk_id":bulk_id, \
                      "filename": file_obl.filename, \
                      "filesize": fileSize, \
                      "fileType": file_extension[-1], \
                      "file_checksum": fileChecksum, \
                      "merchant_id": self.user['institution_data']['id'], \
                      "merchant_admin_id": self.user['id'], \
                      "approval_status": '1', \
                      "date_upload": "NOW()", \
                }

        self.logger.write_to_console("EVENT", "BulkPay File Details | {}".format(fields))

        result = self.model.insertBulkUpload(fields)
        if result == True:
            result = self.model.insertBulkUploadXtraDetails({"bulk_id":bulk_id})
            if result == True:
                return {"code":language.CODES['SUCCESS'], "msg":self.lang['file_recorded'], "data":[]}
        else:
            return {"code":language.CODES['FAIL'], "msg":self.lang['wrong_file_format'], "data":[]}

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

    
    def generate_id(self, preamb):
        """
        Generate unique id
        Parameters: preamb => string to be used at the start of the id
        """
        t_id = preamb + str(hash(str(uuid.uuid1())) % 100000000000)
        return t_id