const express = require('express')
const bodyParser = require('body-parser')
const db = require('./hw-queries')
const db_u = require ('./user-queries')
const port = process.env.PORT || 5100;
const app = express()

// User endpoints
app.get('/no_production_users_view',db_u.getUsers)
app.post('/register', bodyParser.json(), db_u.registerUsers)
app.post('/login', bodyParser.json(), db_u.loginUsers)
// app.put('/users', bodyParser.json(), db.updateUser)

// Hardware endpoints
app.get('/address/:hardwareID',db.getSessionAddress)
app.post('/data', bodyParser.json(), db.saveSensorData)
app.put('/status', bodyParser.json(), db.updateHardware)

app.listen(port,() => console.log(`Listening port ${port}\n`))