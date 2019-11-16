// DB setup
const pg = require('pg')

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

// DB Connection
pool.connect(error => {
    if (error) {
        console.log("Problems when connecting to the database.")
        throw error
    }
})

// Hardware queries
const getSessionAddress = (request, response) => {
    let hardwareID = request.params.hardwareID
    pool.query('SELECT * from "HARDWARE_STATUS" WHERE "hardwareID" = $1;',[hardwareID],(error,results) => {
        if (error) {
            response.status(500).send({"HttpStatusCode": 500, "HttpMessage": "Internal Server Error", "MoreInformation": "Problems requesting data to the database."})
            throw error
        }
        response.status(200).json(results.rows)
        // response.render(results.rows)
    })
}
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
            response.status(200).send({"HttpStatusCode": 200, "HttpMessage": "OK", "MoreInformation": "Hardware added."})
        })
    }
    // Create another conditional to avoid hardware duplication
}
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
            response.status(200).send({"HttpStatusCode": 200, "HttpMessage": "OK", "MoreInformation": "Status updated."})
        })
    }
}

module.exports = {
    getSessionAddress,
    saveSensorData,
    updateHardware
}