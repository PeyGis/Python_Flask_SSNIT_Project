import os
import datetime
from app.config import ACCESS_LOG_PATH, EVENT_LOG_PATH, ERROR_LOG_PATH, CS_REQ_LOG_PATH, AD_REQ_LOG_PATH, USER_ACCESS_LOG_PATH, UPLOAD_LOG_PATH, PROCESS_UPLOAD_LOG_PATH
# from appLibs.api_calls import api_calls

class Logger():
    """docstring for log"""
    def __init__(self):
        try:
            self.access_file = os.path.abspath(ACCESS_LOG_PATH)
            self.event_file = os.path.abspath(EVENT_LOG_PATH)
            self.error_file = os.path.abspath(ERROR_LOG_PATH)
            self.cs_req_file = os.path.abspath(CS_REQ_LOG_PATH)
            self.upload_file = os.path.abspath(UPLOAD_LOG_PATH)
            self.process_upload_file = os.path.abspath(PROCESS_UPLOAD_LOG_PATH)
            self.ad_req_file = os.path.abspath(AD_REQ_LOG_PATH)
            self.ad_access_file = os.path.abspath(USER_ACCESS_LOG_PATH)
            # self.http_error_url = SMARTDOG_URL
            # self.http_event_url = "http://localhost:5000/logs"
            pass
        except Exception as e:
            raise e

    '''
    Writing into files
    '''
    def write_to_file(self, log_level="EVENT", msg="", extra_data=None):
        # Get time
        today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")
        filename_perf = datetime.datetime.now().strftime("%Y-%m-%d")
        # Form message
        msg = str(today) + " | " + log_level + " | " + msg + "\n"

        # Get file
        if log_level == "ERROR":
            filename = self.error_file+ "/" +filename_perf +".log"
            # Send Error Alert to SmartDog
            # if extra_data != None:
            #   request_data = {"tag": "app_trigger_error_sig",
            #               "apikey": "123456789abcdefghijk",
            #               "appID": "NS00001",
            #               "error_msg": extra_data['msg'],
            #               "error_type": extra_data['type'],
            #               "error_time": str(today),
            #               "error_author": "USSD GATEWAY",
            #               "module_name": extra_data['module'],
            #               "error_severity": extra_data['severity'],
            #               "emails": ALERT_LIST }
            #   api_calls.request_api(api_calls, request_data)

        elif log_level == "EVENT":
            filename = self.event_file+ "/" +filename_perf +".log"
        elif log_level == "ACCESS":
            filename = self.access_file+ "/" +filename_perf +".log"
        elif log_level == "UPLOAD":
            filename = self.upload_file+ "/" +filename_perf +".log"
        elif log_level == "PROCESS_UPLOAD":
            filename = self.process_upload_file+ "/" +filename_perf +".log"

        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, "a") as f:
            f.write(msg)
        pass

        '''
    Writing into files
    '''
    def write_to_console(self, log_level="EVENT", msg="", extra_data=None):
        # Get time
        today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")
        # Form message
        msg = str(today) + " | " + log_level + " | " + msg + "\n"   
        # Print to screen
        print(msg)
        pass

    '''
    Writing into files and console
    '''
    def write_log(self, log_level="EVENT", msg="", extra_data=None):
        # Get time
        today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")
        filename_perf = datetime.datetime.now().strftime("%Y-%m-%d")
        # Form message
        msg = str(today) + " | " + log_level + " | " + msg + "\n"

        print(msg)

        # Get file
        if log_level == "ERROR":
            filename = self.error_file+ "/" +filename_perf +".log"
            # Send Error Alert to SmartDog
            # if extra_data != None:
            #   request_data = {"tag": "app_trigger_error_sig",
            #               "apikey": "123456789abcdefghijk",
            #               "appID": "NS00001",
            #               "error_msg": extra_data['msg'],
            #               "error_type": extra_data['type'],
            #               "error_time": str(today),
            #               "error_author": "USSD GATEWAY",
            #               "module_name": extra_data['module'],
            #               "error_severity": extra_data['severity'],
            #               "emails": ALERT_LIST }
            #   api_calls.request_api(api_calls, request_data)

        elif log_level == "EVENT":
            filename = self.event_file+ "/" +filename_perf +".log"
        elif log_level == "ACCESS":
            filename = self.access_file+ "/" +filename_perf +".log"
        elif log_level == "USER_ACCESS":
            filename = self.ad_access_file+ "/" +filename_perf +".log"
        elif log_level == "ADMIN":
            filename = self.ad_req_file+ "/" +filename_perf +".log"
        elif log_level == "CUSTOMER":
            filename = self.cs_req_file+ "/" +filename_perf +".log"
        elif log_level == "UPLOAD":
            filename = self.upload_file+ "/" +filename_perf +".log"
        elif log_level == "PROCESS_UPLOAD":
            filename = self.process_upload_file+ "/" +filename_perf +".log"

        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, "a") as f:
            f.write(msg)
        pass




    '''
    TODO
    '''


    # def write_to_http_socket(self, log_level, msg):
    #   # Get time
    #   today = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S:%f")
    #   # Form message
    #   msg = str(today) + " | " + log_level + " | " + msg

    #   # Get file
    #   if log_level == "ERROR":
    #       filename = self.error_file
    #   elif log_level == "EVENT":
    #       filename = self.event_file
    #   elif log_level == "ACCESS":
    #       filename = self.access_file
        
    #   os.makedirs(os.path.dirname(filename), exist_ok=True)
        
    #   with open(filename, "a") as f:
    #       f.write(msg)
    #   pass

# if __name__ == '__main__':
#   logger = logger()
#   logger.write_to_console("EVENT", "TEST EVENT")
    # logger.write_to_file("EVENT", "TEST EVENT")

