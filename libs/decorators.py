# Importing flask Dependencies
from flask import request
from flask import Response, flash
from flask import render_template
from flask import url_for, redirect
from functools import wraps
from app.libs.logger import Logger

class AccessLogger():
    """
    Class: AccessLogger
    -------------------
    Logs all the sorce ip, method an route for each requets
    Return: Function
    """
    def __init__(self):
        self.logger = Logger()

    def log_request(self, f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            self.logger.write_log("ACCESS", "{} | {} | {}".format(request.remote_addr, request.method, request.url))
            return f(*args, **kwargs)
        return wrapper
