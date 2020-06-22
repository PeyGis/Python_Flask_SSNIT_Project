import json
import socket
import requests
from app.config import API_URL, DEF_HEADER, SOCKET_IP, SOCKET_PORT

class ApiCalls():
    """
    This class contains all function calls to external APIs
    """

    def request_api(self, req_params, route='', method='post', url=API_URL, headers=DEF_HEADER):
        """
        This function makes and get response form fusion Virtuals account API

        @Params : req_params [dict]
        @Params : models [str]
        @Params : functions [str]
        @Params : method [str] val ['post', 'get']
        @Params : url [str]
        @Params : headers [dict]
        """
        req_data={}
        if route != '':
            url += route

        if route != {}:
            req_data = req_params

        if method == 'post':
            r = requests.post(url, data=req_data, headers=headers).json()
        elif method == 'get':
            r = requests.get(url, params=req_data, headers=headers).json()
        elif method == 'put':
            r = requests.put(url, data=req_data, headers=headers).json()
        elif method == 'delete':
            r = requests.delete(url, data=req_data, headers=headers).json()
        elif method == 'patch':
            r = requests.patch(url, data=req_data, headers=headers).json()
        else:
            return {"code":"00", "msg":"Method is not supported."}
        
        return r


    def request_api_raw(self, req_params, route='', method='post', url=API_URL, headers=DEF_HEADER):
        """
        This function makes and get response form fusion Virtuals account API

        @Params : req_params [dict]
        @Params : models [str]
        @Params : functions [str]
        @Params : method [str] val ['post', 'get']
        @Params : url [str]
        @Params : headers [dict]
        """
        req_data={}
        if route != '':
            url += route

        if route != {}:
            req_data = req_params

        if method == 'post':
            r = requests.post(url, data=req_data, headers=headers)
        elif method == 'get':
            r = requests.get(url, params=req_data, headers=headers)
        elif method == 'put':
            r = requests.put(url, data=req_data, headers=headers)
        elif method == 'delete':
            r = requests.delete(url, data=req_data, headers=headers)
        elif method == 'patch':
            r = requests.patch(url, data=req_data, headers=headers)
        else:
            return {"code":"00", "msg":"Method is not supported."}
        
        return r


    def request_api_json(self, req_params, route='', method='post', url=API_URL, headers=DEF_HEADER):
        """
        This function makes and get response form fusion Virtuals account API

        @Params : req_params [dict]
        @Params : models [str]
        @Params : functions [str]
        @Params : method [str] val ['post', 'get']
        @Params : url [str]
        @Params : headers [dict]
        """
        req_data={}
        if route != '':
            url += route

        if route != {}:
            req_data = req_params

        if method == 'post':
            r = requests.post(url, json=req_data, headers=headers).json()
        elif method == 'get':
            r = requests.get(url, params=req_data, headers=headers).json()
        elif method == 'put':
            r = requests.put(url, data=json.dumps(req_data), headers=headers).json()
        elif method == 'delete':
            r = requests.delete(url, data=json.dumps(req_data), headers=headers).json()
        elif method == 'patch':
            r = requests.patch(url, data=json.dumps(req_data), headers=headers).json()
        else:
            return {"code":"00", "msg":"Method is not supported."}
        
        return r


    def request_api_raw_json(self, req_params, route='', method='post', url=API_URL, headers=DEF_HEADER):
        """
        This function makes and get response form fusion Virtuals account API

        @Params : req_params [dict]
        @Params : models [str]
        @Params : functions [str]
        @Params : method [str] val ['post', 'get']
        @Params : url [str]
        @Params : headers [dict]
        """
        req_data={}
        if route != '':
            url += route

        if route != {}:
            req_data = req_params

        if method == 'post':
            r = requests.post(url, data=json.dumps(req_data), headers=headers)
        elif method == 'get':
            r = requests.get(url, data=req_data, headers=headers)
        elif method == 'put':
            r = requests.put(url, data=json.dumps(req_data), headers=headers)
        elif method == 'delete':
            r = requests.delete(url, data=json.dumps(req_data), headers=headers)
        elif method == 'patch':
            r = requests.patch(url, data=json.dumps(req_data), headers=headers)
        else:
            return {"code":"00", "msg":"Method is not supported."}
        
        return r

    def get_all_api_routes(self, req_params):
        apis = self.request_api(req_params, method='get',url=API_URL)
        return apis

    def get_url_for(self, func, apis):
        url = None
        for api in apis:
            if api['rel'] == func:
                url = api['uri']
                break

        return url

    """
    This class contains functions that process the request data
    """
    def send_socket_data(self, data):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((SOCKET_IP, SOCKET_PORT))
            s.send(data)
            rec_data = s.recv(4096)
            s.close()
            return rec_data;
        except Exception as e:
            return b'3sgyoobWi8qzmpW5EmjZdVs16gJzTeIZlQiFHRu/gn8j/AhZJtcwyxFLrb3J4osDrxscrMFKlPYGAiPOzqgx/A=='
            # raise e
        