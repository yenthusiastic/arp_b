### 1. API
The API should accept **GET**, **POST** and **PUT** requests from the custom hardware module on the bike (ESP-based). The data corresponding to the requests will either be retrieved from or inserted into the database. No DELETE request is needed as the hardware should not be able to delete any entry in the database.

#### 1.1. Endpoint architecture
The API should have the following endpoints:
- **GET** - `api/address` - Retrieve a new session address for the hardware
- **POST** - `api/data` - Add new sensor data
- **PUT** - `api/status` - Update the hardware (bike)'s status

#### 1.2. Request Format
- The JSON data in the **POST** request body should have the following format:
```json
{
    "hardwareID": 1,
    "address": "ABC…999",
    "data": [52.5157, 5.8992, 23.57, 40.5]
}
```
where `hardwareID` and `data` are **compulsory fields**, `address` is optional field. 

Note:
    - The `address` is not always required and will be saved as **empty string** in the database when the bike is parked. 
    - The `data` field contains 4 values (for now) in the following order: latitude, longitude, temperature, humidity.

- The JSON data in the **PUT** request body should have the following format:
```json
{
    "hardwareID": 1, 
    "status": "parked",
    "location": [52.5157, 5.8992]
}
```
where `hardwareID` and **at least 1** of the remaining 2 fields are **compulsory**. `status` should be **only** one of the following states: "parked", "rented", "stolen". The location format is `[latitude, longitude]`. 

#### 1.3. Response code
- The API endpoints should return one of the following response status codes in the header

Status Code | Message | Information
---------|----------|----------
200 | OK | Request success, data successfully inserted into database
400* | Bad Request | Invalid JSON data in request body 
500 | Internal Server Error | Data successfully accepted but cannot be inserted into database 
999 | Hardware Defect | The bike/ hardware is defective


- *Example cases of requests that return 400 Response code:
    - any or all of the required fields are missing in the JSON data
    - any or all of the required keys contain empty data
    - sensor data (POST request) does not contain 4 values
    - location data (PUT request) does not contain 2 values
    - etc.

#### 1.4. Response JSON format
- The API endpoints should return a status code in the header and a JSON in the body corresponding to the header status code as follows:
```json
{
    "HttpStatusCode": 200, 
    "HttpMessage": "OK", 
    "MoreInformation": "Success.",
    "SessionAddress": "ABC...999"
}
```
where the `SessionAddress` field is **only** required when a **GET** request to endpoint `api/address` is made.

### 2. Database

#### 2.1. Structure
The graphical view of the Tables (Schemas) in the database is as follows:

<img src = "../media/db_new.png" width="720px">

Upon created, the `HARDWARE_STATUS` table is manually inserted with the initital `session_address` (`address_index` = 0) for each `hardwareID`. Similarly, manual insertion is required for new hardware modules. This is intended to be done through the administration dashboard at later phase of the project. For now, this is done through PgAdmin.
#### 2.2. Access
- The database is currently implemented using a Postgres server and can be accessed through the PgAdmin web interface at https://pg.dev.iota.hub with following credentials:
    - Email address: arpb@iota.dev
    - Password: iota999

- To connect to the database server from PgAdmin or a Python/Javascript program, use the following details:
```shell
DB Host: 'db.dev.iota.pw'
DB Port: 6000
Database name: 'arp_b'
User: 'arp_b'
Password: 'iota999'
```
With SQLAlchemy library, set `SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://arp_b:iota999@db.dev.iota.pw:6000/arpb"`

### 3. Server functions
- Check validity of all **REST** requests, especially the format of the sent JSON data as defined in Section 1.2
- Everytime a valid **PUT** request is received, update the `status` and/or `latitude` and `longitude` fields of given `hardwareID` in the `HARDWARE_STATUS` table with received data
    - example query to update data in PostgreSQL: `UPDATE "HARDWARE_STATUS" SET "status" = 'parked', latitude = 55.990, longitude = 6.001 WHERE "hardwareID" = 1`
- Everytime a valid **GET** request is received (as the bike status changes from "rented" to "parked"), for the given `hardwareID`, 
    - query the value of current `address_index` in the `HARDWARE_STATUS` table, increment it by 1 and update its value in the table
    - generate a new `session_address` based on the new `address_index` using the IOTA library and update its value in the `HARDWARE_STATUS` table
    - return the new `session_address` in the API response body
- Everytime a valid **POST** request is received
    - insert all received data together with an auto generated timestamp in the `SENSOR_DATA` table
        - example query to insert data with automatic timestamp in PostgreSQL: `INSERT into "SENSOR_DATA" values (default, 1, 'ABC...999', 52.5157, 5.8992, 23.57, 40.5, current_timestamp)`
    - update the `latitude` and `longitude` fields of given `hardwareID` in the `HARDWARE_STATUS` table with received data
    - send the sensor data as a JSON object to the Tangle using IOTA library as a non-value transaction to the address provided in the POST request. If no address is provided or the address field is empty (the bike is in `parked` state), retrieve the address of the corresponding `hardwareID` from the `HARDWARE_STATUS` table. Format of the JSON object (for now):
```json
{
    "latitude": 61.123,
    "longitude": 7.933,
    "temperature": 19.2,
    "humidity": 35.7
}
```

