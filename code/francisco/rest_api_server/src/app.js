const express = require('express')
const bodyParser = require('body-parser')
const db = require('./hardware-data/query-data')
const db_u = require ('./user/user-queries')
const port = process.env.PORT || 5100;
const app = express()
const db_i = require('./iota-api/query-address')

// Hardware data
app.post('/data', bodyParser.json(), db.saveSensorData)
app.put('/status', bodyParser.json(), db.updateHardware)

// IOTA API
app.get('/address/:hardwareID', db_i.getAddress)

// User data
app.get('/no_production_users_view',db_u.getUsers)
app.post('/register', bodyParser.json(), db_u.registerUsers)
app.post('/login', bodyParser.json(), db_u.loginUsers)
// app.put('/users', bodyParser.json(), db.updateUser)

app.listen(port,() => console.log(`Listening port ${port}\n`))