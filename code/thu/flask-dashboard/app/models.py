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
from sqlalchemy.dialects.postgresql import ARRAY, array


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
    index = db.Column(db.BigInteger, primary_key = True, nullable = False)
    hardwareID = db.Column(db.Integer, nullable = False)
    address = db.Column(db.Text) 
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    co2 = db.Column(db.Float)
    pressure = db.Column(db.Float)
    pm10 = db.Column(db.Float)
    pm25 = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    
    def __init__(self, hardwareID, address, latitude, longitude, temperature, humidity, co2, pressure, pm10, pm25):
        self.hardwareID = hardwareID
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.temperature = temperature
        self.humidity = humidity
        self.co2 = co2
        self.pressure = pressure
        self.pm10 = pm10
        self.pm25 = pm25
    
    def __repr__(self):
        return '<Hardware ID: {}, address: {}>'.format(self.hardwareID, self.address)
    
    
class Hardware(db.Model):
    __tablename__ = 'HARDWARE_STATUS'
    hardwareID = db.Column(db.Integer, primary_key = True, nullable = False)
    address_index = db.Column(db.Integer) 
    session_address = db.Column(db.Text) 
    status = db.Column(db.String(10))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    sensors = db.Column(ARRAY(db.Text))
    place = db.Column(db.Text) 
    seed = db.Column(db.Text)
   
    
    def __init__(self, hardwareID, address_index, session_address, status, latitude, longitude, sensors):
        self.hardwareID = hardwareID
        self.address_index = address_index
        self.session_address = session_address
        self.status = status
        self.latitude = latitude
        self.longitude = longitude
        self.sensors = sensors

    def save(self):

        # inject self into db session    
        db.session.add ( self )

        # commit change and save the object
        db.session.commit( )
        return self 
    
    def __repr__(self):
        return '<Hardware ID: {}, address index: {}>'.format(self.hardwareID, self.address_index)