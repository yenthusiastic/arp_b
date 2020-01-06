const express = require('express')
const port = process.env.PORT || 5100;
const app = express()
const usersRouter = require('./routers/users')
const hardware_statusRouter = require('./routers/hardware_status')
const sensor_data = require('./routers/sensor_data')

app.use(usersRouter)
app.use(hardware_statusRouter)
app.use(sensor_data)

app.listen(port,() => console.log(`Listening port ${port}\n`))