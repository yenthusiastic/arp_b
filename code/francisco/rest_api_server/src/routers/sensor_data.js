const pool = require('../db/postgresql')
const express = require('express')
const bodyParser = require('body-parser')
const router = new express.Router()

// Add new sensor data
router.post('/data', bodyParser.json(), (request, response) => {

    // connect to the DB
    pool.connect((error, client, done) => {
        
        let {hardwareID, address, latitude, longitude, temperature, humidity, timestamp} = request.body
        if(!hardwareID || !address || !latitude || !longitude || !temperature || !humidity || !timestamp){
            response.status(400).send({"HttpStatusCode": 500, "HttpMessage": "Bad Request", "MoreInformation": "Post request does not content required value(s)."})
        }else{
            client.query('INSERT INTO "SENSOR_DATA"("hardwareID", address, latitude, longitude, temperature, humidity, "timestamp") VALUES ($1, $2, $3, $4, $5, $6, $7);',[hardwareID, address, latitude, longitude, temperature, humidity, timestamp], (error,results) => {
                if (error){
                    done()
                    response.status(500).send({"HttpStatusCode": 500, "HttpMessage": "Internal Server Error", "MoreInformation": "Problems requesting data to the database."})
                    throw error
                }
                else{
                    updateHardware(client, hardwareID, latitude, longitude, response)
                    response.status(200).send({"HttpStatusCode": 201, "HttpMessage": "OK", "MoreInformation": "Sensor data added."})
                    done()
                }
            })
        }
    })
})

let updateHardware = (client, hardwareID, latitude, longitude, response) => {
    client.query('UPDATE "HARDWARE_STATUS" SET  latitude = $1, longitude = $2 WHERE "hardwareID" = $3;', [latitude, longitude, hardwareID]), (error, results) => {
        if (error){
            response.status(500).send({"HttpStatusCode": 500, "HttpMessage": "Internal Server Error", "MoreInformation": "Problems requesting data to the database."})
            throw error
        }else{
            response.status(201).send({"HttpStatusCode": 201, "HttpMessage": "OK", "MoreInformation": "Hardware status updated."})
        }
    }
}

module.exports = router