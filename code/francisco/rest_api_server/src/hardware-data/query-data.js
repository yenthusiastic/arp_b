const pg = require('pg')

// Setup the DB variables
const conString = {
    host: 'db.dev.iota.pw',
    // Do not hard code your username and password.
    // Consider using Node environment variables.
    // https://www.npmjs.com/package/pg-pool
    user: 'arp_b',     
    password: 'iota999',
    database: 'arp_b',
    port: 6000,
}
let pool = new pg.Pool(conString)

// Connect to the database
pool.connect(error => {
    if (error) {
        console.log("Problems when connecting to the database.")
        throw error
    }
})

// Add new sensor data
const saveSensorData = (request, response) => {
    let {hardwareID, address, latitude, longitude, temperature, humidity, timestamp} = request.body
    if(!hardwareID || !address || !latitude || !longitude || !temperature || !humidity || !timestamp){
        response.status(400).send({"HttpStatusCode": 500, "HttpMessage": "Bad Request", "MoreInformation": "Post request does not content required value(s)."})
    }else{
        pool.query('INSERT INTO "SENSOR_DATA"("hardwareID", address, latitude, longitude, temperature, humidity, "timestamp") VALUES ($1, $2, $3, $4, $5, $6, $7);',[hardwareID, address, latitude, longitude, temperature, humidity, timestamp], (error,results) => {
            if (error){
                response.status(500).send({"HttpStatusCode": 500, "HttpMessage": "Internal Server Error", "MoreInformation": "Problems requesting data to the database."})
                throw error
            }
            response.status(200).send({"HttpStatusCode": 201, "HttpMessage": "OK", "MoreInformation": "Hardware added."})
        })
    }
    // Create another conditional to avoid hardware duplication
}
// Update the hardware (bike)'s status
const updateHardware = (request, response) => {
    let { status, latitude, longitude, hardwareID } = request.body
    if(!status || !latitude || !longitude || !hardwareID){
        response.status(400).send({"HttpStatusCode": 500, "HttpMessage": "Bad Request", "MoreInformation": "Post request does not content required value(s)."})
    }else{
        pool.query('UPDATE "HARDWARE_STATUS" SET status = $1, latitude = $2, longitude = $3 WHERE "hardwareID" = $4;',[status, latitude, longitude, hardwareID],(error, results) => {
            if (error){
                response.status(500).send({"HttpStatusCode": 500, "HttpMessage": "Internal Server Error", "MoreInformation": "Problems requesting data to the database."})
                throw error
            }
            response.status(200).send({"HttpStatusCode": 201, "HttpMessage": "OK", "MoreInformation": "Status updated."})
        })
    }
}

module.exports = {
    saveSensorData,
    updateHardware
}