from app.libs.mysqllib import MysqlLib
 
class LogModel(object):
    """docstring for UserFunctions"""
    def __init__(self, user):
        super(LogModel, self).__init__()
        self.dbconn = MysqlLib()
        self.user = user

    def getAllTransactions(self, request_params):

        where_con_list = []
        where_con = ''

        if  "status" in request_params and request_params['status'] != "":
            where_con_list.append("msg_stat='{}' ".format(request_params['status']))

        if  "branch" in request_params and request_params['branch'] != "":
            where_con_list.append("account_branch='{}' ".format(request_params['branch']))

        if  "destination" in request_params and request_params['destination'] != "":
            where_con_list.append("destination='{}' ".format(request_params['destination']))

        if  "type" in request_params and request_params['type'] != "":
            where_con_list.append("type='{}' ".format(request_params['type']))

        if  "tag" in request_params and request_params['tag'] != "":
            where_con_list.append("fusion_tag='{}' ".format(request_params['tag']))

        where_con = " and ".join(where_con_list)
        if where_con == "":
            where_con = "1"

        if request_params['fromdate'] == "" or request_params['todate'] == "":
            data = self.dbconn.select_from_table_paged("tbl_transactions", condition="WHERE "+ where_con +" ORDER BY response_time DESC", offset=request_params['offset'], records=request_params['records'])
            data_count = self.dbconn.select_count_table("tbl_transactions", condition="WHERE "+ where_con)
        else:
            data = self.dbconn.select_from_table_paged("tbl_transactions", condition=" WHERE "+ where_con +" and response_time between '{0}' and '{1}' ORDER BY response_time DESC".format(request_params['fromdate'], request_params['todate']), offset=request_params['offset'], records=request_params['records'])
            data_count = self.dbconn.select_count_table("tbl_transactions", condition="WHERE "+ where_con)
        return [data, data_count]


    def getAllTransactionsByBranch(self, request_params):

        where_con_list = []
        where_con = ''

        if request_params['status'] != "":
            where_con_list.append("status='{}' ".format(request_params['status']))

        where_con = " and ".join(where_con_list)
        if where_con == "":
            where_con = "1"

        if request_params['fromdate'] == "" or request_params['todate'] == "":
            data = self.dbconn.select_from_table_paged("tbl_transactions", ["tbl_file_upload"], ["tbl_transaction.*"], ["tbl_transaction.bulk_id=tbl_file_upload.bulk_id AND tbl_file_upload.merchant_id='{}'".format(self.user['institution_data']['id'])], "WHERE "+ where_con +" ORDER BY transaction_date DESC".format(request_params['fromdate'], request_params['todate']), offset=request_params['offset'], records=request_params['records'])
        else:
            data = self.dbconn.select_from_table_paged("tbl_transactions", ["tbl_file_upload"], ["tbl_transaction.*"], ["tbl_transaction.bulk_id=tbl_file_upload.bulk_id AND tbl_file_upload.merchant_id='{}'".format(self.user['institution_data']['id'])], "WHERE "+ where_con +" and transaction_date between '{0}' and '{1}' ORDER BY date_upload DESC".format(request_params['fromdate'], request_params['todate']), offset=request_params['offset'], records=request_params['records'])
        return data


    def getAllTransactionsfilter(self):
        filter_data = {}
        filter_data['branches'] = self.dbconn.select_distinct("tbl_transactions", "account_branch")
        filter_data['destination'] = self.dbconn.select_distinct("tbl_transactions", "destination")
        filter_data['type'] = self.dbconn.select_distinct("tbl_transactions", "type")
        filter_data['status'] = self.dbconn.select_distinct("tbl_transactions", "msg_stat")
        filter_data['tag'] = self.dbconn.select_distinct("tbl_transactions", "fusion_tag")

        print(filter_data)
        return filter_data


    def searchTransactions(self, request_params):
        search_data = self.dbconn.search_table(request_params['search_param'], "tbl_transactions", ['xref', 'reference', 'account_branch', 'processing_branch', 'account_number', 'des_act', 'destination', 'msisdn', 'msg_stat', 'fusion_tag', 'type', 'request_time', 'response_time'])

        return search_data
        


    def getAllTransactionsfilterForBranch(self):

        pass


    def getBulkUploadDetailsByBulkId(self, bulk_id):
        print(bulk_id)
        data = self.dbconn.joint_select("tbl_file_upload", ["tbl_login", "tbl_file_upload_xdetails"], ["tbl_file_upload.*","tbl_login.username", "tbl_file_upload_xdetails.amount","tbl_login.institution_shortName", ], ["tbl_file_upload.merchant_admin_id=tbl_login.id", "tbl_file_upload_xdetails.bulk_id='{}'".format(bulk_id)], "WHERE tbl_file_upload.bulk_id= \'"+ bulk_id +"\'")
        approval_data = self.dbconn.joint_select("tbl_file_upload_approval", ["tbl_login"], ["tbl_login.*", "tbl_file_upload_approval.*"], ["tbl_file_upload_approval.merchant_admin_id=tbl_login.id"], gen_condition="WHERE tbl_file_upload_approval.bulk_id='"+ bulk_id +"'")
        if approval_data == []:
            data[0]['approval_data'] =  []
        else:
            data[0]['approval_data'] =  approval_data
        return data


    def insertBulkUpload(self, data):
        admin = self.dbconn.insert_in_table("tbl_file_upload",data)
        return True


    def insertBulkUploadXtraDetails(self, data):
        res = self.dbconn.insert_in_table("tbl_file_upload_xdetails", data)
        return res

    def updateAdminByUsername(self, username, data):
        admin = self.dbconn.update_table("tbl_login", data, "WHERE bulk_id='"+ username +"'")
        return True

    def getValidationLog(self, request_params):
        return True
    
