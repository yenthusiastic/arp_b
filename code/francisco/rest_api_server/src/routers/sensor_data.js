const pool = require('../db/postgresql')
const express = require('express')
const bodyParser = require('body-parser')
const router = new express.Router()

// Add new sensor data
router.post('/data', bodyParser.json(), (request, response) => {
    let {hardwareID, address, latitude, longitude, temperature, humidity, timestamp} = request.body
    if(!hardwareID || !address || !latitude || !longitude || !temperature || !humidity || !timestamp){
        response.status(400).send({"HttpStatusCode": 500, "HttpMessage": "Bad Request", "MoreInformation": "Post request does not content required value(s)."})
    }else{
        pool.query('INSERT INTO "SENSOR_DATA"("hardwareID", address, latitude, longitude, temperature, humidity, "timestamp") VALUES ($1, $2, $3, $4, $5, $6, $7);',[hardwareID, address, latitude, longitude, temperature, humidity, timestamp], (error,results) => {
            if (error){
                response.status(500).send({"HttpStatusCode": 500, "HttpMessage": "Internal Server Error", "MoreInformation": "Problems requesting data to the database."})
                throw error
            }
            response.status(200).send({"HttpStatusCode": 201, "HttpMessage": "OK", "MoreInformation": "Sensor data added."})
        })
    }
})

// Update the hardware (bike)'s status
router.put('/status', bodyParser.json(),(request, response) => {
    let { status, latitude, longitude, hardwareID } = request.body
    if(!status || !latitude || !longitude || !hardwareID){
        response.status(400).send({"HttpStatusCode": 500, "HttpMessage": "Bad Request", "MoreInformation": "Post request does not content required value(s)."})
    }else{
        pool.query('UPDATE "HARDWARE_STATUS" SET status = $1, latitude = $2, longitude = $3 WHERE "hardwareID" = $4;',[status, latitude, longitude, hardwareID],(error, results) => {
            if (error){
                response.status(500).send({"HttpStatusCode": 500, "HttpMessage": "Internal Server Error", "MoreInformation": "Problems requesting data to the database."})
                throw error
            }
            response.status(200).send({"HttpStatusCode": 201, "HttpMessage": "OK", "MoreInformation": "Hardware status updated."})
        })
    }
})

module.exports = router