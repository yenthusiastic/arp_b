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
SENSOR_DATA_KEYS = ["latitude", "longitude", "temperature", "humidity"]
HARDWARE_STATUS_TABLE = "HARDWARE_STATUS"
SENSOR_DATA_TABLE = "SENSOR_DATA"

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
        addr = None
        
        if DEBUG:
            print(">>>Request: \n{0}".format(self.requestline))
            print(">>>Headers: \n{0}".format(self.headers))
            print(">>>JSON: \n{0}\n".format(req_json)) 
            print("JSON length", len(req_json))
        if len(req_json) < 2:
            self._set_response(400, 'Bad Request', 'Invalid JSON data. Minimum 2 data fields required')
        else:
            try:
                hw_id = req_json["hardwareID"]
                s_data = req_json["data"]
                if len(req_json) == 3:
                    addr = req_json["address"]
                else:
                    print('Address field not provided')
                if hw_id is not None and s_data is not None: 
                    data_str = ""
                    data_arr = []
                    for val in s_data:
                        data_str+= str(val) + ", "
                        data_arr.append(val)
                    if len(data_arr) < len(SENSOR_DATA_KEYS):
                        while len(data_arr) < len(SENSOR_DATA_KEYS):
                            data_str += "null, "
                            data_arr.append(None);
                    data_str = data_str[:-2]
                    print(data_str)
                    ret_msg = self.insert_data(hw_id, addr, data_str)
                    print("returned message: {}".format(ret_msg))
                    if ret_msg[0] == 0:
                        json_data = {}
                        try:
                            for count, data_header in enumerate(SENSOR_DATA_KEYS):
                                json_data[data_header] = data_arr[count]
                            self._set_response(200, "OK", 'Success')
                        except Exception as e:
                            self._set_response(200, "OK", 'One or more sensor values missing in JSON data')
                        print(json.dumps(json_data))
                        i_handler = IotaHandler()
                        i_handler.data_to_tangle(ret_msg[1], json.dumps(json_data))
                    else:
                        self._set_response(500, "Internal Server Error", 'Error inserting values to database')
                else:
                    self._set_response(400, "Bad Request", 'Invalid JSON data. One or more empty data fields provided')
            except KeyError as e:
                self._set_response(400, "Bad Request", "Invalid JSON data. 'hardwareID' and 'data' are required keys")
            
        
    def do_PUT(self):
        datalen = int(self.headers['Content-Length'])
        data = self.rfile.read(datalen)
        req_json = json.loads(json.loads(data))
        status = None
        location = None
        key_len = 0
        
        if DEBUG:
            print(">>>Request: \n{0}".format(self.requestline))
            print(">>>Headers: \n{0}".format(self.headers))
            print(">>>JSON: \n{0}\n".format(req_json))
            print("JSON length", len(req_json))
        if len(req_json) < 2:
            self._set_response(400, "Bad Request", 'Invalid JSON data. Minimum 2 data fields required')
        else:
            try:
                hw_id = req_json["hardwareID"]
                key_len+=1
            except KeyError as e:
                self._set_response(400, "Bad Request", "Invalid JSON data. 'hardwareID' is required key")
                return -1
            try:
                status = req_json["status"]
                key_len+=1
            except KeyError as e:
                print('Status field not provided')
                pass
            try:
                location = req_json["location"]
                key_len+=1
            except KeyError as e:
                print('Location field not provided')
                pass
            if key_len > 1:    
                err_code = self.update_status(hw_id, status, location)
                if err_code == 0:
                    self._set_response(200, "OK", 'Success.')
                else:
                    self._set_response(500, "Internal Server Error", 'Error inserting values to database')
            else:
                self._set_response(400, "Bad Request", 'Invalid JSON data. One or more required data fields are empty')
           

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
            
    def insert_data(self, hw_id, addr, data_str):
        ses_addr = addr
        if ses_addr is not None:
            sql_query = """INSERT INTO public."{0}" values (DEFAULT, {1}, '{2}', {3}, current_timestamp) """.format(SENSOR_DATA_TABLE, hw_id, ses_addr, data_str)
        else:
            sql_query = """INSERT INTO public."{0}" values (DEFAULT, {1}, '', {2}, current_timestamp) """.format(SENSOR_DATA_TABLE, hw_id, data_str)
            ses_addr = self.connect("""SELECT "session_address" FROM public."{0}" WHERE "hardwareID" = {1} """.format(HARDWARE_STATUS_TABLE, hw_id), resp=True)[0]
        if DEBUG:
            print(ses_addr)
            print(sql_query)  
        #sql_query = 'SELECT * FROM "SENSOR_DATA"' 
        return self.connect(sql_query), ses_addr
            
            
    def update_status(self, hw_id, hw_status, location):
        res = self.connect("""SELECT * FROM public."{0}" WHERE "hardwareID" = {1} """.format(HARDWARE_STATUS_TABLE, hw_id), resp=True)
        sql_query = ""
        if res is not None:
            if location is not None:
                if hw_status is not None:
                    sql_query = """UPDATE public."{0}" SET "status" = '{2}', "latitude" = {3}, "longitude" = {4} where "hardwareID" = {1} """.format(HARDWARE_STATUS_TABLE, hw_id, hw_status, location[0], location[1])
                else:
                    sql_query = """UPDATE public."{0}" SET "latitude" = {2}, "longitude" = {3} where "hardwareID" = {1} """.format(HARDWARE_STATUS_TABLE, hw_id, location[0], location[1])
            elif hw_status is not None and location is None:
                sql_query = """UPDATE public."{0}" SET "status" = '{2}' where "hardwareID" = {1} """.format(HARDWARE_STATUS_TABLE, hw_id, hw_status)
            if DEBUG:
                print(res)
                print(sql_query)
        else:
            sql_query = """INSERT INTO public."{0}" values ({1}, '{2}', '{3}', '{4}') """.format(HARDWARE_STATUS_TABLE, hw_id, hw_status, location[0], location[1])
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