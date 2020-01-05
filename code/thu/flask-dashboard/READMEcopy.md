### Usage Manual - Admin Dashboard Panel for Bikota Renting System

Version: v0.2 (16.12.2019)

Author: Thu Nguyen

#### 1. Description
The Admin Dashboard Panel is a web platform which provides administration tools for the Bikota Renting Service including managing the mobile renting hardwares, viewing bike distribution on a map, viewing real-time renting statistics, sensor data and managing user preferences.

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

<img src="../../../media/admin_dashboard.PNG" width=70%>


##### 2.2. Map
- On this page the system admin can view the locations of all hardware modules in the system on a map of Germany. Each marker on the map represents one module.
- By hovering over the marker, the admin can view the status and detailed location (Longitude, Lattitude) of the specific hardware. By clicking on the hyperlinked location, the admin will be directed to a Google Maps link where the hardware is located.
- The markers are colored differently depending on the hardware status:
    - Green for `parked`
    - Blue for `rented`
    - Yellow for `offline`
    - Red for `defect`


Preview: 

<img src="../../../media/admin_map.PNG" width=70%>
<img src="../../../media/admin_map2.png" width=50%>


##### 2.3. Charts
- On this page the system admin can view collected sensor data as line charts
- The admin can filter sensor data visualization using the input field/ date time picker and dropdown menus, by following parameters:
    - `Hardware ID`, the unique ID of a hardware module on the bike
    - `Session address`, the unique address of a renting session, which is a 81-character IOTA address that was used to receive payment for that specific renting session
    - `Sensor type`, the type of sensor(s) that is/are attached to a hardware module on the bike
    - and `Time range`, the date time interval within which the admin wishes to view the sensor data 
- When a single hardware ID is selected, the corresponding sensors and session addresses related to that selected hardware will be updated in the <button style="color: #1DC7EA">Sensors type <i class="fa fa-chevron-down"></i></button> and <button style="color: #1DC7EA">Session address <i class="fa fa-chevron-down"></i></button> dropdown menus.
- When a single hardware ID and a session address is selected, the `Time range` date time picker will be disabled as each session has its own associated time interval.
- When a single hardware ID is selected and a time interval is provided/ picked, the <button style="color: #1DC7EA">Session address <i class="fa fa-chevron-down"></i></button> dropdown menu will be disabled.
- When a single hardware ID is selected but no session address or time interval is provided, a default time interval of the last hour will be used for fetching data.
- When multiple hardware IDs are selected, the <button style="color: #1DC7EA">Session address <i class="fa fa-chevron-down"></i></button> dropdown menu will be disabled as no 2 hardware modules share the same session address. 
- The admin can clear the input fields and selections using the <button><i class="fa fa-remove" style="color: red"></i></button> (Clear) icon next to each input field
- The admin has to click on the <button style="color: #1DC7EA">Update Charts</button> button to apply the selected filters. A warning message will pop up if the admin clicks this button while inputs are missing or when no data is found for selected fiters.
- Sensor data corresponding to the selected filters will be displayed as line chart(s) with proper title, legend and labels. Each chart shows the data for only a single sensor type but for one or more hardwares or session addresses.

Preview: 

<img src="../../../media/admin_charts.PNG" width=70%>

##### 2.4. Login/ Register Account
- On this page the system admin can log in with an existing account using a username and password or register a new account using an email, username and password. 
- The username has to contain a minimum of 4 characters and a maximum of 20 characters. 
- The password has to contain a minimum of 6 characters and a maximum of 50 characters. 
- The email has to contain a minimum of 6 characters and a maximum of 50 characters. 


Preview: 

<img src="../../../media/admin_login.PNG" width=70%>
<img src="../../../media/admin_register.PNG" width=70%>


##### 2.5. User Profile
- On this page the system admin can activate any of the 3 following sections to make changes to their account data:
    - `Edit profile` section, where account information can be updated including: Company, Username, Email address, First name, Last name, Address, City, Country, Postal code, Biography. A success message will pop up to notify if the profile is successfully updated in the system.
    - `Change password` section, where the admin can change the account's password by typing in the current and the new passwords. A warning message will pop up if the current password(s) is/are incorrect or do not match.
    - `Delete account` section, where the account can be deleted permanently upon providing the correct password. A success message will pop up to notify if the account is successfully removed from the system.


Preview: 

<img src="../../../media/admin_user1.PNG" width=70%>
<img src="../../../media/admin_user2.PNG" width=51%>