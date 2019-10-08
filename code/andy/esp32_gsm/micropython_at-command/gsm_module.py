# Driver for SIM800L module (using AT commands)
# MIT License; Copyright (c) 2017 Jeffrey N. Magee
node_url = "https://nodes.thetangle.org/"
command = '{"addresses": ["SVJQSVYGFUYZHKSQD9OYGSEMCSAWKNXEXMGJSUKQHHDYPDDOTVXYCHFWEAOCZUVOQFANVVLIDAPOTIDY9"], "threshold": 100, "command": "getBalances"}'
headers = {'content-type': 'application/json','X-IOTA-API-Version': '1'}

from machine import UART, Pin
from time import sleep_ms
import urequests as requests
import math
import json

# kludge required because "ignore" parameter to decode not implemented
def convert_to_string(buf):
    try:
        tt =  buf.decode('utf-8').strip()
        return tt
    except UnicodeError:
        print("convert_to_string:", buf)
        tmp = bytearray(buf)
        for i in range(len(tmp)):
            if tmp[i]>127:
                tmp[i] = ord('#')
        return bytes(tmp).decode('utf-8').strip()

class SIM800LError(Exception):
    pass

def check_result(errmsg,expected,res):
    if not res:
        res = 'None'
    #print(errmsg+res)
    if not expected == res and not res == 'None':
        raise SIM800LError('SIM800L Error {}\nExpected: {}\n Result. {}'.format(errmsg, expected, res))


