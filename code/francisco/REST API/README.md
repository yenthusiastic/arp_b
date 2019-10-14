Summary
----------

V1.1 

GET - api/address - Retrieve a new session address for the hardware
POST - api/data - Add new sensor data
PUT - api/status - Update the hardware (bike)'s status

#### 1. GET

Test the get method by sending a htttp GET request to:

http://be.dev.iota.pw:5100/address/1

**Still pending to update the 'address_index' and generate a new 'session_address'.**

#### 2. POST

Test the post method by sending a http POST request to:

http://be.dev.iota.pw:5100/data

With the following data in JSON format:
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
**Still pending to update 'latitude' and 'longitude' fields of the given 'hardware ID' in the 'HARDWARE_STATUS' table.**

#### 3. PUT

Test the post method by sending a http PUT request to:

http://be.dev.iota.pw:5100/status

With the following data in JSON format:
```json
{
	"status":"rented",
	"latitude":"61.123",
	"longitude":"7.933",
	"hardwareID":"1"
}
```
