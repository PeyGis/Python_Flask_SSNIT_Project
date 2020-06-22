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
from threading import Thread
import unicodecsv

from passlib.hash import sha256_crypt

from app import config
from app import language
from app.activities.models import Activities
# from app.admins.models import Administrator
# from app.institutions.models import Institution
from app.libs.logger import Logger
from app.libs.utils import Utilites

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


    def getAllActivities(self, request_data):
        """
            This function handles all logic related to login on the platform

            @Params : void
        """

        if request_data == {}:
            request_data = {'page': 0, 'fromdate': '', 'todate': ''}
        else:
            pass

        print(request_data)
 
        self.logger.write_to_console("EVENT", "loading all bulkpay uploads for {0}".format(self.user['username']))
        
        if request_data == {}:
            request_data = {'offset':0, 'records':11, 'fromdate':'', 'todate':'', 'status':''}
        else:
            request_data['offset'] = int(request_data['page'])*11
            request_data['records'] = 11

        customer_data = self.model.getAllActivities(request_data)
        print(customer_data)

        branch_data = self.model.getBranches()

        for result in customer_data[0]:

            result["date_created"] = result["date_created"].strftime("%Y-%m-%d %H:%M:%S")

            # if result["status"] == 1:
            #     result["status"] = self.lang["active"]
            # else:
            #     result["status"] = self.lang["inactive"]

        pages = math.ceil(customer_data[1][0]['count']/12)
        print(pages)

        self.logger.write_to_console("EVENT", "Administrators gotten | Success.")
        return {"code":language.CODES['SUCCESS'], "msg":self.lang['data_retrived'], "data":customer_data[0], "pages": pages, "branches": branch_data}
        return customer_data


    def getAllBlacklist(self, request_data):
        """
            This function handles all logic related to login on the platform

            @Params : void
        """

        if request_data == {}:
            request_data = {'page': 0, 'fromdate': '', 'todate': ''}
        else:
            pass

        print(request_data)
 
        self.logger.write_to_console("EVENT", "loading all customer request uploads for {0}".format(self.user['username']))
        
        if request_data == {}:
            request_data = {'offset':0, 'records':11, 'fromdate':'', 'todate':'', 'branch':'', 'request_type':''}
        else:
            request_data['offset'] = int(request_data['page'])*11
            request_data['records'] = 11

        customer_data = self.model.getAllBlack(request_data)
        print(customer_data)

        for result in customer_data[0]:

            result["date_blacklisted"] = result["date_blacklisted"].strftime("%Y-%m-%d %H:%M:%S")

            # if result["status"] == 1:
            #     result["status"] = self.lang["active"]
            # else:
            #     result["status"] = self.lang["inactive"]

        pages = math.ceil(customer_data[1][0]['count']/12)
        print(pages)

        self.logger.write_to_console("EVENT", "Administrators gotten | Success.")
        return {"code":language.CODES['SUCCESS'], "msg":self.lang['data_retrived'], "data":customer_data[0], "pages": pages}
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


    def addCustomer(self, request_data):
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

    def getUserActivities(self, request_data):
        """
            This function handles all logic related to login on the platform

            @Params : void
        """       
        self.logger.write_to_console("EVENT", "Getting customer request: {}".format(request_data))
        customer_data = self.model.getCustomerActivities(request_data)
        # self.logger.write_to_console("EVENT", "Get customer reponse: {}".format(customer_data))
        return customer_data

    def getCustomerDetials(self, customer_id):
        """
            This function handles all logic related to login on the platform
            @Params : void
        """       
        self.logger.write_to_console("EVENT", "Getting customer request: {}".format(customer_id))
        customer_data = self.model.getCustomer(customer_id)
        cust_accs_data = self.model.getCustomerAccounts(customer_id)
        cust_transactions_data = []

        for account in cust_accs_data:
            cust_transactions_data = cust_transactions_data + self.model.getCustomerTransactions(account['account_number'])

        cust_requests_data = self.model.getCustomerRequests(customer_id)
        cust_branches = self.model.getBranches()

        return {"code":language.CODES['SUCCESS'], "msg":self.lang['data_retrived'], "data":customer_data, "accounts": cust_accs_data, "transactions": cust_transactions_data, "requests": cust_requests_data, "branches": cust_branches}

    def getCustomerReqDetails(self, request_data):
        """
            This function handles all logic related to login on the platform

            @Params : void
        """       
        self.logger.write_to_console("EVENT", "Getting customer request: {}".format(request_data))
        customer_data = self.model.getCustomerRequestsByRequestId(request_data['request_id'])
        request_details = self.model.getNewCustomerRegistration(customer_data[0])
        # self.logger.write_to_console("EVENT", "Get customer reponse: {}".format(customer_data))
        for result in request_details:
            result["dob"] = result["dob"].strftime("%Y-%m-%d %H:%M:%S")
            result["request_date"] = result["request_date"].strftime("%Y-%m-%d %H:%M:%S")

        return request_details[0]

    def blockCustomerRequest(self, request_data):
        """
            This function handles all logic related to login on the platform

            @Params : void
        """
        self.logger.write_to_console("EVENT", "{0} Block Customer {1}".format(self.user['username'], str(request_data)))

        pending_requests = self.model.getCustomerRequests(request_data['customer_id'])

        if len(pending_requests) > 0:
            for reques in pending_requests:
                if reques['request_type'] == 7:
                    return {'code': '01', 'msg': 'Block request for user is already pending.'}


        result = self.model.addCustomerRequest({'requested_by': self.user['username'], 'request_type': '7', 'customer_msisdn': request_data['customer_id'], 'customer_account': request_data['customer_id'], 'branch': self.user['branch_id'] })
        self.logger.write_log("CUSTOMER", "Block Customer Request | {} | {} ".format(request_data['customer_id'], self.user['username']))
        
        return {'code': '00', 'msg': 'Request sent.'}


    def enableCustomerRequest(self, request_data):
        """
            This function handles all logic related to login on the platform

            @Params : void
        """
        self.logger.write_to_console("EVENT", "{0} Activate user Customer {1}".format(self.user['username'], str(request_data)))

        pending_requests = self.model.getCustomerRequests(request_data['customer_id'])

        if len(pending_requests) > 0:
            for reques in pending_requests:
                if reques['request_type'] == 8:
                    return {'code': '01', 'msg': 'Unblock user request for user is already pending.'}


        result = self.model.addCustomerRequest({'requested_by': self.user['username'], 'request_type': '8', 'customer_msisdn': request_data['customer_id'], 'customer_account': request_data['customer_id'], 'branch': self.user['branch_id'] })

        self.logger.write_log("CUSTOMER", "Unblock Customer Request | {} | {} ".format(request_data['customer_id'], self.user['username']))
        
        return {'code': '00', 'msg': 'Request sent.'}


    def resetPinRequest(self, request_data):
        """
            This function handles all logic related to login on the platform

            @Params : void
        """
        self.logger.write_to_console("EVENT", "{0} Customer Reset Pin {1}".format(self.user['username'], str(request_data)))

        pending_requests = self.model.getCustomerRequests(request_data['customer_id'])

        if len(pending_requests) > 0:
            for reques in pending_requests:
                if reques['request_type'] == 1:
                    return {'code': '01', 'msg': 'Reset pin request for customer is already pending.'}


        result = self.model.addCustomerRequest({'requested_by': self.user['username'], 'request_type': '1', 'customer_msisdn': request_data['customer_id'], 'customer_account': request_data['customer_id'], 'branch': self.user['branch_id'] })

        self.logger.write_log("CUSTOMER", "Reset Pin Request | {} | {} ".format(request_data['customer_id'], self.user['username']))
        
        return {'code': '00', 'msg': 'Request sent.'}


    def deactivateCustomerAccountRequest(self, request_data):
        """
            This function handles all logic related to login on the platform

            @Params : void
        """
        self.logger.write_to_console("EVENT", "{0} Deactivate Customer Account {1}".format(self.user['username'], str(request_data)))

        pending_requests = self.model.getCustomerRequests(request_data['customer_id'])

        if len(pending_requests) > 0:
            for reques in pending_requests:
                if reques['request_type'] == 4:
                    return {'code': '01', 'msg': 'Account Deactivation request for user is already pending.'}


        result = self.model.addCustomerRequest({'requested_by': self.user['username'], 'request_type': '4', 'customer_msisdn': request_data['customer_id'], 'customer_account': request_data['customer_id'], 'change_to': request_data['account_req'], 'branch': self.user['branch_id'] })

        self.logger.write_log("CUSTOMER", "Deactivate Customer Account Request | {} | {} | {} ".format(request_data['customer_id'], request_data['account_req'], self.user['username']))
        
        return {'code': '00', 'msg': 'Request sent.'}


    def activateCustomerAccountRequest(self, request_data):
        """
            This function handles all logic related to login on the platform

            @Params : void
        """
        self.logger.write_to_console("EVENT", "{0} Activate Customer Account {1}".format(self.user['username'], str(request_data)))

        pending_requests = self.model.getCustomerRequests(request_data['customer_id'])

        if len(pending_requests) > 0:
            for reques in pending_requests:
                if reques['request_type'] == 5:
                    return {'code': '01', 'msg': 'Account Deactivation request for user is already pending.'}


        result = self.model.addCustomerRequest({'requested_by': self.user['username'], 'request_type': '5', 'customer_msisdn': request_data['customer_id'],  'customer_account': request_data['customer_id'], 'change_to': request_data['account_req'], 'branch': self.user['branch_id'] })

        self.logger.write_log("CUSTOMER", "Activate Customer Account Request | {} | {} | {} ".format(request_data['customer_id'], request_data['account_req'], self.user['username']))
        
        return {'code': '00', 'msg': 'Request sent.'}


    def addCustomerAccountRequest(self, request_data):
        """
            This function handles all logic related to login on the platform

            @Params : void
        """
        self.logger.write_to_console("EVENT", "{0} Add Customer Account {1}".format(self.user['username'], str(request_data)))

        pending_requests = self.model.getCustomerRequests(request_data['customer_id'])

        if len(pending_requests) > 0:
            for reques in pending_requests:
                if reques['request_type'] == 6 and reques['change_to'] == request_data['new_account']:
                    return {'code': '01', 'msg': 'Add account request for user is already pending.'}


        result = self.model.addCustomerRequest({'requested_by': self.user['username'], 'request_type': '6', 'customer_msisdn': request_data['customer_id'], 'customer_account': request_data['customer_id'], 'change_to': request_data['new_account'], 'branch': self.user['branch_id'] })

        self.logger.write_log("CUSTOMER", "Add Customer Account Request | {} | {} | {} ".format(request_data['customer_id'], request_data['new_account'], self.user['username']))
        
        return {'code': '00', 'msg': 'Request sent.'}


    def updateCustomer(self, request_data):
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


    def declineCustomerRequest(self, request_data):
        """
            This function handles all logic related to login on the platform

            @Params : void
        """
        self.logger.write_to_console("EVENT", "{0} Add Customer Account {1}".format(self.user['username'], str(request_data)))

        pending_requests = self.model.getCustomerRequestsByRequestId(request_data['request_id'])
        print(pending_requests)
        if len(pending_requests) > 0:
            if pending_requests[0]['request_type'] == 0:
                #Remove from tbl_customer
                self.model.deleteCustomerNewCustomer(pending_requests[0]['customer_account'], pending_requests[0]['customer_msisdn'])
                #Remove from tbl_user_requests
                self.model.deleteCustomerRequest(request_data['request_id'])
                self.logger.write_log("CUSTOMER", "Customer Registration Declined | {} | {} | {} ".format(pending_requests[0]['customer_msisdn'], pending_requests[0]['customer_account'], self.user['username']))
                return {'code': '00', 'msg': 'Registration request declined successfully.'}
            else:
                #Remove from tbl_user_requests
                self.model.deleteCustomerRequest(request_data['request_id'])
                return {'code': '00', 'msg': 'Request declined successfully.'}
        else:
            self.model.deleteCustomerRequest(request_data['request_id'])
            return {'code': '01', 'msg': 'No request for found.'}


    def approveCustomerRequest(self, request_data):
        """
            This function handles all logic related to login on the platform

            @Params : void
        """
        self.logger.write_to_console("EVENT", "{0} Add Customer Account {1}".format(self.user['username'], str(request_data)))

        pending_requests = self.model.getCustomerRequestsByRequestId(request_data['request_id'])
        print(pending_requests)

        if len(pending_requests) > 0:
            if pending_requests[0]['request_type'] == 0:
                return self.registerNewUser(pending_requests[0])
            
            elif pending_requests[0]['request_type'] == 1:
                return self.changeUserPin(pending_requests[0])

            elif pending_requests[0]['request_type'] == 2:
                return self.changeUserPhoneNumber(pending_requests[0])

            elif pending_requests[0]['request_type'] == 3:
                return self.changeUserAccountNumber(pending_requests[0])

            elif pending_requests[0]['request_type'] == 4:
                return self.deactivateUserAccountNumber(pending_requests[0])

            elif pending_requests[0]['request_type'] == 5:
                return self.activateUserAccountNumber(pending_requests[0])

            elif pending_requests[0]['request_type'] == 6:
                return self.addUserAccountNumber(pending_requests[0])

            elif pending_requests[0]['request_type'] == 7:
                return self.deactivateUser(pending_requests[0])
            
            elif pending_requests[0]['request_type'] == 8:
                return self.activateUser(pending_requests[0])
            else:
                self.model.deleteCustomerRequest(request_data['request_id'])
                return {'code': '01', 'msg': 'No request for found.'}
        else:
            self.model.deleteCustomerRequest(request_data['request_id'])
            return {'code': '01', 'msg': 'No request for found.'}

    def registerNewUser(self, request_data):
        # GET User data
        customer_data = self.model.getNewCustomerRegistration(request_data)
        print(customer_data)
        # Send to Dari API to register
        result = self.model.sic_register_customer(customer_data[0])

        if result['code'] == '00':
            self.model.deleteCustomerNewCustomer(customer_data[0]['customer_account'], customer_data[0]['customer_msisdn'])
            self.model.deleteCustomerRequest(request_data['id'])
            self.logger.write_log("CUSTOMER", "Customer Registration Approved | {} | {} | {} ".format(customer_data[0]['customer_msisdn'], customer_data[0]['customer_account'], self.user['username']))
            return {'code': '00', 'msg':"Customer registration approved"}
        else:
            return {'code': '01', 'msg': result['msg']}


    def changeUserPin(self, request_data):
        # GET User data
        customer_data = self.model.getCustomer(request_data['customer_account'])
        print(customer_data)
        # Send to Dari API to register
        result = self.model.sic_reset_customer_pin(customer_data[0])

        if result['code'] == '00':
            self.model.deleteCustomerRequest(request_data['id'])
            self.logger.write_log("CUSTOMER", "Approved Change Pin | {} | {} ".format(customer_data[0]['id'], self.user['username']))
            return {'code': '00', 'msg':"Customer pin reset sucessful."}
        else:
            return {'code': '01', 'msg': result['msg']}


    def changeUserPhoneNumber(self, request_data):
        # GET User data
        res = False
        customer_data = self.model.getCustomer(request_data['customer_account'])
        customer_accs = self.model.getCustomerAccounts(request_data['customer_account'])
        print(customer_data)
        print(customer_accs)

        for account in customer_accs:
            # Send to Dari API to register
            result = self.model.fusion_deactivate_customer({'msisdn': customer_data[0]['msisdn'], 'uniqueID': customer_data[0]['account']})
            print(result)
            if result['code'] == '00':
                reg_result = self.model.fusion_register_customer({'msisdn': request_data['change_to'], 'uniqueID': customer_data[0]['account']})
                print(reg_result)
                if reg_result['code'] == '00':
                    res = True
            else:
                pass

        if res == True:
            self.model.updatevouchers({'id': customer_data['id'], 'msisdn': request_data['change_to']})
            self.model.deleteCustomerRequest(request_data['id'])
            self.logger.write_log("CUSTOMER", "Approved Change Phone Number | {} | from: {} | to: {} | {} ".format(customer_data[0]['msisdn'], customer_data[0]['msisdn'], request_data['change_to'], self.user['username']))
            return {'code': '00', 'msg':"Customer phone number change sucessful."}
        else:
            self.model.deleteCustomerRequest(request_data['id'])
            return {'code': '01', 'msg':"Customer phone number change failed."}


    def changeUserAccountNumber(self, request_data):
        # GET User data 
        customer_data = self.model.getCustomer(request_data['customer_account'])
        print(customer_data)
        # Send to Dari API to register
        # result = self.model.sic_reset_customer_pin(customer_data[0])

        # if result['code'] == '00':
        self.model.deleteCustomerRequest(request_data['id'])
        return {'code': '00', 'msg':"Customer account changed successfully."}
        # else:
        #     return {'code': '01', 'msg': result['msg']}

    def deactivateUserAccountNumber(self, request_data):
        # GET User data
        # customer_data = self.model.getCustomer(request_data['customer_account'])
        # customer_accs = self.model.getCustomerAccounts(request_data['customer_account'])
        # print(customer_data)
        # print(customer_accs)
        # result = None
        # acc_id = None

        # # Send to Dari API to register
        # for account in customer_accs:
        #     if account['account_number'] == request_data['change_to']:
        #         acc_id = account['id']
        #         result = self.model.fusion_deactivate_customer({'msisdn': request_data['change_to'], 'uniqueID': customer_data[0]['account']})
        #         break

        # if result['code'] == '00':
        #     self.model.updateCustomerAccount({'id': acc_id, 'status': 'INACTIVE'})
        #     self.model.deleteCustomerRequest(request_data['id'])
        #     return {'code': '00', 'msg':"Customer deactivation successful."}
        # else:
        #     return {'code': '01', 'msg': result['msg']}
        # GET User data
        customer_data = self.model.getCustomer(request_data['customer_account'])
        print(customer_data)
        # Send to Dari API to register
        result = self.model.sic_change_customer_account_status(request_data, "INACTIVE")

        if result['code'] == '00':
            self.model.deleteCustomerRequest(request_data['id'])
            self.logger.write_log("CUSTOMER", "Approved Change Pin | {} | {} ".format(customer_data[0]['id'], self.user['username']))
            return {'code': '00', 'msg':"Customer account has been blocked."}
        else:
            return {'code': '01', 'msg': result['msg']}

    def activateUserAccountNumber(self, request_data):
        # GET User data
        # customer_data = self.model.getCustomer(request_data['customer_account'])
        # customer_accs = self.model.getCustomerAccounts(request_data['customer_account'])
        # print(customer_data)
        # print(customer_accs)
        # result = None
        # acc_id = None

        # Send to Dari API to register
        # for account in customer_accs:
        #     if account['account_number'] == request_data['change_to']:
        #         acc_id = account['id']
        #         result = self.model.fusion_activate_customer({'msisdn': request_data['change_to'], 'uniqueID': customer_data[0]['account']})
        #         break

        # if result['code'] == '00':
        #     self.model.updateCustomerAccount({'id': acc_id, 'status': 'ACTIVE'})
        #     self.model.deleteCustomerRequest(request_data['id'])
        #     return {'code': '00', 'msg':"Customer account activation successful."}
        # else:
        #     return {'code': '01', 'msg': result['msg']}
        customer_data = self.model.getCustomer(request_data['customer_account'])
        print(customer_data)
        # Send to Dari API to register
        result = self.model.sic_change_customer_account_status(request_data, "ACTIVE")

        if result['code'] == '00':
            self.model.deleteCustomerRequest(request_data['id'])
            self.logger.write_log("CUSTOMER", "Approved Account Activation | {} | {} | {} ".format(customer_data[0]['id'], request_data['change_to'], self.user['username']))
            return {'code': '00', 'msg':"Customer account has been blocked."}
        else:
            return {'code': '01', 'msg': result['msg']}

    def addUserAccountNumber(self, request_data):
        # GET User data
        customer_data = self.model.getCustomer(request_data['customer_account'])
        print(customer_data)
        # Send to Dari API to register
        result = self.model.fusion_register_customer({'msisdn': customer_data[0]['msisdn'], 'uniqueID': request_data[0]['change_to']})

        if result['code'] == '00':
            self.model.deleteCustomerRequest(request_data['id'])
            self.logger.write_log("CUSTOMER", "Approved Account Activation | {} | {} | {} ".format(customer_data[0]['id'], request_data['change_to'], self.user['username']))
            return {'code': '00', 'msg':"Customer account added sucessfully."}
        else:
            return {'code': '01', 'msg': result['msg']}

    def deactivateUser(self, request_data):
        # GET User data
        customer_data = self.model.getCustomer(request_data['customer_account'])
        print(customer_data)
        # Send to Dari API to register
        result = self.model.sic_change_customer_status(customer_data[0], "INACTIVE")

        if result['code'] == '00':
            self.model.deleteCustomerRequest(request_data['id'])
            self.logger.write_log("CUSTOMER", "Approved Account Deactivation | {} | {} | {} ".format(customer_data[0]['id'], request_data['change_to'], self.user['username']))
            return {'code': '00', 'msg':"Customer account has been blocked."}
        else:
            return {'code': '01', 'msg': result['msg']}

    def activateUser(self, request_data):
        # GET User data
        customer_data = self.model.getCustomer(request_data['customer_account'])
        print(customer_data)
        # Send to Dari API to register
        result = self.model.sic_change_customer_status(customer_data[0], "ACTIVE")

        if result['code'] == '00':
            self.model.deleteCustomerRequest(request_data['id'])
            return {'code': '00', 'msg':"Customer account has been unblocked."}
        else:
            return {'code': '01', 'msg': result['msg']}
        

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
            request_data = {'offset':0, 'records':11, 'fromdate':'', 'todate':'', 'request_type':''}
        else:
            request_data['offset'] = int(request_data['page'])*11
            request_data['records'] = 11

        customer_data = self.model.getAllUploads(request_data)
        print(customer_data)

        for result in customer_data[0]:

            result["upload_date"] = result["upload_date"].strftime("%Y-%m-%d %H:%M:%S")

            if result["processed_date"] != None:
                result["processed_date"] = result["processed_date"].strftime("%Y-%m-%d %H:%M:%S")

            if result["approved_date"] != None:
                result["approved_date"] = result["approved_date"].strftime("%Y-%m-%d %H:%M:%S")


        pages = math.ceil(customer_data[1][0]['count']/12)
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
            self.logger.write_log("CUSTOMER", "Uploaded Bulk Registration | {} | {} ".format(fields['bulk_id'], self.user['username']))
            return {"code":language.CODES['SUCCESS'], "msg":self.lang['file_recorded'], "data":[]}
        else:
            return {"code":language.CODES['FAIL'], "msg":self.lang['wrong_file_format'], "data":[]}

    def approve_uploaded_file(self, request_data):
        self.logger.write_to_console("EVENT", "Recording Uploaded file | {}".format(request_data['bulk_id']))

        bulk_details = self.model.getBulkUploadDetails(request_data['bulk_id'])

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
            self.logger.write_to_console("EVENT", "Starting processing Thread for | {}".format(request_data['bulk_id']))
            processing_thread = Thread(target=self.process_csv, args=(os.path.join(config.UPLOAD_DIRECTORY, request_data['bulk_id']+".csv"), request_data['bulk_id'], self.user['username'], bulk_details[0]['uploaded_by'], request_data['bulk_id']))
            processing_thread.start()
            self.logger.write_to_console("EVENT", "Thread started for | {}".format(request_data['bulk_id']))

            self.logger.write_log("CUSTOMER", "Approved Bulk Registration | {} | {} ".format(request_data['bulk_id'], self.user['username']))
            return {"code":language.CODES['SUCCESS'], "msg": "File processing approved.", "data":[]}
        else:
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
            self.logger.write_log("CUSTOMER", "Decline Bulk Registration | {} | {} ".format(request_data['bulk_id'], self.user['username']))
            return {"code":language.CODES['SUCCESS'], "msg": "File processing declined.", "data":[]}
        else:
            return {"code":language.CODES['FAIL'], "msg":self.lang['wrong_file_format'], "data":[]}


    def process_csv(self, upload_id, filename, username, uploaded_by, bulk_id):

        try:
            res=[]
            first_name = ""
            last_name = ""
            middle_name = ""
            dob = ""
            gender = ""
            region = ""
            city = ""
            msisdn = ""
            uniqueid = ""
            registered_by = username
            print("processing csv")

            with open(upload_id, "rb") as f:
                reader= unicodecsv.DictReader(f)
                #file upload is being read in a group in a dictionary{}
                print(reader)
                res=[x for x in reader]
            #     self.log.write_to_file(msg="In process_csv_reader {}".format(res),filename="event")
            # print(res)

            #reading the file in a format way for processing
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

                            if key.lower() == "first_name":
                                first_name = value

                            if key.lower() == "last_name":
                                last_name = value

                            if key.lower() == "middle_name":
                                middle_name = value

                            if key.lower() == "dob":
                                dob = value

                            if key.lower() == "gender":
                                gender = value

                            if key.lower() == "region":
                                region = value

                            if key.lower() == "city":
                                city = value

                            if key.lower() == "msisdn":
                                msisdn = value

                            if key.lower() == "uniqueid":
                                uniqueid = value

                        except Exception as e:
                            raise e
                            print(e)
                            error = str(e)
                            return error
                    
                    #sending request to the tups_portal(etienee' portal)
                    request_data = {
                          "action": "register",
                          "uniqueid": uniqueid,
                          "msisdn": msisdn,
                          "firstname": first_name,
                          "lastname": last_name,
                          "middlename": middle_name,
                          "dob": dob,
                          "gender": gender,
                          "region": region,
                          "city": city,
                          "requestedBy": uploaded_by,
                          "requestBranch": uniqueid[:3]
                        }

                    self.logger.write_to_console("EVENT", "Sending registrations request | {}".format(request_data))
                    api_response = self.model.sic_bulk_register_customer(request_data)
                    print(api_response)
                    # api_response = {"code": "00", "msg": "Response"}
                    self.logger.write_to_console("EVENT", "Registration response | {}".format(api_response))
                    #response from tups portal(etienne's portal) successfully save to tbl_bulk_transaction
                    
                    if api_response["code"]=="00":
                        self.logger.write_to_console("EVENT", "Registration Successful | {}".format(request_data))

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
