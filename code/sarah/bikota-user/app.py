from flask import Flask, render_template, request
from sqlalchemy.dialects.postgresql import ARRAY, array
from flask_sqlalchemy import SQLAlchemy

import psycopg2 
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim


app = Flask(__name__, template_folder="templates")

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://arp_b:iota999@db.dev.iota.pw:6000/arp_b"  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = "FALSE"


db = SQLAlchemy(app) # flask-sqlalchemy)

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


geolocator = Nominatim(user_agent="Bikota", timeout=10)
hour_diff = 0
multiplier = 1
units = {
    "Temperature" : "°C",
    "Humidity" : "%H",
    "CO2" : "PPM",
    "Pressure" : "hPa",
    "PM10" : "ug/m<sup>3</sup>",
    "PM25" : "ug/m<sup>3</sup>"
}

chart_colors = ["112, 214, 96", 
                "255,102,102",
                "245,206,66", 
                "75,192,192", 
                "123, 152, 237",
                "222, 129, 227",
                "75,192,192", 
                "245,206,66", 
                "112, 214, 96", 
                "123, 152, 237",
                "222, 129, 227"]

db_host='db.dev.iota.pw'
db_port=6000
database='arp_b'
user='arp_b'
password='iota999'

def connect_DB():
    try:        
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(host=db_host, port=db_port, user=user, password=password, database=database)
        print("Successfully connected to DB")
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return -1

conn = connect_DB()

def exec_query(msg, num_values):
    print("""Executing SQL query on Database server...""")
    try:
        cur = conn.cursor()
        cur.execute(msg)
        conn.commit()
        res = cur.fetchall()
        if res:
            if num_values == 1:
                res = [r[0] for r in res]
                print('Success. Database connection closed.')
                return res
            elif num_values == 2:
                timestamp = []
                #values = []
                selector_data = []
                for row in res:
                    timestamp.append(row[0])
                    selector_data.append(row[1])
                #values.append(selector_data)
                print('Success. Database connection closed.')
                return timestamp, selector_data
            else:
                timestamp = []
                values = []
                for row in res:
                    timestamp.append(row[0])
                for index in range (1, num_values):
                    selector_data = []
                    for row in res:
                        selector_data.append(row[index])
                    values.append(selector_data)
                print('Success. Database connection closed.')
                return timestamp, values
        else:
            print("No data fetched from query: {}".format(msg))
            return -1
            
    except:
        print("Error while executing SQL query: {}".format(msg))
        return -1

def query_data_addr(selector, addr):
    global hour_diff, multiplier
    begin_time = db.session.query(SensorData.timestamp).filter(SensorData.address==addr).order_by(SensorData.timestamp.asc()).first()[0]
    end_time = db.session.query(SensorData.timestamp).filter(SensorData.address==addr).order_by(SensorData.timestamp.desc()).first()[0]
    hour_difference = int((end_time -  begin_time)/timedelta(minutes=5)/24)
    multiplier = 5
    if hour_difference < 1:
        hour_difference = int((end_time -  begin_time)/timedelta(minutes=1)/12)
        multiplier = 3
        if hour_difference < 10:
            hour_difference = int((end_time -  begin_time)/timedelta(minutes=1)/4)
            multiplier = 1
    print("hour_difference, multplier: ", hour_difference, multiplier)
    hour_diff = hour_difference
    if hour_difference != 0:
        query = 'SELECT "timestamp", "{0}" FROM (SELECT "timestamp", "address", "{0}", "index" '.format(selector)
        query += 'FROM public."SENSOR_DATA" WHERE "{}" IS NOT NULL AND '.format(selector)
        query += """ "address" = '{0}' ORDER BY "timestamp" DESC) AS TEMP_TABLE WHERE index%({1}*{2}) = 0 ORDER BY TEMP_TABLE."timestamp" ASC """.format(addr, hour_difference, multiplier)
        print("""Executing SQL query on Database server...""")
        print(query)
        return exec_query(query, 2)
    else:
        print("No data found for selected address")
        return -1

def query_session_loc(addr):
    global hour_diff, multiplier
    if hour_diff != 0:
        query = 'SELECT * FROM (SELECT "timestamp", "latitude", "longitude", "index" '
        query += 'FROM public."SENSOR_DATA" WHERE "latitude" IS NOT NULL AND "longitude" IS NOT NULL AND '
        query += """ "address" = '{0}' ORDER BY "timestamp" DESC) AS TEMP_TABLE WHERE index%({1}*{2}) = 0 ORDER BY TEMP_TABLE."timestamp" ASC """.format(addr, 1,1)
        print("""Executing SQL query on Database server...""")
        return exec_query(query, 3)
    else:
        print("No data found for selected address")
        return -1

