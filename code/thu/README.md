### Notes
#### Create a virtual environment in Python
In Terminal/ Command Prompt, type in:
```
python -m venv <name-of-env>
```
To activate the environment:
```
cd <dir-of-env>
source name-of-env/bin/activate
```
To deactivate:
```
deactivate
```

#### Create a virtual environment in Anaconda
In Anaconda Prompt, type in: 
```
conda create --name <name-of-env>
```
To activate the environment:
```
conda activate <name-of-env>
```
To deactivate:
```
conda deactivate
```

#### Organize and execute Flask application 
- In Flask, all `HTML` pages have to be stored under a folder named `templates`. This folder is usually placed directly under the app root folder where the main program e.g. `app.py` or `run.py` are.  
- All styling sheets, e.g. `CSS` and all `JS` scripts have to be stored under (directly under or in other sub-folders of) a folder named `static`. The `static` folder is directly under the app root folder. 
- Routing of the pages are configured in a Python script, usually named `views.py` and saved in the app root folder. 
- In summary, the project structure can look like follows:
```
.                           
+-- static/
|    +-- styles.css
|    +-- script.js
+-- templates/
|    +-- index.html
+-- app.py
+-- views.py
```
- To deploy the app on a specific port, say port 5001, in the app root folder run the command:
```
flask run -p <custom-port-number>
```

When no port number is given explicitly, the default port number 5000 will be used to host the website content. 
For local machine, access the web server at `127.0.0.1:<custom-port-number>`.

#### Access web server
- The Flask server for User Interface will be running on port 5021 and accessible at bikota.dev.iota.pw
- The Flask server for Admin Panel will be running on port 5020 and accessible at web.dev.iota.pw


### Plans/ TODOs
#### API Endpoints (deactivated)
For communication with bike hardware module
- [x] Simple API endpoint for handling GET/PUT/POST requests at https://req.dev.iota.pw. Check [Python API documentation for details](../../documentation/API_python.md).
- [x] Define JSON data structure for API request body
- [x] Send transaction with sensor data to Tangle through connection with IOTA node
- [ ] Advanced API with multiple endpoints using additional frameworks and authentication

#### Postgres database
    - [x] Define database schemas and structure
    - [x] Run Postgres and PgAdmin servers from Docker images. Check [Database Server documentation for details](../../documentation/database_server.md).

#### Sensor data aggregation policy
Currently sensor data is being saved into the database every second, which means a lot of data points will be fetched when a large time interval is requested in the SQL query. This reults in poor performance while generating the sensor charts on the Admin Panel Dashboard. To prevent this, the SQL query should fetch aggregated data instead of all raw data points. The extent of aggregation can vary depending on the total amount of data points recorded within the requested time range. 

#### Web Application
- Database connection
    - Use Flask SQLAlchemy ORM model to represent databases as objects and quickly insert/ update/ delete small number of entries. Can be used for:
        - Creating, updating and deleting user accounts or hardware modules
    - Use the **psycopg2** package for raw SQL executions for more heavy-loaded data. Can be used for:
        - Querying current location and/or status of all hardwares
        - Quering large amount of sensor data 
        - Filtering data by user's selections
- Administration dashboard: 
    - [X] User authentication
        - [X] Login 
        - [X] Registration
        - [X] Logout
    - [X] User profile management
        - [X] Show user profile
        - [X] Update profile
        - [X] Update password 
        - [X] Delete account with confirmation dialog
    - [ ] Bike visualization (Main dashboard)
        - [ ] Visualize all bikes as markers on a map with details including
            - Hardware ID
            - Attached sensor(s)
            - Current address
            - Current status
            - Current location 
        - [ ] Filter map by 
            - [ ] Status
            - [ ] Location & radius
    - [X] Hardware management
        - [X] Create new hardware with required details
            - Hardware ID
            - Attached sensor(s)
            - Address
            - Status
            - Place/ City of location
        - [X] Update hardware details
        - [X] Delete hardware with confirmation dialog
    - [X] Visualize sensor data of hardware(s) as charts, filter by
        - [X] Hardware ID
        - [X] Sensor type
        - [X] Session address
        - [X] Time range
    - [ ] Visualize aggregated instead of raw sensor data when the queried time period returns too many data points (checked Sensor data aggregation policy section for details)
    - [ ] Constant refresh rate of 5 seconds



