from app.libs.mysqllib import MysqlLib

class Validator(object):
    """docstring for UserFunctions"""
    def __init__(self, user):
        super(Validator, self).__init__()
        self.dbconn = MysqlLib()
        self.user = user

    def getValidatorByMsisdn(self, msisdn):
        validator = self.dbconn.select_from_table('tbl_validators', condition = "WHERE msisdn= '"+ msisdn +"'")
        return validator

    def getValidatorByEmail(self, email):
        validator = self.dbconn.select_from_table('tbl_validators', condition = "WHERE email= '"+ email +"'")
        return validator

    def getAllValidators(self, request_params):
        where_con = ""

        if request_params['branch'] == "None":
            where_con = "1"
        else:
            where_con = "branch= '"+ request_params['branch'] +"'"

        data = self.dbconn.select_from_table_paged("tbl_validators", condition=" WHERE " + where_con + " ORDER BY date_created DESC", offset=request_params['offset'], records=request_params['records'])
        data_count = self.dbconn.select_count_table("tbl_validators", condition=" WHERE " + where_con)
        
        return [data, data_count]   

    def addValidator(self, data):
        admin = self.dbconn.insert_in_table("tbl_validators", data)
        return admin

    def updateValidator(self, data):
        admin = self.dbconn.update_table("tbl_validators", data, "WHERE email='{}'".format(data['email']))
        return admin
        
    def deleteValidator(self, request_id):
        data = self.dbconn.delete_from_table("tbl_validators", condition=" WHERE validator_id={}".format(request_id))
        return data

    def getBranches(self):
        data = self.dbconn.select_from_table("tbl_branches")
        return data
    
    def getValidatorsHistory(self, request_params):
        where_con = ""

        if request_params['user_branch'] == "Non":
            where_con = "1"
        else:
            where_con = "user_branch= '"+ request_params['user_branch'] +"'"

        if request_params['fromdate'] == "" or request_params['todate'] == "":
            data = self.dbconn.select_from_table_paged("tbl_activity_log", condition=" WHERE user_type='{}'".format(request_params["user_type"]) + " AND " + where_con + " ORDER BY date_created DESC", offset=request_params['offset'], records=request_params['records'])
            data_count = self.dbconn.select_count_table("tbl_activity_log", condition=" WHERE user_type='{}'".format(request_params["user_type"]) + " AND " + where_con)
        else:
            data = self.dbconn.select_from_table_paged("tbl_activity_log", condition= " WHERE user_type='{}'".format(request_params["user_type"]) + " AND " + where_con +" AND DATE(date_created) BETWEEN '{0}' AND '{1}' ORDER BY date_created DESC".format(request_params['fromdate'], request_params['todate']), offset=request_params['offset'], records=request_params['records'])
            data_count = self.dbconn.select_count_table("tbl_activity_log", condition= " WHERE user_type='{}'".format(request_params["user_type"]) + " AND " + where_con +" AND DATE(date_created) BETWEEN '{0}' AND '{1}'".format(request_params['fromdate'], request_params['todate']))
        
        return [data, data_count]
        
    def searchValidatoinHistory(self, request_params):
        data = self.dbconn.select_from_table("tbl_activity_log", condition= " WHERE user_type='{}'".format(request_params["user_type"]) + " AND serial_no LIKE '%{}%'".format(request_params['search_param']))
        return data


