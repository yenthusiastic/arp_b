const express = require('express')
const port = process.env.PORT || 5100;
const app = express()
const usersRouter = require('./routers/users')
const session_addressRouter = require('./routers/session_address')
const sensor_dataRouter = require('./routers/sensor_data')
const hardware_statusRouter = require('./routers/hardware_status')


app.use(usersRouter)
app.use(session_addressRouter)
app.use(hardware_statusRouter)
app.use(sensor_dataRouter)

app.listen(port,() => console.log(`Listening port ${port}\n`))