class SIM800L:

    def __init__(self,uart_object, gsm_apn, req_server_url, debug=False):  # pos =1 or 2 depending on skin position
        self._uart = uart_object
        self.apn = gsm_apn
        self.req_server = req_server_url
        self.debug = debug
        #self._uart = pyb.UART(uartno, 9600, read_buf_len=2048)
        self.incoming_action = None
        self.no_carrier_action = None
        self.clip_action = None
        self._clip = None
        self.msg_action = None
        self._msgid = 0
        self.savbuf = None
        self.credit = ''
        self.credit_action = None
        
    def read(self, num=None):
        return self._uart.read(num)
        
        
    def isReady(self):
        return self.command('ATZ')
    
    
    def status(self):
        return self.command('AT+cipstatus', 3)


    def setup(self):
        #self.command('ATE0\n')         # command echo off
        self.command('AT+CMGF=1\n')    # plain text SMS
        self.command('AT+CLTS=1\n')    # enabke get local timestamp mode
        self.command('AT+CSCLK=0\n')   # disable automatic sleep
        
    def network_status(self):
        return self.command('at+cgatt?')
    
    def wakechars(self):
        self._uart.write('AT\n')        # will be ignored
        sleep_ms(100)
    
    def sleep(self,n):
        self.command('AT+CSCLK={}\n'.format(n))

    def call(self,numstr):
        self.command('ATD{};\n'.format(numstr))
        
    def hangup(self):
        self.command('ATH\n')     
  
    def signal_strength(self):
        result = self.command('AT+CSQ\n',3)
        if result:
            params=result.split(',')
            if not params[0] == '':
                params2 = params[0].split(':')
                if params2[0]=='+CSQ':
                    x = int(params2[1])
                    if not x == 99:
                        return(math.floor(x/6+0.5))
        return 0
        
    def network_name(self):   
        result = self.command('AT+COPS?\n',3)
        if result:
            params=result.split(',')
            if not params[0] == '':
                params2 = params[0].split(':')
                if params2[0]=='+COPS':
                    if len(params)>2:
                        names = params[2].split('"')
                        if len(names)>1:
                            return names[1]
        return ''


    def send_sms(self,destno,msgtext):
        result = self.command('AT+CMGS="{}"\n'.format(destno),99,5000,msgtext+'\x1A')
        if result and result=='>' and self.savbuf:
            params = self.savbuf.split(':')
            if params[0]=='+CUSD' or params[0] == '+CMGS':
                return 'OK'
        return 'ERROR'
    
                     
    def date_time(self):
        result = self.command('AT+CCLK?\n',3)
        if result:
            if result[0:5] == "+CCLK":
                return result.split('"')[1]
        return ''
        

    def cmd(self, command):
        self._uart.write(command + '\n')
        while self._uart.any() > 0:
            print(self._uart.readline())
        
        
    def command(self, cmdstr, lines=1, waitfor=1000, msgtext=None):
        #flush input
        #print(cmdstr)
        try:
            while self._uart.any():
                if self.debug: 
                    print("uart_any",self._uart.any())
                    print(self._uart.read(),'\n')
            print('write:',self._uart.write(cmdstr + '\n'),cmdstr)
            if msgtext:
                self._uart.write(msgtext + '\n')
            if waitfor > 0:
                if self._uart.any() == 0:
                    for i in range(waitfor/10):
                        sleep_ms(10)
                        if self._uart.any() > 0:
                            break
            buf=self._uart.readline() #discard linefeed etc
            if self.debug:
                print(1,buf)
            if self._uart.any() == 0:
                for i in range(waitfor/10):
                    sleep_ms(10)
                    if self._uart.any() > 0:
                        break
            buf=self._uart.readline()
            if self.debug:
                print(2,buf)
            result = convert_to_string(buf)
            if not buf:
                return None
            if lines>1:
                self.savbuf = ''
                for i in range(lines-1):
                    if self._uart.any() == 0:
                        for i in range(waitfor/10):
                            sleep_ms(10)
                            if self._uart.any() > 0:
                                i=30
                                print("i",i)
                                break
                    buf=self._uart.readline()
                    if not buf:
                        return result
                    buf = convert_to_string(buf)
                    if self.debug:
                        print("buf:", buf)
                    if not buf == '' and not buf == 'OK':
                        self.savbuf += buf+'\n'
                print("savbuf",self.savbuf)
                return self.savbuf
            return result
        except Exception as e:
            print("command| Exception: {}".format(e))

    
      
    
    def get_location(self):
        return self.command('at+cipgsmloc=1,1',4)
    
    

    def connectGSM(self):
        self.command('AT+CSTT="' + self.apn + '"', waitfor=3000)
        self.command("AT+CIICR", waitfor=5000)
        self.command("AT+CIFSR", waitfor=3000)
        return self._uart.read(self._uart.any())

    def connect_gsm(self, apn=None):
        if self.status != 'OK':
            print("Waiting for module to be ready...")
            for i in range(20):
                sleep_ms(100)
                if self.status == 'OK':
                    break
        if apn == None:
            apn = self.apn
        res = self.command('AT+SAPBR=3,1,"Contype","GPRS"\n')
        check_result("SAPBR 1: ",'OK',res)
        res = self.command('AT+SAPBR=3,1,"APN","{}"\n'.format(apn))
        check_result("SAPBR 2: ",'OK',res)
        res = self.command('AT+SAPBR=1,1\n',2,3000)
        return check_result("SAPBR 3: ",'OK',res)
    
    def disconnect_gsm(self):
        return self.command('AT+SAPBR=0,1\n',2) # close Bearer context

    
    def connect_gsm2(self):
        self.command('at+cipshut',3)
        self.command('at+cipmux=0',3)
        self.command('at+cgatt=1',3)
        self.command('AT+CGDCONT=1,"IP","web.vodafone.de"',3)
        self.command('at+cstt="web.vodafone.de","",""',3)
        self.command('AT+CIICR',3)
        self.command('AT+CIFSR',3)
    
    def disconnect_gsm2(self):
        self.command('AT+CIPSHUT',3)
    
    
    def http2(self, url=None):
        if url==None:
            url='"req.dev.iota.pw","5000"'
        self.command('at+CIPSTART="TCP",'+url, 3)
        self.command('AT+CIPSEND',3)
        _header='''GET / HTTP/1.1\r\nHost: req.dev.iota.pw\r\nContent-Type: application/json\r\nContent-Length:148\r\nX-IOTA-API-Version': '1'\r\n\n'''        
        self.command(_header + json.dumps(command) + '\r\n' + chr(26),5)
        #self.command('AT+CIPCLOSE',3,3000)
    
    # http get command using gprs
    def http_get(self,url=None):
        # r.text.split(',')[0].split(':')[1][3:-2]
        if url == None:
            url = self.req_server
        resp = None
        nbytes = 0
        rstate = 0
        is_ssl = 0
        proto, dummy, surl = url.split("/", 2)
        if proto == "http:":
            is_ssl = 0
        elif proto == "https:":
            is_ssl = 1
        else:
            raise ValueError("Unsupported protocol: " + proto)
        try:
            res = self.command('AT+HTTPINIT\n',1)
            check_result("HTTPINIT: ",'OK',res)
            res = self.command('AT+HTTPPARA="CID",1\n')
            check_result("HTTPPARA 1: ",'OK',res)
            res = self.command('AT+HTTPPARA="URL","{}"\n'.format(surl))
            check_result("HTTPPARA 2: ",'OK',res)
            res = self.command('AT+HTTPSSL={}\n'.format(is_ssl))
            check_result("HTTPSSL: ",'OK',res)
            res = self.command('AT+HTTPACTION=0\n', waitfor=6000)
            check_result("HTTPACTION: ",'OK',res)
            for i in range(50):  #limit wait to max 20 x readline timeout
                buf = self._uart.readline()
                if buf and not buf==b'\r\n':
                    buf = convert_to_string(buf)
                    #print(buf)
                    prefix,retcode,bytes = buf.split(',')
                    rstate = int(retcode)
                    nbytes = int(bytes)
                    break
                sleep_ms(100)
            res = self.command('AT+HTTPREAD\n',1, waitfor=3000)
            if self.debug:
                print("response", res)
            buf = self._uart.read(nbytes)
            if self.debug:
                print("nbytes",nbytes)
            check_result("HTTPACTION: ",'+HTTPREAD: {}'.format(nbytes),res)
            if buf[-4:] == b'OK\r\n':  # remove final OK if it was read
                buf = buf[:-4]
            resp = Response(buf)
        except SIM800LError as err:
            print(str(err))
        self.command('AT+HTTPTERM\n',1) # terminate HTTP task
        return resp


    # http get command using gprs
    def http_get_iota(self,url=None):
        # r.text.split(',')[0].split(':')[1][3:-2]
        if url == None:
            url = self.req_server
        resp = None
        nbytes = 0
        rstate = 0
        is_ssl = 0
        proto, dummy, surl = url.split("/", 2)
        if proto == "http:":
            is_ssl = 0
        elif proto == "https:":
            is_ssl = 1
        else:
            raise ValueError("Unsupported protocol: " + proto)
        try:
            res = self.command('AT+HTTPINIT\n',1)
            check_result("HTTPINIT: ",'OK',res)
            res = self.command('AT+HTTPPARA="CID",1\n')
            check_result("HTTPPARA 1: ",'OK',res)
            res = self.command('AT+HTTPPARA="URL","{}"\n'.format(surl))            
            check_result("HTTPPARA 2: ",'OK',res)
            res = self.command('AT+HTTPSSL={}\n'.format(is_ssl))
            check_result("HTTPSSL: ",'OK',res)
            _header='''GET / HTTP/1.1\nHost: req.dev.iota.pw\nContent-Type: application/json\nContent-Length:192\nX-IOTA-API-Version': '1'\n\n'''        
            #_header='''Content-Length:148\r\nX-IOTA-API-Version': '1'\r\n\n'''        
            #self.command('AT+HTTPPARA="TIMEOUT","{}"\n'.format(30),3)
            #self.command('AT+HTTPPARA="CONTENT","{}"\n'.format("application/json"),3)
            self.command('AT+HTTPDATA=263,1000',3)
            self.command(_header + command,5,5000)
            
            res = self.command('AT+HTTPACTION=0\n',3, waitfor=10000)
            #check_result("HTTPACTION: ",'OK',res)
            for i in range(50):  #limit wait to max 20 x readline timeout
                buf = self._uart.readline()
                if buf and not buf==b'\r\n':
                    buf = convert_to_string(buf)
                    #print(buf)
                    prefix,retcode,bytes = buf.split(',')
                    rstate = int(retcode)
                    nbytes = int(bytes)
                    break
                sleep_ms(100)
            res = self.command('AT+HTTPREAD\n',1, waitfor=3000)
            if self.debug:
                print("response", res)
            buf = self._uart.read(nbytes)
            if self.debug:
                print("nbytes",nbytes)
            check_result("HTTPACTION: ",'+HTTPREAD: {}'.format(nbytes),res)
            if buf[-4:] == b'OK\r\n':  # remove final OK if it was read
                buf = buf[:-4]
            resp = Response(buf)
        except SIM800LError as err:
            print(str(err))
        self.command('AT+HTTPTERM\n',1) # terminate HTTP task
        return resp

    def send_request(self, url="https://req.dev.iota.pw/"):
        try:
            req_status = None
            print("sending request...")
            json_data = [{"hardwareID": 1}, {"vbat": 3850}]
            #req = requests.get(url)
            req = requests.post(url, json=json_data)
            req_status = [req.status_code, req.reason]
            if req_status is not None:
                pass
            else:
                return False
            print(req_status)
        except Exception as e:
            print("Exception at request: ", e)


    def test(self):
        #r = self.http_get('http://dev.iota.pw/')
        r = self.http_get('http://exploreembedded.com/wiki/images/1/15/Hello.txt')
        print(r.text)


    
 
 
class Response:
    
    def __init__(self, buf, status = 200):
        self.encoding = "utf-8"
        self._cached = buf
        self.status = status
    
    def close(self):
        self._cached = None
    
    @property
    def content(self):
        return self._cached
    
    @property
    def text(self):
        return str(self.content, self.encoding)
    
    def json(self):
        import ujson
        return ujson.loads(self.content)

