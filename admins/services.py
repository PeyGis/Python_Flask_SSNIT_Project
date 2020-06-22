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

from passlib.hash import sha256_crypt

from app import config
from app import language
from app.admins.models import Administrator
from app.libs.logger import Logger
from app.libs.utils import Utilites

class adminServices(object):
    """
    Class contains functions and attributes for authtentication
    Function: * getCampainge(sel)
    """
    def __init__(self, user):
        self.lang = {}
        self.lang = getattr(language, config.DEFAULT_LANG)
        self.user = user
        self.model = Administrator(user)
        self.logger = Logger()
        


    def adminlogin(self, request_data, try_var):
        """
        This function handles all logic related to login on the platform
        @Params : void
        """
        self.logger.write_to_console("EVENT", "Login request for "+ request_data['username'])
        
        admin_data = self.model.getAdminByUsernameLogin(request_data['username'])
        if admin_data == []:
            self.logger.write_log("USER_ACCESS", "Login request | "+ request_data['username'] + " | Failed | Non-Existing User.")
            return {"code":language.CODES['FAIL'], "msg":self.lang['wrong_username'], "data":[]}
        else:
            print(try_var)
            if try_var != None and try_var >=3: 
                self.model.updateAdministrator({"active":"2", "last_login":"NOW()", "username":request_data['username']})
                if try_var == 3:
                    return {"code":language.CODES['FAIL'], "msg":"Sorry your account has been blocked. Kindly contact your administrator.", "data":2, "username": request_data['username']}
                else:
                    return {"code":language.CODES['FAIL'], "msg":"Sorry your account has been blocked. Kindly contact your administrator.", "data":[]}
                
            else:
                if admin_data[0]['active'] == 1:
                    print(admin_data[0])
                    verify_pass = sha256_crypt.verify(request_data['password'], admin_data[0]['password'])
                    self.logger.write_to_console("EVENT", "varify Password | "+ str(verify_pass))
                    
                    if verify_pass == True:
                        self.model.updateAdministrator({"status":"1", "last_login":"NOW()", "username":request_data['username']})
                        self.logger.write_log("USER_ACCESS", "Login request | "+ request_data['username'] + " | Successful | Login Successful")
                        return {"code":language.CODES['SUCCESS'], "msg":self.lang['login_successful'], "data":admin_data[0], "username": request_data['username']}
                    else:
                        self.logger.write_to_console("EVENT", "Login request failed for "+ request_data['username'] + " | Failed | Wrong Password.")
                        return {"code":language.CODES['FAIL'], "msg":self.lang['wrong_username'], "data":1, "username": request_data['username']}

                else:
                    self.logger.write_to_console("EVENT", "Login request failed for "+ request_data['username'] + " | Failed | Blocked User")
                    return {"code":language.CODES['FAIL'], "msg":"Sorry your account has been blocked. Kindly contact your administrator.", "data":2, "username": request_data['username']}

    def adminLogout(self):
        result = self.model.updateAdministrator({"status":"0", "username":self.user['username']})
        return result

    def getAllAdministrators(self, request_data):
        """
            This function handles all logic related to login on the platform

            @Params : void
        """

        if request_data == {}:
            request_data = {'offset':0, 'records':11, 'fromdate':'', 'user_right_id': '', "branch": '','active': ''}
        else:
            request_data['offset'] = int(request_data['page'])*11
            request_data['records'] = 11

        self.logger.write_to_console("EVENT", "Getting administrator list for {} -> {}".format(self.user['username'], request_data))
        
        if self.user['branch_code'] == "All":
            administrators_data = self.model.getAllAdministrators(request_data)
            admin_groups_data =  self.model.getAdminGroups()
            branches_data =  self.model.getBranches({'offset':0, 'records': 11})
        else:
            administrators_data = self.model.getAllAdministratorsByBranch(request_data)
            admin_groups_data =  self.model.getAdminGroups()
            branches_data =  self.model.getBranches({'offset':0, 'records': 11})

        for result in administrators_data:
            result["created"] = result["created"].strftime("%Y-%m-%d %H:%M:%S")
            result["last_login"] = result["last_login"].strftime("%Y-%m-%d %H:%M:%S")
            
            if "pass_date" in result:
                result["pass_date"] = result["pass_date"].strftime("%Y-%m-%d %H:%M:%S")

        self.logger.write_to_console("EVENT", "Administrators list gotten successfully for {}".format(self.user['username']))
        return {"code":language.CODES['SUCCESS'], "msg":self.lang['data_retrived'], "data":administrators_data, 'admin_group': admin_groups_data, 'branches': branches_data}


    def getAllAdministratorsExport(self, request_data):
        """
            This function handles all logic related to login on the platform

            @Params : void
        """

        request_data['offset'] = 0
        request_data['records'] = 10000
 
        self.logger.write_to_console("EVENT", "Getting administrator list for {} -> {}".format(self.user['username'], request_data))

        export_list = [['USERNAME', 'FIRST NAME', 'LAST NAME', 'EMAIL','PHONE NUMBER','BRANCH','GROUP', 'STATUS', 'DATE CREATED']]
        
        if self.user['branch_code'] == "All":
            administrators_data = self.model.getAllAdministrators(request_data)
            admin_groups_data =  self.model.getAdminGroups()
            branches_data =  self.model.getBranches()
        else:
            administrators_data = self.model.getAllAdministratorsByBranch(request_data)
            admin_groups_data =  self.model.getAdminGroups()
            branches_data =  self.model.getBranches()

        for result in administrators_data:
            result["created"] = result["created"].strftime("%Y-%m-%d %H:%M:%S")
            result["last_login"] = result["last_login"].strftime("%Y-%m-%d %H:%M:%S")
            if "pass_date" in result:
                result["pass_date"] = result["pass_date"].strftime("%Y-%m-%d %H:%M:%S")
            
            if result["active"] == 1:
                result["active"] = self.lang["active"]
            else:
                result["active"] = self.lang["inactive"]

            export_list.append([result['username'], result['first_name'], result['last_name'], result['email'], result['email'], result['branch_code'], result['name'], result['active'], result['created']])

        self.logger.write_to_console("EVENT", "Administrators Export list gotten successfully for {}".format(self.user['username']))
        return export_list


    def addAdmin(self, request_data):
        """
            This function handles all logic related to login on the platform

            @Params : void
        """
        self.logger.write_to_console("EVENT", "{0} Adding Admin {1}".format(self.user['username'], str(request_data)))
        request_data['msisdn'] = "233" + request_data['msisdn'][-9:]
        request_data['email'] = request_data['email'].strip()
        
        admin_data = self.model.getAdminByUsername(request_data['username'])
        if admin_data == []:
            admin_data = self.model.getAdminByMsisdn(request_data['msisdn'])
            if admin_data == []:
                admin_data = self.model.getAdminByEmail(request_data['email'])
                if admin_data == []:
                    self.logger.write_to_console("EVENT", "Preparing data")
                    # raw_password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))
                    utl = Utilites()
                    raw_password = utl.generate_password(10)
                    password = sha256_crypt.encrypt(raw_password)
                    self.logger.write_to_console("EVENT", "Generated password: {0} \n Hashed Password: {1} \n".format(raw_password, password))

                    # request_data['msisdn'] = "233" + request_data['msisdn'][-9:]
                    request_data['password'] = password
                    request_data['last_login'] = "NOW()"

                    res = self.model.addAdministrator(request_data) 
                    if res == True:
                        Utilites.send_mail(Utilites, "SSNIT PORTAL", "<p>Hi {0}</p><p>Welcome SSNIT, below are your login credentials.<br><br>Username: {1}<br>Password: {2}<br><br><br> Regards</p><p>FUSION PLATFORM</p>".format(request_data['first_name'], request_data['username'], raw_password), [request_data['email']])
                        return {"code":language.CODES['SUCCESS'], "msg":self.lang['admin_added'], "data":[]}
                    else:
                        return {"code":language.CODES['FAIL'], "msg":self.lang['admin_add_fail'], "data":[]}
                else:
                    self.logger.write_to_console("EVENT", "Existing Admin Username "+ request_data['username'] + " | Blocked User.")
                    return {"code":language.CODES['FAIL'], "msg": "Email is already registered to another administrator.", "data":[]}
            else:
                self.logger.write_to_console("EVENT", "Existing Admin Username "+ request_data['username'] + " | Blocked User.")
                return {"code":language.CODES['FAIL'], "msg": "Phone number is already registered to another administrator.", "data":[]}

        else:
            self.logger.write_to_console("EVENT", "Existing Admin Username "+ request_data['username'] + " | Blocked User.")
            return {"code":language.CODES['FAIL'], "msg": "Username is already registered to another administrator.", "data":[]}


    def addAdminGroup(self, request_data):
        """
            This function handles all logic related to login on the platform

            @Params : void
        """
        self.logger.write_to_console("EVENT", "{0} Adding Admin Group {1}".format(self.user['username'], str(request_data)))

        res = self.model.addAdministratorGroup(request_data)
        if res == True:
            return {"code":language.CODES['SUCCESS'], "msg": "New group added successfully.", "data":[]}
        else:
            return {"code":language.CODES['FAIL'], "msg": "Failed to add group.", "data":[]}


    def updateAdminGroup(self, request_data):
        """
            This function handles all logic related to login on the platform

            @Params : void
        """
        self.logger.write_to_console("EVENT", "{0} Updating Admin Group {1}".format(self.user['username'], str(request_data)))

        res = self.model.updateAdministratorGroup(request_data)
        if res == True:
            return {"code":language.CODES['SUCCESS'], "msg": "Group updated successfully.", "data":[]}
        else:
            return {"code":language.CODES['FAIL'], "msg": "Failed to update group.", "data":[]}


    def getAdmin(self, request_data):
        """
            This function handles all logic related to login on the platform

            @Params : void
        """
        self.logger.write_to_console("EVENT", "Login request for "+ request_data['username'])
        
        admin_data = self.model.getAdminByUsername(request_data['username'])
        if admin_data == []:
            self.logger.write_to_console("EVENT", "Failed to get admin "+ request_data['username'] + " | Non-Existing User.")
            return {"code":language.CODES['FAIL'], "msg":self.lang['wrong_username'], "data":[]}
        else:
            self.logger.write_to_console("EVENT", "Administor Data retreived successfully "+ request_data['username'] + " | Success.")
            return {"code":language.CODES['SUCCESS'], "msg":self.lang['login_successful'], "data":admin_data[0]}

    def getAdminInstDetails(self):
        """
            This function handles all logic related to login on the platform

            @Params : void
        """
        self.logger.write_to_console("EVENT", "Getting Details for "+ self.user['username'])
        
        admin_data = self.model.getAdminByUsername(self.user['username'])
        if admin_data == []:
            self.logger.write_to_console("EVENT", "Failed to get admin "+ self.user['username'] + " | Non-Existing User.")
            return {"code":language.CODES['FAIL'], "msg":self.lang['wrong_username'], "data":[]}
        else:
            self.logger.write_to_console("EVENT", "Administor Data retreived successfully "+ self.user['username'] + " | Success.")
            return {"code":language.CODES['SUCCESS'], "msg":self.lang['login_successful'], "data":admin_data[0]}


    def updateAdmin(self, request_data):
        """
            This function handles all logic related to login on the platform

            @Params : void
        """
        self.logger.write_to_console("EVENT", "{0} Updating Admin {1}".format(self.user['username'], str(request_data)))
        
        self.logger.write_to_console("EVENT", "Preparing data")

        request_data['msisdn'] = "233" + request_data['msisdn'][-9:]

        res = self.model.updateAdministrator(request_data)
        if res == True:
            return {"code":language.CODES['SUCCESS'], "msg":self.lang['admin_updated'], "data":[]}
        else:
            return {"code":language.CODES['FAIL'], "msg":self.lang['admin_update_failed'], "data":[]}


    def changeAdminPassword(self, request_data):
        """
            This function handles all logic related to login on the platform

            @Params : void
        """
        self.logger.write_to_console("EVENT", "{0} changing Admin password {1}".format(self.user['username'], str(request_data)))

        if request_data['newPassword'] == request_data['oldPassword']:
            return {"code":language.CODES['FAIL'], "msg": "New password can not be the same as the old password.", "data":[]}

        utl = Utilites()
        comple = utl.password_complexity_check(request_data['newPassword'])
        print(comple)
        if comple['strength'] < 10:
            self.logger.write_to_console("EVENT", "password_weak_password"+ self.user['username'] + " | Password change.")
            return {"code":language.CODES['FAIL'], "msg": "The password entered is weak. Kindly make sure the password length is 8 and above and contains a a least one digit symbol uppercase and lowercase", "data":[]}

        if request_data['newPassword'] == request_data['newPasswordRep']:
            admin_data = self.model.getAdminByUsername_chg(self.user['username'])
            if admin_data == []:
                self.logger.write_to_console("EVENT", "User does not exit "+ self.user['username'] + " | Non-Existing User.")
                return {"code":language.CODES['FAIL'], "msg":self.lang['wrong_username'], "data":[]}
            else:
                verify_pass = sha256_crypt.verify(request_data['oldPassword'], admin_data[0]['password'])
                self.logger.write_to_console("EVENT", "varify Password | "+ str(verify_pass))
                
                if verify_pass == True:
                    password = sha256_crypt.encrypt(request_data['newPassword'])
                    res = self.model.updateAdministrator({"password":password, "username":self.user['username'], "pass_date": "NOW()"})
                    if res == True:
                        admin_data = self.model.getAdminByUsernameLogin(self.user['username'])
                        try:
                            Utilites.send_mail(Utilites, "SSNIT PASSWORD CHANGE", "<p>Hi {0}</p><p>Your SSNIT password has been changed. If you are not aware of this change kindly send a mail to <a>support@nsano.com</a>.<br><br>Best Regards</p><p>FUSION PLATFORM</p>".format(admin_data[0]['first_name']), [admin_data[0]['email']])
                        except Exception as e:
                            pass
                        return {"code":language.CODES['SUCCESS'], "msg":self.lang['admin_sucessful_pass_change'], "data":admin_data[0]}
                    else:
                        return {"code":language.CODES['FAIL'], "msg":self.lang['admin_update_failed'], "data":[]}
                else:
                    self.logger.write_to_console("EVENT", "wrong previous password "+ self.user['username'] + " | Password change.")
                    return {"code":language.CODES['FAIL'], "msg":self.lang['wrong_old_password'], "data":[]}

        else:
            self.logger.write_to_console("EVENT", "password_mismatch "+ self.user['username'] + " | Password change.")
            return {"code":language.CODES['FAIL'], "msg":self.lang['password_mismatch'], "data":[]}


    def resetAdminPassword(self, request_data):
        """
            This function handles all logic related to login on the platform

            @Params : void
        """
        self.logger.write_to_console("EVENT", "{0} resting Admin password {1}".format(request_data['username'], str(request_data)))

        admin_data = self.model.getAdminByUsername(request_data['username'])
        if admin_data == []:
            self.logger.write_to_console("EVENT", "Login request failed for "+ request_data['username'] + " | Non-Existing User.")
            return {"code":language.CODES['FAIL'], "msg":self.lang['wrong_username'], "data":[]}
        else:
            utl = Utilites()
            raw_password = utl.generate_password(10)
            # raw_password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))
            password = sha256_crypt.encrypt(raw_password)
            self.logger.write_to_console("EVENT", "Generated password: {0} \n Hashed Password: {1} \n".format(raw_password, password))
            
            res = self.model.updateAdministrator({"password":password, "username":request_data['username']})
            if res == True:
                Utilites.send_mail(Utilites, "SSNIT PASSWORD RESET", "<p>Hi {0}</p><p>Your SSNIT password has been changed to <strong>{1}</strong>.<br>Keeping your password safe is your responsibility.<br><br><br><br>Regards</p><p>FUSION PLATFORM</p>".format(request_data['username'], raw_password), [admin_data[0]['email']])
                return {"code":language.CODES['SUCCESS'], "msg":(self.lang['admin_pass_reset_successful']+ admin_data[0]['email']), "data":[]}
            else:
                return {"code":language.CODES['FAIL'], "msg":self.lang['admin_pass_reset_failed'], "data":[]}


    def searchAdmins(self, request_data):
        """
            This function handles all logic related to login on the platform

            @Params : void
        """
        print(request_data)
 
        self.logger.write_to_console("EVENT", "Searching Transactions for {0}".format(request_data['search_param']))
        admin_data = []
        if self.user['branch_code'] == "All":
            admin_data = self.model.searchAdmins(request_data)
        else:
            admin_data = self.model.searchAdminsBranch(request_data)

        for result in admin_data:
            result["created"] = result["created"].strftime("%Y-%m-%d %H:%M:%S")
            result["last_login"] = result["last_login"].strftime("%Y-%m-%d %H:%M:%S")
            
            if "pass_date" in result and result['pass_date'] is not None:
                result["pass_date"] = result["pass_date"].strftime("%Y-%m-%d %H:%M:%S")
            
            if result["active"] == 1:
                result["active"] = self.lang["active"]
            else:
                result["active"] = self.lang["inactive"]
        
        return admin_data




    def getAllBranches(self, request_data):
        """
            This function gets branches in the db

            @Params : void
        """
        print("inside get branches route ", str(request_data))
        if request_data == {}:
            request_data = {'offset':0, 'records':11}
        else:
            request_data['offset'] = int(request_data['page'])*11
            request_data['records'] = 11
 
        #self.logger.write_to_console("EVENT", "Getting branches list for {0} -> {1}".format(self.user['username'], request_data))
        
        branches_data = self.model.getBranches(request_data)
        print(branches_data)
        self.logger.write_to_console("EVENT", "Branches list gotten successfully for {}".format(self.user['username']))
        return branches_data

    def getAllBranchesFully(self):
        filter_data={}
        filter_data['branches'] = self.model.dbconn.select_from_table("tbl_branches")
        print(filter_data)
        return filter_data

    def getAllBranchesExport(self):
        """
            This function handles all logic related to login on the platform

            @Params : void
        """
        request_data = {}
        request_data['offset'] = 0
        request_data['records'] = 10000

        # inst_model = Institution(self.user)
 
        self.logger.write_to_console("EVENT", "Getting administrator list for {} -> {}".format(self.user['username'], request_data))

        export_list = [['BRANCH ID', 'ACRONYM', 'BRANCH NAME', 'BRANCH CODE']]
        
        branches_data =  self.model.getBranches()
        for result in branches_data:
            export_list.append([result['branch_id'], result['acronym'], result['branch_name'], result['branch_code']])

        self.logger.write_to_console("EVENT", "Branches Export list gotten successfully for {}".format(self.user['username']))
        return export_list


    def searchBranches(self, request_data):
        """
            This function handles all logic related to login on the platform

            @Params : void
        """
        print(request_data)
 
        self.logger.write_to_console("EVENT", "Searching Transactions for {0}".format(request_data['search_param']))
        admin_data = []
        
        admin_data = self.model.searchBranches(request_data)
        
        return admin_data

    def addBranch(self, request_data):
        """
            This function handles all logic related to login on the platform

            @Params : void
        """
        self.logger.write_to_console("EVENT", "{0} Adding Branch {1}".format(self.user['username'], str(request_data)))
        branch_codes = self.model.getBranchByCode(request_data['branch_code'])
        if branch_codes == []:
            res = self.model.addAdminBranch(request_data)
            if res == True:
                self.logger.write_log("ADMIN", "ADDED BRANCH | {} | SUCESSFUL | {}".format(str(request_data), self.user['username']))
                return {"code":language.CODES['SUCCESS'], "msg": "New branch added successfully.", "data":[]}
            else:
                return {"code":language.CODES['FAIL'], "msg": "Failed to add branch.", "data":[]}
        else:
             return {"code":language.CODES['FAIL'], "msg": "Branch code already exist", "data":[]}


    def removeBranch(self, request_data):
        """
            This function handles all logic related to login on the platform

            @Params : void
        """
        self.logger.write_to_console("EVENT", "{0} Adding Branch {1}".format(self.user['username'], str(request_data)))

        res = self.model.removeAdminBranch(request_data)
        if res == True:
            self.logger.write_log("ADMIN", "REMOVED BRANCH | {} | SUCESSFUL | {}".format(str(request_data), self.user['username']))
            return {"code":language.CODES['SUCCESS'], "msg": "New branch removed successfully.", "data":[]}
        else:
            return {"code":language.CODES['FAIL'], "msg": "Failed to remove branch.", "data":[]}