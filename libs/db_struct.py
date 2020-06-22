# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
#from app import db

# Define a base model for other database tables to inherit
# class Base(db.Model):

from mongokit import *

import datetime
import config

# Grab a database connection
connection = Connection(host=config.MONGO_HOST, port=config.MONGO_PORT)

# Define a Login model
@connection.register
class Login(Document):
    __collection__ = 'users'
    __database__   = config.MONGO_DATABASE
    structure = {
      'username': str,
      'password': str,
      'access_level': str,
      'institution': str,
      'first_name': str,
      'last_name': str,
      'last_name': str,
      'email': str,
      'msisdn': str,
      'status': int,
      'created_at': datetime.datetime,
      'pass_date': datetime.datetime
    }
    required_fields = ['username', 'password', 'created_at', 'access_level', 'institution', 'email', 'msisdn']
    default_values = {
      'status': 0,
      'created_at': datetime.datetime.utcnow,
      'pass_date': datetime.datetime.utcnow
    }
    use_dot_notation = True


# Define a Country model
@connection.register
class Api_routes(Document):
    __collection__ = 'api_routes'
    __database__   = config.MONGO_DATABASE
    structure = {
      'data': list,
    }
    # required_fields = ['countryCode', 'countryName', 'currencyCode', 'languages']
    use_dot_notation = True

