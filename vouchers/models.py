import json
from app.libs.mysqllib import MysqlLib
from app.libs.api_calls import ApiCalls
from app.libs.security import AESCipher
from app.config import API_URL, FUSION_URL, VA_URL, FS_INST_APIKEY, FS_INST_ID

class Vouchers(object):
    """docstring for UserFunctions"""
    def __init__(self, user):
        super(Vouchers, self).__init__()
        self.dbconn = MysqlLib()
        self.user = user
        self.API = ApiCalls()


    def getAllVouchers(self, request_params):

        where_con_list = []
        where_con = ''

        if 'status' in request_params and request_params['status'] != "" and request_params['status'] != "All":
            where_con_list.append("status='{}' ".format(request_params['status']))

        if 'user_msisdn' in request_params and request_params['user_msisdn'] != "" and request_params['user_msisdn'] != "All":
            where_con_list.append("user_msisdn='{}' ".format(request_params['user_msisdn']))

        where_con = " and ".join(where_con_list)
        if where_con == "":
            where_con = "1"

        if request_params['fromdate'] == "" or request_params['todate'] == "":
            print("Yess Herreeee")
            data = self.dbconn.select_from_table_paged("tbl_vouchers", condition=" WHERE "+ where_con +" ORDER BY date_uploaded DESC", offset=request_params['offset'], records=request_params['records'])
            data_count = self.dbconn.select_count_table("tbl_vouchers", condition="WHERE "+ where_con)
        else:
            data = self.dbconn.select_from_table_paged("tbl_vouchers", condition=" WHERE "+ where_con +" AND date_uploaded between '{0}' and '{1}' ORDER BY date_uploaded DESC".format(request_params['fromdate'], request_params['todate']), offset=request_params['offset'], records=request_params['records'])
            data_count = self.dbconn.select_count_table("tbl_vouchers", condition="WHERE "+ where_con)
        return [data, data_count]


    def getAllCustomerReqs(self, request_params):

        where_con_list = []
        where_con = ''

        if 'request_type' in request_params and request_params['request_type'] != "" and request_params['request_type'] != "All":
            where_con_list.append("request_type='{}' ".format(request_params['request_type']))

        if 'branch' in request_params and request_params['branch'] != "" and request_params['branch'] != "All":
            where_con_list.append("rbranch='{}' ".format(request_params['branch']))

        where_con = " and ".join(where_con_list)
        if where_con == "":
            where_con = "1"

        if request_params['fromdate'] == "" or request_params['todate'] == "":
            print("Yess Herreeee")
            data = self.dbconn.select_from_table_paged("tbl_user_requests", condition=" WHERE "+ where_con +" ORDER BY request_date DESC", offset=request_params['offset'], records=request_params['records'])
            data_count = self.dbconn.select_count_table("tbl_user_requests", condition="WHERE "+ where_con)
        else:
            data = self.dbconn.select_from_table_paged("tbl_user_requests", condition=" WHERE "+ where_con +" AND request_date between '{0}' and '{1}' ORDER BY request_date DESC".format(request_params['fromdate'], request_params['todate']), offset=request_params['offset'], records=request_params['records'])
            data_count = self.dbconn.select_count_table("tbl_user_requests", condition="WHERE "+ where_con)
        return [data, data_count]

    def getAllUploads(self, request_params):

        where_con_list = []
        where_con = ''

        if 'branch' in request_params and request_params['branch'] != "" and str(request_params['branch']).lower() != "all":
            where_con_list.append("branch='{}' ".format(request_params['branch']))

        where_con = " and ".join(where_con_list)
        if where_con == "":
            where_con = "1"

        if request_params['fromdate'] == "" or request_params['todate'] == "":
            print("Yess Herreeee")
            data = self.dbconn.select_from_table_paged("tbl_uploads", condition=" WHERE "+ where_con +" ORDER BY upload_date DESC", offset=request_params['offset'], records=request_params['records'])
            data_count = self.dbconn.select_count_table("tbl_uploads", condition="WHERE "+ where_con)
        else:
            data = self.dbconn.select_from_table_paged("tbl_uploads", condition=" WHERE "+ where_con +" AND upload_date between '{0}' and '{1}' ORDER BY upload_date DESC".format(request_params['fromdate'], request_params['todate']), offset=request_params['offset'], records=request_params['records'])
            data_count = self.dbconn.select_count_table("tbl_uploads", condition="WHERE "+ where_con)
        return [data, data_count]

    def getVoucherById(self, customer_id):
        data = self.dbconn.select_from_table_paged("tbl_vouchers", condition=" WHERE id='{}' ORDER BY date_uploaded DESC".format(customer_id))
        return data

    def getVoucherByHash(self, vhash):
        print(vhash)
        data = self.dbconn.select_from_table_paged("tbl_vouchers", condition=" WHERE voucher_hash='{}' ORDER BY date_uploaded DESC".format(vhash))
        print(data)
        return data

    def getVoucherByBulkId(self, bulk_id, request_params):
        if request_params['serial_status'] == "" and request_params['branch_assigned'] == "":
            data = self.dbconn.select_from_table_paged('tbl_serials', condition = " WHERE bulk_id= '{}'".format(bulk_id), offset=request_params['offset'], records=request_params['records'])
            data_count = self.dbconn.select_count_table('tbl_serials', condition = "WHERE bulk_id= '"+ bulk_id +"'")
        elif request_params['serial_status'] == "All" and request_params['branch_assigned'] is not "None":
            data = self.dbconn.select_from_table_paged('tbl_serials', condition = " WHERE bulk_id='{0}' AND branch_assigned='{1}'".format(bulk_id, request_params['branch_assigned']), offset=request_params['offset'], records=request_params['records'])
            data_count = self.dbconn.select_count_table('tbl_serials', condition = " WHERE bulk_id='{0}' AND branch_assigned='{1}'".format(bulk_id, request_params['branch_assigned']))
        elif request_params['serial_status'] is not "All" and request_params['branch_assigned'] == "None":
            data = self.dbconn.select_from_table_paged('tbl_serials', condition = " WHERE bulk_id='{0}' AND serial_status='{1}'".format(bulk_id, request_params['serial_status']), offset=request_params['offset'], records=request_params['records'])
            data_count = self.dbconn.select_count_table('tbl_serials', condition = " WHERE bulk_id='{0}' AND serial_status='{1}'".format(bulk_id, request_params['serial_status']))
        elif request_params['serial_status'] == "All" and request_params['branch_assigned'] == "None":
            data = self.dbconn.select_from_table_paged('tbl_serials', condition = " WHERE bulk_id='{0}'".format(bulk_id), offset=request_params['offset'], records=request_params['records'])
            data_count = self.dbconn.select_count_table('tbl_serials', condition = " WHERE bulk_id='{0}'".format(bulk_id))
        else:
            data = self.dbconn.select_from_table_paged('tbl_serials', condition = " WHERE bulk_id='{0}' AND branch_assigned='{1}' AND serial_status='{2}'".format(bulk_id, request_params['branch_assigned'], request_params['serial_status']), offset=request_params['offset'], records=request_params['records'])
            data_count = self.dbconn.select_count_table('tbl_serials', condition = " WHERE bulk_id='{0}' AND branch_assigned='{1}' AND serial_status='{2}'".format(bulk_id, request_params['branch_assigned'], request_params['serial_status']))
        return [data, data_count]

    def getCustomerAccounts(self, customer_id):
        data = self.dbconn.select_from_table_paged("tbl_customer_account", ["id", "account_number", "branch", "status"], " WHERE customer='{}'".format(customer_id))
        return data

    def getCustomerTransactions(self, customer_acc):
        data = self.dbconn.select_from_table_paged("tbl_transactions", condition=" WHERE account_number='{0}' or des_act='{0}' ORDER BY request_time DESC".format(customer_acc))
        return data

    def getCustomerRequests(self, customer_id):
        data = self.dbconn.select_from_table_paged("tbl_user_requests", condition=" WHERE customer_account='{}' ORDER BY request_date DESC".format(customer_id))
        return data

    def getNewCustomerRegistration(self, request_data):
        data = self.dbconn.select_from_table_paged("tbl_details_change", condition=" WHERE customer_account='{}' AND customer_msisdn='{}' ORDER BY request_date DESC".format(request_data['customer_account'], request_data['customer_msisdn']))
        return data

    def getCustomerRequestsByRequestId(self, request_id):
        data = self.dbconn.select_from_table_paged("tbl_user_requests", condition=" WHERE id={} ORDER BY request_date DESC".format(request_id))
        return data

    def addCustomerRequest(self, data):
        response = self.dbconn.insert_in_table("tbl_user_requests", data)
        return response

    def updateVoucher(self, data):
        admin = self.dbconn.update_table("tbl_vouchers", data, "WHERE unique_id='{}'".format(data['unique_id']))
        return admin

    def getSerialByHash(self, vhash):
        data = self.dbconn.select_from_table('tbl_serials', condition = "WHERE hashed_serial_number= '{}' ORDER BY date_approved DESC".format(vhash))
        return data

    def updateSerial(self, data):
        data = self.dbconn.update_table("tbl_serials", data, "WHERE serial_id='{}'".format(data['serial_id']))
        return data

    def getValidatorByMsisdn(self, msisdn):
        validator = self.dbconn.select_from_table('tbl_validators', condition = "WHERE msisdn= '"+ msisdn +"'")
        return validator

    def updateCustomerAccount(self, data):
        admin = self.dbconn.update_table("tbl_customer_account", data, "WHERE id='{}'".format(data['id']))
        return admin

    def searchCustomers(self, request_params):
        search_data = self.dbconn.search_table(request_params['search_param'], "tbl_customers", ["id", "first_name", "middle_name", "last_name", "gender", "status", "join_date"])
        print(search_data)
        return search_data

    def searchCustomersReq(self, request_params):
        search_data = self.dbconn.search_table(request_params['search_param'], "tbl_user_requests", ["id", "requested_by", "request_type", "customer_msisdn", "customer_account", "change_to", "change_from", "request_date", "approved_by", "approve_date", "branch"])
        print(search_data)
        return search_data

    def getBranches(self):
        data = self.dbconn.select_from_table("tbl_branches")
        return data

    def deleteCustomerRequest(self, request_id):
        data = self.dbconn.delete_from_table("tbl_user_requests", condition=" WHERE id={}".format(request_id))
        return data

    def deleteCustomerNewCustomer(self, customer_account, customer_msisdn):
        data = self.dbconn.delete_from_table("tbl_details_change", condition=" WHERE customer_account='{}' and customer_msisdn='{}'".format(customer_account, customer_msisdn))
        return data

    def addNewRegistrationRequest(self, data):
        response = self.dbconn.insert_in_table("tbl_details_change", data)
        return response

    def insertBulkUpload(self, data):
        admin = self.dbconn.insert_in_table("tbl_uploads",data)
        return True

    def updateBulkUpload(self, data):
        print("special data")
        print(data)
        admin = self.dbconn.update_table("tbl_uploads", data, "WHERE bulk_id='{}'".format(data['bulk_id']))
        return admin

    def getBulkUploadDetails(self, request_id):
        data = self.dbconn.select_from_table_paged("tbl_uploads", condition=" WHERE bulk_id='{}'".format(request_id))
        return data

    def add_voucher(self, data):
        response = self.dbconn.insert_in_table("tbl_vouchers", data)
        return response

    def add_voucher_new(self, data):
        response = self.dbconn.insert_in_table("tbl_serials", data)
        return response

    def updateBulkAssignSerialBranch(self, data, bulk_id, minRange, maxRange):
        data = self.dbconn.update_table("tbl_serials", data,  condition=" WHERE bulk_id='{}' and batch_id between '{}' and '{}'".format(bulk_id, minRange, maxRange))
        return data

    def add_user_activity(self, data):
        response = self.dbconn.insert_in_table("tbl_activity_log", data)
        return response

    def addBlacklist(self, data):
        response = self.dbconn.insert_in_table("tbl_black_list", data)
        return response


    #API CALLS
    def sic_register_customer(self, user_data):
        request_data = {
                          "action": "register",
                          "uniqueid": user_data['customer_account'],
                          "msisdn": user_data['customer_msisdn'],
                          "firstname": user_data['new_fname'],
                          "lastname": user_data['new_lname'],
                          "middlename": user_data['new_mname'],
                          "dob": user_data['dob'].strftime("%Y-%m-%d"),
                          "gender": user_data['new_gender'],
                          "region": user_data['region'],
                          "city": user_data['city'],
                          "requestedBy": self.user['username'],
                          "requestBranch": self.user['branch_id']
                        }

        req_data = {'model':"bankClient", 'func':"register", 'args':request_data}
        print(request_data)
        encryptor = AESCipher()
        encoded_data = encryptor.encrypt(json.dumps(req_data))
        print(encoded_data)
        # response_data = self.API.send_socket_data(encoded_data)
        # response_data = self.API.request_api_raw_json(encoded_data, url=API_URL, method='post', headers={"Authorization": "21d39021fc624f309fd9d41332e34rt5f"})
        response_data = b'/MuglLXPw5C22iTP3W7aBWdHYpaToXvBOmSLmxB0ClX/PxrGHSarwj3TtE95R7LD'
        print(response_data)
        resp_data = encryptor.decrypt(response_data)
        print(resp_data)
        resp_data = json.loads(resp_data.decode('UTF-8'))
        print(resp_data)
        print(type(resp_data))
        # data = {'code': '00', 'msg': 'Registration successful.'}
        # print(data)
        return resp_data

    def sic_bulk_register_customer(self, request_data):
    
        req_data = {'model':"bankClient", 'func':"register", 'args':request_data}
        print(request_data)
        encryptor = AESCipher()
        encoded_data = encryptor.encrypt(json.dumps(req_data))
        print(encoded_data)
        # response_data = self.API.send_socket_data(encoded_data)
        # response_data = self.API.request_api_raw_json(encoded_data, url=API_URL, method='post', headers={"Authorization": "21d39021fc624f309fd9d41332e34rt5f"})
        response_data = b'/MuglLXPw5C22iTP3W7aBWdHYpaToXvBOmSLmxB0ClX/PxrGHSarwj3TtE95R7LD'
        print(response_data)
        resp_data = encryptor.decrypt(response_data)
        resp_data = json.loads(resp_data.decode('UTF-8'))
        print(resp_data)
        print(type(resp_data))
        # data = {'code': '00', 'msg': 'Registration successful.'}
        # print(data)
        return resp_data

    def sic_reset_customer_pin(self, user_data):
        request_data = {
                          "action": "resetpin",
                          "msisdn": user_data['id'],
                        }

        req_data = {'model':"bankClient", 'func':"resetpin", 'args':request_data}
        print(request_data)
        encryptor = AESCipher()
        encoded_data = encryptor.encrypt(json.dumps(req_data))
        print(encoded_data)
        # response_data = self.API.send_socket_data(encoded_data)
        # response_data = self.API.request_api_raw_json(encoded_data, url=API_URL, method='post', headers={"Authorization": "21d39021fc624f309fd9d41332e34rt5f"})
        response_data = b'/MuglLXPw5C22iTP3W7aBWdHYpaToXvBOmSLmxB0ClX/PxrGHSarwj3TtE95R7LD'
        print(response_data)
        resp_data = encryptor.decrypt(response_data)
        resp_data = json.loads(resp_data.decode('UTF-8'))
        print(resp_data)
        print(type(resp_data))
        # data = {'code': '00', 'msg': 'Registration successful.'}
        # print(data)
        return resp_data

    def sic_change_customer_status(self, user_data, status):
        request_data = {
                          "action": "customerstatus",
                          "msisdn": user_data['id'],
                          "status": status
                        }

        req_data = {'model':"bankClient", 'func':"customerstatus", 'args':request_data}
        print(request_data)
        encryptor = AESCipher()
        encoded_data = encryptor.encrypt(json.dumps(req_data))
        print(encoded_data)
        # response_data = self.API.send_socket_data(encoded_data)
        # response_data = self.API.request_api_raw_json(encoded_data, url=API_URL, method='post', headers={"Authorization": "21d39021fc624f309fd9d41332e34rt5f"})
        response_data = b'/MuglLXPw5C22iTP3W7aBWdHYpaToXvBOmSLmxB0ClX/PxrGHSarwj3TtE95R7LD'
        print(response_data)
        resp_data = encryptor.decrypt(response_data)
        resp_data = json.loads(resp_data.decode('UTF-8'))
        print(resp_data)
        print(type(resp_data))
        # data = {'code': '00', 'msg': 'Registration successful.'}
        # print(data)
        return resp_data

    def sic_change_customer_account_status(self, user_data, status):
        request_data = {
                          "action": "accountstatus",
                          "uniqueid": user_data['change_to'],
                          "status": status
                        }

        req_data = {'model':"bankClient", 'func':"accountstatus", 'args':request_data}
        print(request_data)
        encryptor = AESCipher()
        encoded_data = encryptor.encrypt(json.dumps(req_data))
        print(encoded_data)
        # response_data = self.API.send_socket_data(encoded_data)
        # response_data = self.API.request_api_raw_json(encoded_data, url=API_URL, method='post', headers={"Authorization": "21d39021fc624f309fd9d41332e34rt5f"})
        response_data = b'/MuglLXPw5C22iTP3W7aBWdHYpaToXvBOmSLmxB0ClX/PxrGHSarwj3TtE95R7LD'
        print(response_data)
        resp_data = encryptor.decrypt(response_data)
        resp_data = json.loads(resp_data.decode('UTF-8'))
        print(resp_data)
        print(type(resp_data))
        # data = {'code': '00', 'msg': 'Registration successful.'}
        # print(data)
        return resp_data

    def get_fusion_VA_details_by_holder_id(self, holder_id):
        req_data = {'model':"FUSION", 'func':"getByHolderId", 'params':json.dumps({"holderId": holder_id})}
        data = self.API.request_api(req_data, url=VA_URL, method='post', headers={"Authorization": "21d39021fc624f309fd9d41332e34rt5f"})
        # data = {'msg': {'accountName': 'VA_GT', 'accountMaps': [{'balance': '0', 'entityType': 'WALLET', 'usage': 'COLLECTIONS', 'mapID': '143c0ce34bf44205bd4447ec049f1ba3', 'entityID': '55df143cfedc9bfd3bb99977', 'threshold': 1, 'mapName': 'TIGO_COLLECTIONS'}, {'balance': '5005.00', 'entityType': 'WALLET', 'usage': 'DISBURSEMENTS', 'mapID': 'edc0369efeed434f9f200fc46e766925', 'entityID': '55df143cfedc9bfd3bb99977', 'threshold': 10000, 'mapName': 'TIGO_DISBURSEMENTS'}, {'balance': '0', 'entityType': 'WALLET', 'usage': 'COLLECTIONS', 'mapID': '5ed7ab06054f4c4b916c3f91ca1dcf6a', 'entityID': '55df1563fedc9bfd3bb99978', 'threshold': 1, 'mapName': 'AIRTEL_COLLECTIONS'}, {'balance': '5005.00', 'entityType': 'WALLET', 'usage': 'DISBURSEMENTS', 'mapID': '18fe760f3c50468895612b0b1ffe7973', 'entityID': '55df1563fedc9bfd3bb99978', 'threshold': 10000, 'mapName': 'AIRTEL_DISBURSEMENTS'}, {'balance': '0', 'entityType': 'WALLET', 'usage': 'COLLECTIONS', 'mapID': 'a09b2fdb7737476ebba6517042eb6bf4', 'entityID': '55df15fa12ece2fa3b91c54f', 'threshold': 1, 'mapName': 'MTN_COLLECTIONS'}, {'balance': '1178.27', 'entityType': 'WALLET', 'usage': 'DISBURSEMENTS', 'mapID': '22e76033e6c44bf2b8e2790bc2cc8163', 'entityID': '55df15fa12ece2fa3b91c54f', 'threshold': 10000, 'mapName': 'MTN_DISBURSEMENTS'}, {'balance': '0', 'entityType': 'WALLET', 'usage': 'COLLECTIONS', 'mapID': 'fc38611e361b42eaadcb48e95b60fead', 'entityID': '57e3c7ba4100ec664fb15a87', 'threshold': 1, 'mapName': 'VODAFONE_COLLECTIONS'}, {'balance': '4965.00', 'entityType': 'WALLET', 'usage': 'DISBURSEMENTS', 'mapID': '4892f3dcca8649849af69dc10bb07346', 'entityID': '57e3c7ba4100ec664fb15a87', 'threshold': 10000, 'mapName': 'VODAFONE_DISBURSEMENTS'}], 'id': '58f2e0edcc1a613a5a22a45f', 'accountNumber': 'VA170416031141', 'holderID': '55e474a83b4ec3737fc0104e', 'enabled': True}, 'code': '00'}
        # print(data)
        return data

    def fusion_register_customer(self, user_data):
        route = "/user/bc/{}".format(FS_INST_APIKEY)

        user_data['instID'] = FS_INST_ID
        user_data['kuwaita'] = "kuongeza_benki"
        print(user_data)

        # data = self.API.request_api(user_data, route=route, method='post')
        data = {'msg':"Customer registered Successfully.",  
                'code': '00',
                'data': [],
                }
        return data

    def fusion_deactivate_customer(self, user_data):
        route = "/user/bc/{}".format(FS_INST_APIKEY)

        user_data['instID'] = FS_INST_ID
        user_data['kuwaita'] = "mabadiliko_akaunti"
        user_data['status'] = "false"
        print(user_data)

        # data = self.API.request_api(user_data, route=route, method='post')
        data = {'msg':"Customer registered Successfully.",  
                'code': '00',
                'data': [],
                }
        return data

    def fusion_activate_customer(self, user_data):
        route = "/user/bc/{}".format(FS_INST_APIKEY)

        user_data['instID'] = FS_INST_ID
        user_data['kuwaita'] = "mabadiliko_akaunti"
        user_data['status'] = "true"
        print(user_data)

        # data = self.API.request_api(user_data, route=route, method='post')
        data = {'msg':"Customer registered Successfully.",  
                'code': '00',
                'data': [],
                }
        return data
    
    def getVerificationHistory(self, request_params):
        where_con = ""

        if request_params['status'] == "All":
            where_con = "1"
        else:
            where_con = "status= '"+ request_params['status'] +"'"

        if request_params['fromdate'] == "" or request_params['todate'] == "":
            data = self.dbconn.select_from_table_paged("tbl_activity_log", condition=" WHERE user_type='{}'".format(request_params["user_type"]) + " AND " + where_con + " ORDER BY date_created DESC", offset=request_params['offset'], records=request_params['records'])
            data_count = self.dbconn.select_count_table("tbl_activity_log", condition=" WHERE user_type='{}'".format(request_params["user_type"]) + " AND " + where_con)
        else:
            data = self.dbconn.select_from_table_paged("tbl_activity_log", condition= " WHERE user_type='{}'".format(request_params["user_type"]) + " AND " + where_con +" AND DATE(date_created) BETWEEN '{0}' AND '{1}' ORDER BY date_created DESC".format(request_params['fromdate'], request_params['todate']), offset=request_params['offset'], records=request_params['records'])
            data_count = self.dbconn.select_count_table("tbl_activity_log", condition= " WHERE user_type='{}'".format(request_params["user_type"]) + " AND " + where_con +" AND DATE(date_created) BETWEEN '{0}' AND '{1}'".format(request_params['fromdate'], request_params['todate']))
        
        return [data, data_count]

    def searchVerifiedVouchers(self, request_params):
        data = self.dbconn.select_from_table("tbl_activity_log", condition= " WHERE user_type='{}'".format(request_params["user_type"]) + " AND serial_no LIKE '%{}%'".format(request_params['search_param']))
        return data



