### Usage Manual - Admin Dashboard Panel for Bikota Renting System

Version: v0.5 (15.01.2020)

Author: Thu Nguyen

#### 1. Description
The Admin Dashboard Panel is a web platform which provides administration tools for the Bikota Renting Service including managing the mobile renting hardwares, viewing bike distribution on a map, viewing real-time renting statistics, sensor data and managing user preferences.

Available currently at [admin.bikota.xyz](http://admin.bikota.xyz)

#### 2. Pages
This section describes the various pages available on the Admin Dashboard Panel and the operations that the system admin can perform on each page.
##### 2.1. Dashboard
- On this page the system admin can view system statistics including:
    - Total number of hardware modules
    - Total number of renting sessions
    - Total number of sensors mounted on hardware modules
    - Total number of cities where bikes are available
    - Bike status statistics pie chart
    - Sensor statistics pie chart
    - Distribution of bike and bike usage by location bar chart

Preview: 

<img src="../media/admin_dashboard.PNG" width=100%>

##### 2.2. Map
- On this page the system admin can have an overview of all hardware modules in the system as distributed on a map of Germany. Each marker on the map represents one module.
- By hovering over the marker, the admin can view the ID and last status of the specific hardware. 
- By clicking on the marker, the map will zoom into the location of that hardware. The admin can view detailed location of the hardware. By clicking on the hyperlinked location, the admin will be directed to a Google Maps link where the hardware is located.
- In the default view, the markers are colored differently depending on the hardware status.

Preview: 

<img src="../media/admin_map.png" width=100%>

<img src="../media/admin_map2.png" width=100%>

- The admin can filter the hardwares using the  `Hardware Status` dropdown menu on the right side of the map.
- The admin can also filter the hardwares on the map by sensor type using the `Sensor Type` dropdown menu. Only hardware modules with selected sensor type attached will be shown on the map. By hovering over the marker, the admin can view the ID of the hardware, the last sensor value and corresponding timestamp recorded from the module. The color of the marker varies depending on the sensor value and the scale on the bottom right corner.  
- The admin can zoom in, zoom out or reset to default zoom with the `+` `-` or `HOME` buttons on the top left corner correspondingly.

Preview: 

<img src="../media/admin_map3.png" width=100%>


##### 2.3. Charts
- On this page the system admin can view collected sensor data as line charts
- The admin can filter sensor data visualization using the input field/ date time picker and dropdown menus, by following parameters:
    - `Hardware ID`, the unique ID of a hardware module on the bike
    - `Session address`, the unique address of a renting session, which is a 81-character IOTA address that was used to receive payment for that specific renting session
    - `Sensor type`, the type of sensor(s) that is/are attached to a hardware module on the bike
    - and `Time range`, the date time interval within which the admin wishes to view the sensor data 
- When a single hardware ID is selected, the corresponding sensors and session addresses related to that selected hardware will be updated in the `Sensor Type` and `Session address` dropdown menus.
- When a single hardware ID and a session address is selected, the `Time range` date time picker will be disabled as each session has its own associated time interval.
- When a single hardware ID is selected and a time interval is provided/ picked, the `Session address` dropdown menu will be disabled.
- When a single hardware ID is selected but no session address or time interval is provided, a default time interval of the last hour will be used for fetching data.
- When multiple hardware IDs are selected, the `Session address` dropdown menu will be disabled as no 2 hardware modules share the same session address. 
- The admin can clear the input fields and selections using the `X` (Clear) icon next to each input field
- The admin has to click on the `Update Charts` button to apply the selected filters. A warning message will pop up if the admin clicks this button while inputs are missing or when no data is found for selected fiters.
- Sensor data corresponding to the selected filters will be displayed as line chart(s) with proper title, legend and labels. Each chart shows the data for only a single sensor type but for one or more hardwares or session addresses.
- The data has been aggregated to render smooth curve on the visualization.

Preview: 

<img src="../media/admin_charts.PNG" width=1000%>

##### 2.4. Hardware Manager
- On this page the system admin can view a table which shows all details of every hardware module registered in the system. These includes:
    - `ID`, which is the unique ID of the hardware module
    - `Status`, which is the latest status of the hardware. The status property can only be 1 out of 4 values: 
        - `parked`, meaning the bike carrying this hardware is in parking state and thus is available for rent
        - `rented`, meaning the bike carrying this hardware is in already in a renting session
        - `defect`, meaning this hardware module is reported defective and thus is not in operation
        - `offline`, meaning this hardware module is functional but not in operation
    - `Attached sensors`, which list all sensor types attached to this hardware module
    - `Location`, which is the latest city/ state/ region where this hardware module can be found
- The admin can additionally perform following actions for the table:
    - search within the table using the `Search` input field
    - toggle fullscreen mode for the table using the toggle button
    - select columns to show or hide in the table using the dropdown menu on the top right
    - navigate between pages
    - select the number of data rows to display per page using the dropup menu on the bottom left
- The admin can manage each hardware modules in the system using the `Actions` buttons in the corresponding row of the table including:
    - Edit details of the hardware using the `Edit` button. A pop-up window will appear for user to make changes to the hardware.
    - Remove the hardware completely from the system using the `X` (Clear) button. A pop-up window will appear for user to confirm this irreversible action.
- The admin can register new a hardware into the system using the `+ Add New Hardware` button. A pop-up window will appear for user to enter details of the new hardware. 
- A warning message will pop up in one of the following cases:
    - The admin tries to register a new hardware which has the same `hardware ID` as an existing one.
    - No `hardware ID` is given while editing existing hardware or  adding new hardware
    - The system is unable to edit/ create/ remove the selected hardware
- A success message will pop up to notify if the selected hardware has been sucessfully edited in/ added to/ removed from the system.

Preview: 

<img src="../media/admin_hardware.PNG" width=100%>

##### 2.5. User Profile
- On this page the system admin can activate any of the 3 following sections to make changes to their account data:
    - `Edit profile` section, where account information can be updated including: Company, Username, Email address, First name, Last name, Address, City, Country, Postal code, Biography. A success message will pop up to notify if the profile is successfully updated in the system.
    - `Change password` section, where the admin can change the account's password by typing in the current and the new passwords. A warning message will pop up if the current password(s) is/are incorrect or do not match.
    - `Delete account` section, where the account can be deleted permanently upon providing the correct password. A success message will pop up to notify if the account is successfully removed from the system.


Preview: 

<img src="../media/admin_user1.PNG" width=100%>
<img src="../media/admin_user2.PNG" width=70%>


##### 2.6. Login/ Register Account
- On this page the system admin can log in with an existing account using a username and password or register a new account using an email, username and password. 
- The username has to contain a minimum of 4 characters and a maximum of 20 characters. 
- The password has to contain a minimum of 6 characters and a maximum of 50 characters. 
- The email has to contain a minimum of 6 characters and a maximum of 50 characters. 


Preview: 

<img src="../media/admin_login.PNG" width=100%>
<img src="../media/admin_register.PNG" width=100%>

-------
Based on [Flask Dashboard Light](https://appseed.us/admin-dashboards/flask-dashboard-light-bootstrap) provided by **AppSeed**
