from app.libs.mysqllib import MysqlLib

class Administrator(object):
    """docstring for UserFunctions"""
    def __init__(self, user):
        super(Administrator, self).__init__()
        self.dbconn = MysqlLib()
        self.user = user

    def getAdminByUsernameLogin(self, username):
        # admin = self.dbconn.select_from_table('tbl_logins', condition = "WHERE username= '"+ username +"'")
        admin = self.dbconn.joint_select("tbl_logins", ["tbl_user_rights", "tbl_branches"], ["tbl_logins.password", "tbl_logins.username", "tbl_logins.user_right_id", "tbl_logins.first_name", "tbl_logins.last_name", "tbl_logins.email", "tbl_logins.msisdn", "tbl_logins.last_login", "tbl_logins.pass_date", "tbl_logins.active", "tbl_logins.status", "tbl_logins.created", "tbl_user_rights.name", "tbl_user_rights.details", "tbl_branches.branch_name", "tbl_branches.branch_code", "tbl_branches.branch_id"], ["tbl_logins.user_right_id=tbl_user_rights.id", "tbl_logins.branch=tbl_branches.branch_code"], gen_condition = "WHERE username= '"+ username +"'")
        return admin

    def getAdminByUsername(self, username):
        # admin = self.dbconn.select_from_table('tbl_logins', condition = "WHERE username= '"+ username +"'")
        admin = self.dbconn.joint_select("tbl_logins", ["tbl_user_rights", "tbl_branches"], ["tbl_logins.username", "tbl_logins.user_right_id", "tbl_logins.first_name", "tbl_logins.last_name", "tbl_logins.email", "tbl_logins.msisdn", "tbl_logins.last_login", "tbl_logins.pass_date", "tbl_logins.active", "tbl_logins.status", "tbl_logins.created", "tbl_user_rights.name", "tbl_user_rights.details", "tbl_branches.branch_name", "tbl_branches.branch_code", "tbl_branches.branch_id"], ["tbl_logins.user_right_id=tbl_user_rights.id", "tbl_logins.branch=tbl_branches.branch_code"], gen_condition = "WHERE username= '"+ username +"'")
        return admin

    def getAdminByUsername_chg(self, username):
        # admin = self.dbconn.select_from_table('tbl_logins', condition = "WHERE username= '"+ username +"'")
        admin = self.dbconn.joint_select("tbl_logins", ["tbl_user_rights", "tbl_branches"], ["tbl_logins.username", "tbl_logins.password", "tbl_logins.user_right_id", "tbl_logins.first_name", "tbl_logins.last_name", "tbl_logins.email", "tbl_logins.msisdn", "tbl_logins.last_login", "tbl_logins.pass_date", "tbl_logins.active", "tbl_logins.status", "tbl_logins.created", "tbl_user_rights.name", "tbl_user_rights.details", "tbl_branches.branch_name", "tbl_branches.branch_code", "tbl_branches.branch_id"], ["tbl_logins.user_right_id=tbl_user_rights.id", "tbl_logins.branch=tbl_branches.branch_code"], gen_condition = "WHERE username= '"+ username +"'")
        return admin

    def getAdminByMsisdn(self, msisdn):
        # admin = self.dbconn.select_from_table('tbl_logins', condition = "WHERE msisdn= '"+ msisdn +"'")
        admin = self.dbconn.joint_select("tbl_logins", ["tbl_user_rights", "tbl_branches"], ["tbl_logins.username", "tbl_logins.user_right_id", "tbl_logins.first_name", "tbl_logins.last_name", "tbl_logins.email", "tbl_logins.msisdn", "tbl_logins.last_login", "tbl_logins.pass_date", "tbl_logins.active", "tbl_logins.status", "tbl_logins.created", "tbl_user_rights.name", "tbl_user_rights.details", "tbl_branches.branch_name", "tbl_branches.branch_code", "tbl_branches.branch_id"], ["tbl_logins.user_right_id=tbl_user_rights.id", "tbl_logins.branch=tbl_branches.branch_code"], gen_condition = "WHERE msisdn= '"+ msisdn +"'")
        return admin

    def getAdminByEmail(self, email):
        # admin = self.dbconn.select_from_table('tbl_logins', condition = "WHERE email= '"+ email +"'")
        admin = self.dbconn.joint_select("tbl_logins", ["tbl_user_rights", "tbl_branches"], ["tbl_logins.username", "tbl_logins.user_right_id", "tbl_logins.first_name", "tbl_logins.last_name", "tbl_logins.email", "tbl_logins.msisdn", "tbl_logins.last_login", "tbl_logins.pass_date", "tbl_logins.active", "tbl_logins.status", "tbl_logins.created", "tbl_user_rights.name", "tbl_user_rights.details", "tbl_branches.branch_name", "tbl_branches.branch_code", "tbl_branches.branch_id"], ["tbl_logins.user_right_id=tbl_user_rights.id", "tbl_logins.branch=tbl_branches.branch_code"], gen_condition = "WHERE email= '"+ email +"'")
        return admin

    def getAllAdministrators(self, request_params):

        where_con_list = []
        where_con = ''

        if 'active' in request_params != "" and request_params['active'] != "" and request_params['active'] != "All":
            where_con_list.append("active='{}' ".format(request_params['active']))

        if 'user_right_id' in request_params != "" and request_params['user_right_id'] != "":
            where_con_list.append("user_right_id='{}' ".format(request_params['user_right_id']))

        if 'branch' in request_params != "" and request_params['branch'] != "" and request_params['branch'] != "All":
            where_con_list.append("branch='{}' ".format(request_params['branch']))

        where_con = " and ".join(where_con_list)
        if where_con == "":
            where_con = "1"

        if request_params['fromdate'] == "" or request_params['todate'] == "":
            data = self.dbconn.joint_select_paged("tbl_logins", ["tbl_user_rights", "tbl_branches"], ["tbl_logins.username", "tbl_logins.user_right_id", "tbl_logins.first_name", "tbl_logins.last_name", "tbl_logins.email", "tbl_logins.msisdn", "tbl_logins.last_login", "tbl_logins.active", "tbl_logins.status", "tbl_logins.created", "tbl_user_rights.name", "tbl_user_rights.details", "tbl_branches.branch_name", "tbl_branches.branch_code"], ["tbl_logins.user_right_id=tbl_user_rights.id", "tbl_logins.branch=tbl_branches.branch_code"], "WHERE "+ where_con +" ORDER BY created DESC", offset=request_params['offset'], records=request_params['records'])
        else:
            data = self.dbconn.joint_select_paged("tbl_logins", ["tbl_user_rights", "tbl_branches"], ["tbl_logins.username", "tbl_logins.user_right_id", "tbl_logins.first_name", "tbl_logins.last_name", "tbl_logins.email", "tbl_logins.msisdn", "tbl_logins.last_login", "tbl_logins.active", "tbl_logins.status", "tbl_logins.created", "tbl_user_rights.name", "tbl_user_rights.details", "tbl_branches.branch_name", "tbl_branches.branch_code"], ["tbl_logins.user_right_id=tbl_user_rights.id", "tbl_logins.branch=tbl_branches.branch_code"], "WHERE "+ where_con +" and created between '{0}' and '{1}' ORDER BY created DESC".format(request_params['fromdate'], request_params['todate']), offset=request_params['offset'], records=request_params['records'])
        return data


    def getAllAdministratorsByBranch(self, request_params):

        where_con_list = []
        where_con = ''

        if 'active' in request_params != "" and request_params['active'] != "" and request_params['active'] != "All":
            where_con_list.append("active='{}' ".format(request_params['active']))

        if 'user_right_id' in request_params != "" and request_params['user_right_id'] != "":
            where_con_list.append("user_right_id='{}' ".format(request_params['user_right_id']))

        if 'branch' in request_params != "" and request_params['branch'] != "" and request_params['branch'] != "All":
            where_con_list.append("branch='{}' ".format(request_params['branch']))

        where_con = " and ".join(where_con_list)
        if where_con == "":
            where_con = "1"

        if request_params['fromdate'] == "" or request_params['todate'] == "":
            data = self.dbconn.joint_select_paged("tbl_logins", ["tbl_user_rights", "tbl_branches"], ["tbl_logins.username", "tbl_logins.user_right_id", "tbl_logins.first_name", "tbl_logins.last_name", "tbl_logins.email", "tbl_logins.msisdn", "tbl_logins.last_login", "tbl_logins.active", "tbl_logins.status", "tbl_logins.created", "tbl_user_rights.name", "tbl_user_rights.details", "tbl_branches.branch_name", "tbl_branches.branch_code"], ["tbl_logins.user_right_id=tbl_user_rights.id", "tbl_logins.branch=tbl_branches.branch_code"], "WHERE "+ where_con +" and tbl_logins.branch='{0}' ORDER BY created DESC".format(self.user['branch_code']), offset=request_params['offset'], records=request_params['records'])
        else:
            data = self.dbconn.joint_select_paged("tbl_logins", ["tbl_user_rights", "tbl_branches"], ["tbl_logins.username", "tbl_logins.user_right_id", "tbl_logins.first_name", "tbl_logins.last_name", "tbl_logins.email", "tbl_logins.msisdn", "tbl_logins.last_login", "tbl_logins.active", "tbl_logins.status", "tbl_logins.created", "tbl_user_rights.name", "tbl_user_rights.details", "tbl_branches.branch_name", "tbl_branches.branch_code"], ["tbl_logins.user_right_id=tbl_user_rights.id", "tbl_logins.branch=tbl_branches.branch_code"], "WHERE "+ where_con +" and tbl_logins.branch='{0}' and created between '{1}' and '{2}' ORDER BY created DESC".format(self.user['branch_code'], request_params['fromdate'], request_params['todate']), offset=request_params['offset'], records=request_params['records'])
        return data

    def addAdministrator(self, data):
        admin = self.dbconn.insert_in_table("tbl_logins", data)
        return admin


    def updateAdministrator(self, data):
        admin = self.dbconn.update_table("tbl_logins", data, "WHERE username='{}'".format(data['username']))
        return admin

    def getAdminGroups(self):
        data = self.dbconn.select_from_table("tbl_user_rights", condition="where id != 1")
        return data

    def addAdministratorGroup(self, data):
        admin = self.dbconn.insert_in_table("tbl_user_rights", data)
        return admin

    def updateAdministratorGroup(self, data):
        admin = self.dbconn.update_table("tbl_user_rights", data, "WHERE id='{}'".format(data['id']))
        return admin

    def getBranches(self, request_params):
        data = self.dbconn.select_from_table_paged("tbl_branches", offset=request_params['offset'], records=request_params['records'])
        return data

    def getBranchByCode(self, branch_code):
        data = self.dbconn.select_from_table("tbl_branches", condition="WHERE branch_code='{}'".format(branch_code))
        return data

    def searchAdmins(self, request_params):
        search_data = self.dbconn.joint_table_search(request_params['search_param'], "tbl_logins", ["tbl_branches", "tbl_user_rights"], ["tbl_logins.username", "tbl_logins.user_right_id", "tbl_logins.first_name", "tbl_logins.last_name", "tbl_logins.email", "tbl_logins.msisdn", "tbl_logins.last_login", "tbl_logins.active", "tbl_logins.status", "tbl_logins.created", "tbl_user_rights.name", "tbl_user_rights.details", "tbl_branches.branch_name", "tbl_branches.branch_code"], ["tbl_logins.branch=tbl_branches.branch_code", "tbl_logins.user_right_id=tbl_user_rights.id"])
        return search_data

    def searchAdminsBranch(self, request_params):
        search_data = self.dbconn.joint_table_search(request_params['search_param'], "tbl_logins", ["tbl_branches", "tbl_user_rights"], ["tbl_logins.username", "tbl_logins.user_right_id", "tbl_logins.first_name", "tbl_logins.last_name", "tbl_logins.email", "tbl_logins.msisdn", "tbl_logins.last_login", "tbl_logins.active", "tbl_logins.status", "tbl_logins.created", "tbl_user_rights.name", "tbl_user_rights.details", "tbl_branches.branch_name", "tbl_branches.branch_code"], ["tbl_logins.branch=tbl_branches.branch_code", "tbl_logins.user_right_id=tbl_user_rights.id"], gen_cond="  and tbl_logins.branch='{0}'".format(self.user['branch_code']))
        return search_data

    def searchAdminsBranch(self, request_params):
            search_data = self.dbconn.joint_table_search(request_params['search_param'], "tbl_logins", ["tbl_branches", "tbl_user_rights"], ["tbl_logins.username", "tbl_logins.user_right_id", "tbl_logins.first_name", "tbl_logins.last_name", "tbl_logins.email", "tbl_logins.msisdn", "tbl_logins.last_login", "tbl_logins.active", "tbl_logins.status", "tbl_logins.created", "tbl_user_rights.name", "tbl_user_rights.details", "tbl_branches.branch_name", "tbl_branches.branch_code"], ["tbl_logins.branch=tbl_branches.branch_code", "tbl_logins.user_right_id=tbl_user_rights.id"], gen_cond="  and tbl_logins.branch='{0}'".format(self.user['branch_code']))
            return search_data

    def searchBranches(self, request_params):
        search_data = self.dbconn.search_table(request_params['search_param'], 'tbl_branches', ["id", "branch_id", "acronym", "branch_name", "branch_code"])
        return search_data

    def addAdminBranch(self, data):
        admin = self.dbconn.insert_in_table("tbl_branches", data)
        return admin

    def removeAdminBranch(self, data):
        admin = self.dbconn.delete_from_table("tbl_branches", "where branch_id={}".format(data['branch_id']))
        return admin