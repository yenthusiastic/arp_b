const express = require('express')
const bodyParser = require('body-parser')
const port = 5100;
const app = express()
const db = require('./queries')

app.get('/users',db.getUsers)
app.post('/users', bodyParser.json(), db.createUser)
app.put('/users', bodyParser.json(), db.updateUser)

// Retrieve a new session address for the hardware
app.get('/address/:hardwareID',db.getSessionAddress)
// Add new sensor data
app.post('/data', bodyParser.json(), db.saveSensorData)
// Update the hardware (bike)'s statuss
app.put('/status', bodyParser.json(), db.updateUser)

app.listen(port,() => console.log(`Listening port ${port}\n`))