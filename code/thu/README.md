### Plans/ TODOs
#### API Endpoints 
For communication with bike hardware module
- [x] Simple API endpoint for handling GET/PUT/POST requests at https://req.dev.iota.pw. Check [Python API documentation for details](../../documentation/API_python.md).
- [x] Define JSON data structure for API request body
- [x] Send transaction with sensor data to Tangle through connection with IOTA node
- [ ] Advanced API with multiple endpoints using additional frameworks and authentication
- Postgres database
    - [x] Define database schemas and structure
    - [x] Run Postgres and PgAdmin servers from Docker images. Check [Database Server documentation for details](../../documentation/database_server.md).

#### Web Application
- Database connection
    - Use Flask SQLAlchemy ORM model to represent databases as objects and quickly insert/ update/ delete small number of entries. Can be used for:
        - Creating, updating and deleting user accounts or hardware modules
    - Use the **psycopg2** package for raw SQL executions for more heavy-loaded data. Can be used for:
        - Querying current location and/or status of all hardwares
        - Quering large amount of sensor data 
        - Filtering data by user's selections

- User interface: 
    - [ ] Visualize **parked** bikes available for rent as markers on a map
    - [ ] Filter map by location and radius
    - [ ] Click on bike to get exact location
    - [ ] Input form for entering IOTA address
    - [ ] Show data collected in the session on a chart
    - [ ] Bikota renting service manual
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
    - [ ] Hardware management
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



