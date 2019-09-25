###Python REST API endpoint for handling HTTP requests 
- API endpoint address: https://req.dev.iota.pw
- PUT request JSON body to update session address of hardware: 
```
{
    "hardwareID": 1; 
    "address": "ABC…999"; 
}
```
- POST request JSON body to insert sensor data of hardware to database:
```
{
    "hardwareID": 1; #Bike ID
    "data": [52.5157, 5.8992, 23.57, 40.5]
}
```
- API response status codes

Status Code | Message 
---------|----------
200 (OK) | Request success, data successfully inserted into database
400 (Bad Request)* | Invalid JSON data in request body 
500 (Internal Server Error) | Data successfully accepted but cannot be inserted into database 

- *Cases of requests that return 400 Response code:
    - any or both of the required keys are missing in the JSON data
    - any or both of the required keys contain empty data
    - sensor data does not contain 4 values

- See [PostgreSQL Server setup documentation](database_server.md) to set up database server and install related tools. Upon success, API server can be run using:
```bash
cd ../code/thu/
python api_server.py
```
- To send requests to API endpoint, use the [api_client IPython Notebook](../code/thu/api_client.ipynb).