# -*- encoding: utf-8 -*-
"""
Light Bootstrap Dashboard - coded in Flask

Author  : AppSeed App Generator
Design  : Creative-Tim.com
License : MIT 
Support : https://appseed.us/support 
"""

from flask               import render_template, request, url_for, redirect, flash
from flask_login         import login_user, logout_user, current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort
from werkzeug.security   import generate_password_hash
from werkzeug.security   import check_password_hash

from app        import app, lm, db, bc
from app.models import User, SensorData, Hardware
from app.forms  import LoginForm, RegisterForm

# provide login manager with load_user callback
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# authenticate user
@app.route('/logout.html')
def logout():
    logout_user()
    flash("Successfully logged out", "success")
    return redirect(url_for('index'))

# register user
@app.route('/register.html', methods=['GET', 'POST'])
def register():
    
    # declare the Registration Form
    form = RegisterForm(request.form)

    msg = None

    if request.method == 'GET': 

        return render_template('layouts/default.html',
                                content=render_template( 'pages/register.html', form=form) )

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form["username"]
        password = request.form["password"]
        pw_hash = generate_password_hash(password) 
        email = request.form["email"]

        # filter User out of database through username
        user = User.query.filter_by(user=username).first()

        # filter User out of database through username
        user_by_email = User.query.filter_by(email=email).first()

        if user or user_by_email:
            if user:
                msg = 'Error: User {} already exists!'.format(username)
            elif user_by_email:
                 msg = 'Error: Email {} already exists!'.format(email)
            flash(msg, "danger")
        
        else:         
            data = {"firstname": "",
                    "lastname": "",
                    "address" : "",
                    "city": "",
                    "zip": "",
                    "country": "",
                    "bio": ""
            
            }
            user = User(username, email, pw_hash, data)

            user.save()

            msg = 'User created, please login' 
            flash(msg, "success")
            return render_template('layouts/default.html',
                            content=render_template( 'pages/login.html', form=form) )

    else:
        msg = 'Invalid input'
        flash(msg, "danger")

    return render_template('layouts/default.html',
                            content=render_template( 'pages/register.html', form=form ) )

# authenticate user
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    
    # Declare the login form
    form = LoginForm(request.form)

    # Flask message injected into the page, in case of any errors
    msg = None

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form["username"]
        password = request.form["password"]

        # filter User out of database through username
        user = User.query.filter_by(user=username).first()

        if user:
            
            #if bc.check_password_hash(user.password, password):
            if check_password_hash(user.password, password):
                login_user(user)
                current_user.user = username
                flash("Successfully logged in", "success")
                return redirect(url_for('index'))
            else:
                msg = "Invalid password. Please try again."
                flash(msg, "danger")
        else:
            msg = "Invalid username. Please try again."
            flash(msg, "danger")

    return render_template('layouts/default.html',
                            content=render_template( 'pages/login.html', form=form) )

# Render the user page
@app.route('/user.html', methods=['GET', 'POST'])
def user():
    if request.method == "POST":
        if request.form["btn"] == "update_profile":
            username = request.form["username"]
            email = request.form["email"]
            user = User.query.filter_by(user=username).first()  #find user by username
            if user:
                if email != "":
                    user.email = email  #username exists, save new email
            else:
                user = User.query.filter_by(email=email).first()    #username does not exists, find user by email
            if user:
                #email exists, save new username and data
                if username != "":
                    user.user = username    
                firstname = request.form["first_name"]
                lastname = request.form["last_name"]
                address = request.form["address"]
                city = request.form["city"]
                zip = request.form["zip"]
                country = request.form["country"]
                bio = request.form["desc_text"]
                user.data = {"firstname": firstname,
                            "lastname": lastname,
                            "address" : address,
                            "city": city,
                            "zip": zip,
                            "country": country,
                            "bio": bio}
                #update database
                db.session.commit()
                current_user.user = username
                flash("Successfully updated profile for user {}".format(username), "success")
            else:
                #both username and email do not exist, show error
                flash("Invalid username or email", "danger")
                username = current_user.user
        elif request.form["btn"] == "change_pwd":
            username = current_user.user
            user = User.query.filter_by(user=username).first()  #find user by username
            password = request.form["curr_pwd"]
            new_pwd = request.form["new_pwd"]
            if request.form["new_pwd_conf"] == new_pwd:
                if check_password_hash(user.password, password):
                    user.password = generate_password_hash(new_pwd)
                    db.session.commit()
                    flash("Successfully updated password for user {}".format(username), "success")
                else:
                    flash("Current password is invalid", "danger")
            else:
                flash("New passwords do not match", "warning")
        elif request.form["btn"] == "delete_acc":
            username = current_user.user
            user = User.query.filter_by(user=username).first()  #find user by username
            password = request.form["pwd_del"]
            if check_password_hash(user.password, password):
                db.session.delete(user)
                db.session.commit()
                flash("Successfully deleted user account {}".format(username), "success")
                return redirect(url_for('index'))
            else:
                flash("Password is invalid", "danger")
            
    else:
        # GET request
        if current_user.is_authenticated:
            username = current_user.user
        else:
            flash("Please log in or register to access user profile", "warning")
            return redirect('/login.html')
    # filter User out of database through username
    user = User.query.filter_by(user=username).first()
    data = user.data
    
    return render_template('layouts/default.html',
                            content=render_template( 'pages/user.html', 
                            username = user.user,
                            firstname=data["firstname"], 
                            lastname=data["lastname"], 
                            email=user.email, 
                            address=data["address"],
                            city=data["city"],
                            country = data["country"],
                            zip = data["zip"], 
                            user_desc=data["bio"]))

