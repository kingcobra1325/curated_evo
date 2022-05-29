# Install Missing Modules
from . import missing_modules

import ast
from os import environ
from dotenv import load_dotenv

# LOAD ENV VARIABLES
load_dotenv('.env')

class EnvVariables:

    # DEFAULT VARS
    def __init__(self):
        self.PRODUCTION = environ.get('PRODUCTION')
        self.SERVICE_EMAIL = environ.get('SERVICE_EMAIL')
        self.SPREADSHEET_ID = environ.get('SPREADSHEET_ID')
        self.DRIVER_PATH = environ.get('DRIVER_PATH')
        try:
            self.GOOGLE_API_KEY = ast.literal_eval(environ.get('GOOGLE_SERVICE_ACCOUNT'))
        except ValueError:
            self.GOOGLE_API_KEY = None
    
    def __repr__(self):
        repr_string = ''
        for k,v in self.__dict__.items():
            repr_string = repr_string + f"{k} -> {v}\n"
        return repr_string

ENV = EnvVariables()