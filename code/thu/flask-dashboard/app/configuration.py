# -*- encoding: utf-8 -*-
"""
Light Bootstrap Dashboard - coded in Flask

Author  : AppSeed App Generator
Design  : Creative-Tim.com
License : MIT 
Support : https://appseed.us/support 
"""

import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    CSRF_ENABLED = True
    #SERVER_NAME="127.0.0.1:5020"
    SECRET_KEY   = "77tgFCdrEEdv77554##@3" 
    SQLALCHEMY_TRACK_MODIFICATIONS 	= False
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://arp_b:iota999@db.dev.iota.pw:6000/arp_b"
