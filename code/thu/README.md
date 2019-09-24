#### Plans
- Python Backend   
    - API for handling POST requests
        - POST/PUT request JSON body to API sub-path */hardware/*: 
        ```
        {
            hardware_id: 1; 
            address: "ABC…999" 
        }
        ```
        - POST request JSON body to API sub-path */sensor/*:
        ```
        {
            hardware_id: 1; 
            data: [52.5157, 5.8992, 23.57, 40.5] 
        }
        ```
    - Web Application
        - Default view: 
            - Visualize **parked** bikes available for rent on a map
            - Click on bike to get location
        - Advanced view: 
            - Input form for entering IOTA address
            - Show a map of collected data in the session corresponding to the entered IOTA address
- Postgres database
    - Define database structure