# Render the table page
@app.route('/table.html')
def table():

    return render_template('layouts/default.html',
                            content=render_template( 'pages/table.html') )

# Render the table page
@app.route('/icons.html')
def icons():
    return render_template('pages/icons.html') 


# Render the charts page
@app.route('/charts.html', methods=['GET', 'POST'])
def charts():
    if current_user.is_authenticated:
        session_addresses = dict()
        hw_ids_str = "1"
        sensors_str = "Temperature, Humidity"
        addr_str = ""
        units = {
            "Temperature" : "°C",
            "Humidity" : "%H",
            "CO2" : "PPM",
            "Pressure" : "hPa",
            "PM10" : "PPM",
            "PM25" : "PPM"
        }
        chart_colors = ["rgba(75,192,192,0.4)", "rgba(245,206,66,0.4)", "rgba(112, 214, 96,0.4)"]
        
        if request.method == "POST":
            chart_data = []
            try:
                hw_ids_str = request.form["hw_label"]
                hw_ids = hw_ids_str.split(", ")
            except:
                hw_ids = [hw_ids_str]
            try:
                sensors_str = request.form["sensor_label"]                
                sensors = sensors_str.split(", ")
            except:
                sensors = [sensors_str]
            try:
                addr_str = request.form["addr_label"]
                addr_arr = addr_str.split(", ")
            except:                
                addr_arr = [addr_str]
           
            finally:
                for sensor in sensors:
                    if sensor:
                        data = {}
                        data["chart_id"] = "chart_{}".format(sensor)
                        data["chart_title"] = sensor
                        data["y_axis"] = "{} ({})".format(sensor, units[sensor])
                        data["legend"] = []
                        data["series"] = []
                        data["chart_color"] = chart_colors
                        for hw_id in hw_ids:
                            if hw_id:
                                data["legend"].append("Hardware {}".format(hw_id)) 
                            else:
                                flash("Please select at least one hardware to show graph", "warning")
                        data["series"].append([28.7, 28.9, 29.0, 28.8, 30.0, 30.1, 30.3, 30.4, 30.5, 30.6, 30.8, 31.0])
                        data["series"].append([29.7, 29.9, 30.0, 29.8, 31.0, 31.1, 31.3, 31.4, 31.5, 31.6, 31.8, 32.0])
                        chart_data.append(data)
                    else:
                        flash("Please select at least one sensor type to show graph", "warning")
            
        else:
                
            chart_data = [{
                "chart_id" : "chart1",
                "chart_title" : "Temperature",
                "legend" : "L1",
                "y_axis" : "Temperature (°C)",
                "series" : [28.7, 28.9, 29.0, 28.8, 30.0, 30.1, 30.3, 30.4, 30.5, 30.6, 30.8, 31.0]
            },
            {
                "chart_id" : "chart2",
                "chart_title" : "Humidity",
                "legend": "L2",
                "y_axis" : "Humidity (%)",
                "series" : [33.4, 33.5, 33.7, 33.8, 33.9, 40.0, 40.1, 40.2, 40.3, 40.5, 40.7, 41.0]

            }]

        hw_ids = [hardware.hardwareID for hardware in Hardware.query.order_by(Hardware.hardwareID).all() if hardware.hardwareID != ""]
        sensors = [sensor for sensor in units]
        for hw_id in hw_ids:
            hw_id = "{}".format(hw_id)
            addresses = [hardware.address for hardware in db.session.query(SensorData.address).filter(SensorData.hardwareID==hw_id).distinct().all() if hardware.address != ""]
            session_addresses[hw_id] = addresses
        labels = ['9:00AM', '12:00AM', '3:00PM', '6:00PM', '9:00PM', '12:00PM', '3:00AM', '6:00AM']
        x_axis = "Time"
        minutes = 5
        return render_template('layouts/default.html',
                                content=render_template( 'pages/charts.html',
                                x_axis = x_axis,
                                labels = labels,
                                minutes=minutes,
                                chart_data = chart_data,
                                sensors=sensors,
                                addresses = session_addresses,
                                hw_ids_str=hw_ids_str,
                                sensors_str=sensors_str,
                                addr_str=addr_str),
                               )
    else:
        flash("Please log in or register to access dashboard", "warning")
        return redirect('/login.html')
        



# App main route + generic routing
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path>')
def index(path):
    if current_user.is_authenticated:
        content = None

        try:

            # try to match the pages defined in -> pages/<input file>
            return render_template('layouts/default.html',
                                    content=render_template( 'pages/'+path) )
        except:

            return  render_template('pages/404.html')
    else:
        
        return redirect('/login.html')
