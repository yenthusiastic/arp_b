# -*- encoding: utf-8 -*-
"""
Light Bootstrap Dashboard - coded in Flask

Author  : AppSeed App Generator
Design  : Creative-Tim.com
License : MIT 
Support : https://appseed.us/support 
"""

from app         import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'USERS'
    id       = db.Column(db.Integer,     primary_key=True)
    user     = db.Column(db.String(20),  unique = True)
    email    = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(500))
    data = db.Column(db.JSON())

    def __init__(self, user, email, password, data):
        self.user       = user
        self.password   = password
        self.email      = email
        self.data = data

    def __repr__(self):
        return '<User %r>' % (self.id)

    def save(self):

        # inject self into db session    
        db.session.add ( self )

        # commit change and save the object
        db.session.commit( )

        return self 


class SensorData(db.Model):
    __tablename__ = 'SENSOR_DATA'
    id = db.Column(db.BigInteger, primary_key = True, nullable = False)
    hardwareID = db.Column(db.Integer, nullable = False)
    address = db.Column(db.Text, nullable = False) 
    latitude = db.Column(db.Float, nullable = False)
    longitude = db.Column(db.Float, nullable = False)
    temperature = db.Column(db.Float, nullable = False)
    humidity = db.Column(db.Float, nullable = False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    
    def __init__(self, hardwareID, address, latitude, longitude, temperature, humidity):
        self.hardwareID = hardwareID
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.temperature = temperature
        self.humidity = humidity
    
    def __repr__(self):
        return '<Hardware ID: {}, address: {}>'.format(self.hardwareID, self.address)
    
    
class Hardware(db.Model):
    __tablename__ = 'HARDWARE_STATUS'
    hardwareID = db.Column(db.Integer, primary_key = True, nullable = False)
    address_index = db.Column(db.Integer, nullable = False) 
    session_address = db.Column(db.Text, nullable = False) 
    status = db.Column(db.String(10), nullable=False)
    latitude = db.Column(db.Float, nullable = False)
    longitude = db.Column(db.Float, nullable = False)
   
    
    def __init__(self, hardwareID, address_index, status, latitude, longitude):
        self.hardwareID = hardwareID
        self.address_index = address_index
        self.status = status
        self.latitude = latitude
        self.longitude = longitude
    
    def __repr__(self):
        return '<Hardware ID: {}, address index: {}>'.format(self.hardwareID, self.address_index)