# werkzeug Imports Needed
# Import password / encryption helper tools

# Importing other dependencies
import uuid
import datetime
import hashlib, random
import base64
import os

from passlib.hash import sha256_crypt

from app import config
from app import language
from app.logs.model import ValidationLog
class logService(object):
    """
        Class contains functions and attributes for authtentication
        Function: * getCampainge(sel)
    """
    def __init__(self, user):
        self.lang = {}
        self.lang = getattr(language, config.DEFAULT_LANG)
        self.user = user
        self.model = ValidationLog()

    def getAllHistory(self):
        return self.model.query.all()


    

    
