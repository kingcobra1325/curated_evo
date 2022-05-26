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
        self.PRODUCTION = environ['PRODUCTION']
        self.SERVICE_EMAIL = environ['SERVICE_EMAIL']
        self.SPREADSHEET_ID = environ['SPREADSHEET_ID']
        self.DRIVER_PATH = environ['DRIVER_PATH']
        self.GOOGLE_API_KEY = ast.literal_eval(environ['GOOGLE_SERVICE_ACCOUNT'])
    
    def __repr__(self):
        repr_string = ''
        for k,v in self.__dict__.items():
            repr_string = repr_string + f"{k} -> {v}\n"
        return repr_string

ENV = EnvVariables()