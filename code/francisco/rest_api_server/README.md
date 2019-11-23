# BIKOTA REST API Server


Restful API appliction to store and retrieve information from the BIKOTA hardware to the PostgreSQL database.

## Prerequisites

Ensure that you have met the following requirements:

* You have a `<Windows/Mac/Linux>` machine.
* You have Node.js installed in your machine. Otherwise, click [here](https://nodejs.org/en/) to download it.

## Installation

To install the REST API, follow these steps:

* Press the "Clone or download" button of this repository, and then click on "Download ZIP".
* Open the console from the folder where you download the REST API, and run the following commands:
	* Install the dependencies.
	`npm install`
	* To start the server.
	`run run start`

## Using the server

Once the server is up and running, you can start sending http request to the endpoints below.


**URL**

http://be.dev.iota.pw

**Endpoints**

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

**Status code**

Status Code | Message | Information
---------|----------|----------
200 | OK | Request success, data fetched successfully
201 | OK | Request success, data successfully inserted or updated into database
400 | Bad Request | Invalid JSON data in request body 
500 | Internal Server Error | Data successfully accepted but cannot be inserted into database 
999 | Hardware Defect | The bike/ hardware is defective

## Examples

* Using [Postman](https://www.getpostman.com/downloads/)

Testing the post method:

1. URL:
1.1 Select the "POST" method request
1.2 Paste the following URL: http://be.dev.iota.pw:5100/data
2. Header: 
2.1 Click on "Headers"
2.2 Insert the following fields in the Headers table:

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
* Using [Python](https://www.python.org/downloads/)

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
```
**Note**: Do not use json.dumps() in the POST and PUT request, otherwise the request will be received as a string instead of an object.

## Contact

If you want to contact me you can reach me at franciscosusana2292@gmail.com.
