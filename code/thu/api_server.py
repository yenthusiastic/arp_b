from http.server import BaseHTTPRequestHandler, HTTPServer 
import json
import requests as req  #pip install requests
import urllib3
# use following steps to install psycopg2
# sudo apt-get install libpq-dev
# git clone https://github.com/psycopg/psycopg2
# python setup.py build
# sudo python setup.py install
import psycopg2 
import sys
from IotaHandler import IotaHandler

ADDR = "0.0.0.0" #0.0.0.0 for public
PORT = 5000

db_host='db.dev.iota.pw'
db_port=6000
database='arp_b'
user='arp_b'
password='iota999'

DEBUG = True
SENSOR_COUNT = 4

ADDR = "0.0.0.0" #0.0.0.0 for public
PORT = 5000

db_host='db.dev.iota.pw'
db_port=6000
database='arp_b'
user='arp_b'
password='iota999'

DEBUG = True
SENSOR_COUNT = 4

class ReqHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status_code):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
    def _set_response(self, status_code, msg, info):
        self._set_headers(status_code)
        json_str = json.dumps({"HttpStatusCode": status_code, "HttpMessage": msg, "MoreInformation": info})
        self.wfile.write(json_str.encode(encoding='utf_8'))

    def do_GET(self):
        self._set_headers(200)
        self.wfile.write(b'<html><body><h1>Welcome to req.dev.iota.pw</h1></body></html>')
        print(">>>Request: \n{0}".format(self.requestline))
        print(">>>Headers: \n{0}".format(self.headers))
        
    def do_POST(self):
        datalen = int(self.headers['Content-Length'])
        data = self.rfile.read(datalen)
        req_json = json.loads(json.loads(data))
        
        if DEBUG:
            print(">>>Request: \n{0}".format(self.requestline))
            print(">>>Headers: \n{0}".format(self.headers))
            print(">>>JSON: \n{0}\n".format(req_json)) 
            print("JSON length", len(req_json))
        if len(req_json) != 2:
            self._set_response(400, 'Bad Request', 'Invalid JSON data. Dict of 2 is required')
        else:
            try:
                hw_id = req_json["hardwareID"]
                s_data = req_json["data"]
                if hw_id is not None and s_data is not None:     
                    if (len(s_data) != SENSOR_COUNT):
                        info = 'Invalid JSON data. Sensor data should contain exactly {} values.'.format(SENSOR_COUNT)
                        self._set_response(400, "Bad Request", info)
                    else:
                        data_str = ""
                        data_arr = []
                        for val in s_data:
                            data_str+= str(val) + ","
                            data_arr.append(val)
                        data_str = data_str[:-1]
                        print(data_str)
                        ret_msg = self.insert_data(hw_id, data_str)
                        print("returned message: {}".format(ret_msg))
                        if ret_msg[0] == 0:
                            self._set_response(200, "OK", 'Success')
                            json_data = {"latitude": data_arr[0], "longitude": data_arr[1], "temperature": data_arr[2], "humidity": data_arr[3]}
                            i_handler = IotaHandler()
                            i_handler.data_to_tangle(ret_msg[1], json.dumps(json_data))
                        else:
                            self._set_response(500, "Internal Server Error", 'Error inserting values to database')
                else:
                    self._set_response(400, "Bad Request", 'Invalid JSON data. One or more empty data fields provided')
            except KeyError as e:
                self._set_response(400, "Bad Request", 'Invalid JSON data. "hardwareID" and "data" are required keys')
            
        
    def do_PUT(self):
        datalen = int(self.headers['Content-Length'])
        data = self.rfile.read(datalen)
        req_json = json.loads(json.loads(data))
        
        if DEBUG:
            print(">>>Request: \n{0}".format(self.requestline))
            print(">>>Headers: \n{0}".format(self.headers))
            print(">>>JSON: \n{0}\n".format(req_json))
            print("JSON length", len(req_json))
        if len(req_json) != 2:
            self._set_response(400, "Bad Request", 'Invalid JSON data. Dict of 2 is required')
        else:
            try:
                hw_id = req_json["hardwareID"]
                address = req_json["address"]
                if hw_id is not None and address is not None:     
                    err_code = self.update_address(hw_id, address)
                    if err_code == 0:
                        self._set_response(200, "OK", 'Success.')
                    else:
                        self._set_response(500, "Internal Server Error", 'Error inserting values to database')
                else:
                    self._set_response(400, "Bad Request", 'Invalid JSON data. One or more empty data fields provided')
            except KeyError as e:
                self._set_response(400, "Bad Request", 'Invalid JSON data. "hardwareID" and "address" are required keys')

    def connect(self, msg, resp=False):
        global conn
        print("""Executing SQL query on Database server...""")
        try:
            cur = conn.cursor()
            cur.execute(msg)
            conn.commit()
            if resp:
                # get response from DB
                res = cur.fetchone()
                return res
            print('Success. Database connection closed.')
            return 0
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while executing SQL query: {}".format(msg))
            print(error)
            return -1
            
    def insert_data(self, hw_id, data_str):
        ses_address = self.connect("""SELECT "session_address" FROM public."HARDWARE" WHERE "hardwareID" = {0} """.format(hw_id), resp=True)[0]
        sql_query = """INSERT INTO public."SENSOR_DATA" values (DEFAULT, '{0}', {1}, current_timestamp) """.format(ses_address, data_str)
        if DEBUG:
            print(ses_address)
            print(sql_query)        
        return self.connect(sql_query), ses_address
            
            
    def update_address(self, hw_id, ses_address):
        res = self.connect("""SELECT * FROM public."HARDWARE" WHERE "hardwareID" = {0} """.format(hw_id), resp=True)
        sql_query = ""
        if res is not None:
            sql_query = """UPDATE public."HARDWARE" SET "session_address" = '{1}' where "hardwareID" = {0} """.format(hw_id, ses_address)
            if DEBUG:
                print(res)
                print(sql_query)
        else:
            sql_query = """INSERT INTO public."HARDWARE" values ({0}, '{1}') """.format(hw_id, ses_address)
            if DEBUG:
                print(sql_query)
        return self.connect(sql_query)
        
        
def connect_DB():
    try:        
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(host=db_host, port=db_port, user=user, password=password, database=database)
        print("Successfully connected to DB")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit()
    return conn

conn = connect_DB()
try:
    server = HTTPServer((ADDR, PORT), ReqHandler)
    print("serving at port", PORT)
    server.serve_forever()
    #server.handle_request()
    server.socket.close()
except Exception as e:
    print('Server shutdown...', e)
    server.shutdown()
finally:
    pass