@app.route('/', methods=["GET", "POST"])
@app.route('/home', methods=["GET", "POST"])
@app.route('/index.html', methods=["GET", "POST"])
def home():
    """Landing page."""
    geojson_data_arr = []
    hardware_data = db.session.query(Hardware.hardwareID, Hardware.latitude, Hardware.longitude, Hardware.place).filter(Hardware.status=="Parked").all()
    for hardware in hardware_data:
        if hardware[1] is not None and hardware[2] is not None:
            try:
                loc = geolocator.reverse("{}, {}".format(hardware[1], hardware[2])).raw["address"]
            except:
                loc = "Unknown"
            geojson_data_arr.append({
                "type": "Feature",
                "properties": {
                    "name": hardware[0],
                    "place": hardware[3],
                    "popupContent": "Hardware {0}<br>Location (lat, lon): <a target='_blank' href='https://google.com/maps/dir//{1},{2}'>{1}, {2}</a><br>Detailed location: {3}".format(hardware[0], hardware[1], hardware[2], loc)
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [hardware[2], hardware[1]]
                }
            })

    if request.method == "POST":
        chart_data = []
        session_addr = ""
        print(request.form)
        
        try:
            session_addr = request.form["session_address"]
            print(session_addr)

            #temp_sensor = db.session.query(SensorData.address, SensorData.co2, SensorData.hardwareID, SensorData.humidity, SensorData.index, SensorData.pressure, SensorData.timestamp).filter(SensorData.address==session_addr).distinct().order_by(SensorData.address).all()
            #print(temp_sensor)
            #temp_sensor_co2 = db.session.query(SensorData.address, SensorData.co2, SensorData.timestamp).filter(SensorData.address==session_addr).distinct().order_by(SensorData.timestamp).all()
            #print(temp_sensor_co2)
            hardwareID = db.session.query(SensorData.hardwareID).filter(SensorData.address==session_addr).all()[0][0]
            print(hardwareID)
            #sensors = db.session.query(Hardware.sensors).filter(Hardware.hardwareID==hardwareID).first()
            #sensors = db.session.query(Hardware.sensors).filter(Hardware.hardwareID==hw_id).all()[0][0]
            if hardwareID:
                sensors = db.session.query(Hardware.sensors).filter(Hardware.hardwareID==hardwareID).all()[0][0]
                print(sensors)
            else:
                sensors = None

            #sensors=["Temperature", "Humidity"]
            #print(len(sensors))
            
            if sensors:
                for sensor in sensors:
                    data = {}
                    data["chart_id"] = "chart_{}".format(sensor)
                    data["chart_title"] = sensor
                    data["y_axis"] = "{} ({})".format(sensor, units[sensor])
                    data["legend"] = ""
                    data["series"] = []
                    if session_addr != "":
                        data["chart_title"] = "{} recorded during renting session".format(sensor) 
                        data["legend"] = "Session address {}".format(session_addr)
                        res = query_data_addr(sensor.lower(), session_addr)
                        if res != -1:
                            try:
                                data["series"].append(res[1])
                                data['labels'] = res[0]
                                chart_data.append(data)
                            except:
                                print("No data found for hardware and sensor.")                        
                        else:
                            print("No data found for request session address and sensor.")
                    else:
                        print("No data found for request session addres and sensor.")
            gps_track_data = []
            hardware_loc = db.session.query(SensorData.latitude, SensorData.longitude, SensorData.timestamp).filter(SensorData.address==session_addr).order_by(SensorData.timestamp.desc()).all()
            # hardware_loc = query_session_loc(session_addr)
            # if hardware_loc != -1:
            #     for index, loc in enumerate(hardware_loc):
            #         gps_track_data.append({
            #         "type": "Feature",
            #         "properties": {
            #             "lat": hardware_loc[1][0][index],
            #             "lon": hardware_loc[1][1][index],
            #             "timestamp" : datetime.strftime(hardware_loc[0][index], "%d.%m.%Y %H:%M:%S")
                        
            #         },
            #         "geometry": {
            #             "type": "Point",
            #             "coordinates": [hardware_loc[1][1][index], hardware_loc[1][0][index]]
            #         }
            #     })
            if hardware_loc:
                for loc in hardware_loc:
                    if loc[0] is not None and loc[1] is not None:
                        gps_track_data.append({
                            "type": "Feature",
                            "properties": {
                                "lat": loc[0],
                                "lon": loc[1],
                                "timestamp" : datetime.strftime(loc[2], "%d.%m.%Y %H:%M:%S")
                                
                            },
                            "geometry": {
                                "type": "Point",
                                "coordinates": [loc[1], loc[0]]
                            }
                        })
            print(gps_track_data)
            return render_template('index.html', geojson_data=geojson_data_arr, chart_data=chart_data, gps_track_data=gps_track_data)
        except:
            return render_template('index.html', geojson_data=geojson_data_arr)     
    else:
        return render_template('index.html', geojson_data=geojson_data_arr, title='Bikota User')



# @app.route('/privacy-policy.html')
# def privacy():
#     """Privacy page page."""
#     return render_template('/privacy-policy.html', title='Privacy Policy')

# @app.route('/terms-conditions.html')
# def terms_conditions():
#     """Terms and conditions page page."""
#     return render_template('/terms-conditions.html', title='Terms Conditions')

if __name__ == "__main__":
    app.run()