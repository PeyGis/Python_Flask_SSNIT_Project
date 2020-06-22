import os
import datetime
from app.libs.api_calls import ApiCalls
import uuid
import hashlib, random
import base64
from random import choice
import re
from app import config

class Utilites():
    """docstring for log"""
    
    '''
    Writing into files
    '''
    def generate_password(self, length=10):
        """
        Function to generate a password
        """

        char_set = {
                 'small': 'abcdefghijklmnopqrstuvwxyz',
                 'nums': '0123456789',
                 'big': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                 # 'special': '^!\$%&/()=?{[]}+~#-_.:,;<>|\\'
                }

        password = []

        while len(password) < length:
            key = choice(list(char_set.keys()))
            # a_char = str(urandom(1))
            a_char = choice(char_set[key])
            if a_char in char_set[key]:
                if self.check_prev_char(password, char_set[key]):
                    continue
                else:
                    password.append(a_char)
        return ''.join(password)


    def check_prev_char(self, password, current_char_set):
        """
        Function to ensure that there are no consecutive 
        UPPERCASE/lowercase/numbers/special-characters.
        """

        index = len(password)
        if index == 0:
            return False
        else:
            prev_char = password[index - 1]
            if prev_char in current_char_set:
                return True
            else:
                return False


    def password_complexity_check(self, password):
        """
        Verify the strength of 'password'
        Returns a dict indicating the wrong criteria
        A password is considered strong if:
            8 characters length or more
            1 digit or more
            1 symbol or more
            1 uppercase letter or more
            1 lowercase letter or more
        """

        # Strength Value
        strength = 10

        # calculating the length
        length_error = len(password) < 8
        if length_error == True:
            strength -= 2

        # searching for digits
        digit_error = re.search(r"\d", password) is None
        if digit_error == True:
            strength -= 2

        # searching for uppercase
        uppercase_error = re.search(r"[A-Z]", password) is None
        if uppercase_error == True:
            strength -= 2

        # searching for lowercase
        lowercase_error = re.search(r"[a-z]", password) is None
        if lowercase_error == True:
            strength -= 2

        # searching for symbols
        symbol_error = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~@"+r'"]', password) is None
        if symbol_error == True:
            strength -= 2

        # overall result
        password_ok = not ( length_error or digit_error or uppercase_error or lowercase_error or symbol_error )

        return {
            'password_ok' : password_ok,
            'length_error' : length_error,
            'digit_error' : digit_error,
            'uppercase_error' : uppercase_error,
            'lowercase_error' : lowercase_error,
            'symbol_error' : symbol_error,
            'strength': strength
        }


    '''
    Writing into files
    '''
    def send_mail(self, subject, msg, receipients=[]):
        # Get time
        # today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")
        # Form message
        # msg = str(today) + " | " + log_level + " | " + msg + "\n"
        request_data = {
                        "subject": subject,
                        "message": msg,
                        "recipients": ",".join(receipients),
                        "signature": '',
                        "sender_name": "SSNIT",
                        "sender_email": "",
                        "password": "",
                        }
        res = ApiCalls.request_api_raw(ApiCalls, request_data, url=config.EMAIL_URL, headers=config.MAIL_HEADER)
        print(res.text)

        return res
        

    '''
    Writing into files
    '''
    def format_msisdn(self, msg, receipients=[]):
        # Get time
        today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")
        # Form message
        msg = str(today) + " | " + log_level + " | " + msg + "\n"

        # Send Error Alert to SmartDog
        if extra_data != None:
            request_data = {"tag": "app_trigger_error_sig",
                        "apikey": "123456789abcdefghijk",
                        "appID": "NS00001",
                        "error_msg": extra_data['msg'],
                        "error_type": extra_data['type'],
                        "error_time": str(today),
                        "error_author": "USSD GATEWAY",
                        "module_name": extra_data['module'],
                        "error_severity": extra_data['severity'],
                        "emails": ALERT_LIST }
            ApiCalls.request_api(ApiCalls, request_data)


    def call_et_api(self, module, group="user", details={}):
        req_obj={"apiKey": "0657015ea18b7233bb2841dd0499cdf4f2fce88c", \
             "apiVersion": "v1_0", \
             "module": module, \
             "group": group, \
             "details": details \
            }
        print(req_obj)
        headers = { 'Content-Type': 'application/json' }
        result = requests.post("http://127.0.0.1:5055", data=json.dumps(req_obj), headers=headers)
        result = json.loads(result.text)
        #conn = http.client.HTTPConnection("45.79.139.232:5055")
        #conn.request("POST", "/", json.dumps(req_obj), headers)

        #res = conn.getresponse()
        #data = res.read()
        #result = data.decode("utf-8")
        print("Got Reponse  ")
        print(result)
        return result


    def initiateManillaTransactionData(self, data):
        order_id = str(uuid.uuid4()).replace('-','')[:15]
        checksum = self.checksum_generator(self, data['source_ip'], '301152115708', data['amount'])

        data['order_id'] = order_id
        data['checksum'] = checksum
        data['merchant_id'] = '301152115708'

        res = {"code": "00", "msg":"Initiated", "data":data}
        return res


    def checksum_generator(self, merchant_ip, merchant_id, total_amount):
        info = '{0}{1}{2}'.format(merchant_ip, merchant_id, total_amount)
        salt_size = 6
        chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        _salt = ''.join(random.choice(chars) for i in range(salt_size))
        _checksum = hashlib.md5(info.encode('utf-8')).hexdigest()
        _checksum = list(_checksum)
        _checksum.insert(5, _salt)
        _checksum = ''.join(_checksum)
        return _checksum

