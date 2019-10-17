const express = require('express')
const bodyParser = require('body-parser')
const port = 5100;
const app = express()
const db = require('./queries')
const db_u = require ('./user-queries')

app.get('/users',db_u.getUsers)
app.post('/users', bodyParser.json(), db_u.createUsers)
app.put('/users', bodyParser.json(), db.updateUser)

app.post('/login', bodyParser.json(), db_u.loginUsers)

// Retrieve a new session address for the hardware
app.get('/address/:hardwareID',db.getSessionAddress)
// Add new sensor data
app.post('/data', bodyParser.json(), db.saveSensorData)
// Update the hardware (bike)'s status
app.put('/status', bodyParser.json(), db.updateHardware)

app.listen(port,() => console.log(`Listening port ${port}\n`))