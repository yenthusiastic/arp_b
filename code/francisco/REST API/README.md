BIKOTA REST API
----------

Restful API appliction to store and retrieve information from the BIKOTA hardware to the PostgreSQL database.

#### Version

V1.3

#### Pending

- [x] Develop Nodejs server.
- [x] Program to execute HTTP request.
- [x] Connecto to the remote PostgreSQL database.
- [x] Program to execute CRUD operations on the database.
- [x] Enable password hashing for user authentification.
- [ ] Update the 'address_index' and generate a new 'session_address'.
- [ ] Update 'latitude' and 'longitude' fields of the given 'hardware ID' in the 'HARDWARE_STATUS' table.
- [ ] Send response with status code.
- [ ] Add hardware authentication.
- [ ] Confirm HTTPS support.

#### URL

http://be.dev.iota.pw

#### Endpoints

* Hardware data

Method | Target | Body Parameters |Description
---------|----------|---------|---------
 GET | address/<Hardware_id> | N/A | Retrieve a new session address for the hardware
 POST | data | hardwareID,address,latitude,longitude,temperature,humidity,timestamp|Add new sensor data
 PUT | status | hardwareID,status,latitude,longitude |Update the hardware (bike)'s status

* Users data

Method | Target | Body Parameters| Description
---------|----------|---------|---------
 GET | no_production_users_view | N/A |Retrieve list of users registered
 POST | register | user, email, password |Add new user
 PUT | login | email, password |Verify user on the database

#### Status code

<Insert table here>

#### Examples

* Postman

Testing the post method:

1. URL:
1.1 Select the "POST" method request
1.2 Paste the following URL: http://be.dev.iota.pw:5100/data
2. Header: 
2.1 Click on "Headers"
2.2 Insert the following data in the Headers table:

Key | Value | Description
---------|----------|---------
 Content-Type | application/json | 
 3. Body: 
 3.1 Click on "Body"
 3.2 Click on "raw"
 3.3 Click on "JSON"
 3.4 Paste the following JSON code in the body:

```json
{
	"hardwareID":"1",
	"address":"Postman_test",
	"latitude":"61.123",
	"longitude":"7.933",
	"temperature":"19.2",
	"humidity":"35.7",
	"timestamp":"2019-10-13 02:19:05.749277+02"
}
```
* Python's request library

1. Import the libraries:

```
import requests as req
import json
```
2. Run the code below:

```
# Example POST request to Javascript-based backend
header = {"Content-Type": "application/json"}
resp = req.post("https://be.dev.iota.pw/data", json={
	"hardwareID":"1",
	"address":"Postman_test",
	"latitude":"61.123",
	"longitude":"7.933",
	"temperature":"19.2",
	"humidity":"35.7",
	"timestamp":"2019-10-15 13:37:05.749277+02"
},headers = header)
print(resp.text)
<<<<<<< HEAD
```
=======
```
>>>>>>> e3b7d755c44025a8d51749edf28e6f6917b6ae03
