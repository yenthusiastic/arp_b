const express = require('express')
const bodyParser = require('body-parser')
const db = require('./hw-queries')
const db_u = require ('./user-queries')
const port = 5100;
const app = express()

// Code to test request from python
let urlencodedParser = bodyParser.urlencoded({ extended: false });
app.use(urlencodedParser);

// Users view, registration, and login
app.get('/no_production_users_view',db_u.getUsers)
app.post('/register', bodyParser.json(), db_u.registerUsers)
app.post('/login', bodyParser.json(), db_u.loginUsers)
// app.put('/users', bodyParser.json(), db.updateUser)

// Retrieve a new session address for the hardware
app.get('/address/:hardwareID',db.getSessionAddress)
// Add new sensor data
app.post('/data', bodyParser.json(), db.saveSensorData)
// Update the hardware (bike)'s status
app.put('/status', bodyParser.json(), db.updateHardware)

app.listen(port,() => console.log(`Listening port ${port}\n`))