const pool = require('../db/postgresql')
const express = require('express')
const bodyParser = require('body-parser')
const router = new express.Router()

// Update the hardware (bike)'s status
router.put('/status', bodyParser.json(),(request, response) => {
    
    // connect to the DB
    pool.connect((error, client, done) => {

        let { status, latitude, longitude, hardwareID } = request.body
        if(!status || !latitude || !longitude || !hardwareID){
            done()
            response.status(400).send({"HttpStatusCode": 500, "HttpMessage": "Bad Request", "MoreInformation": "Post request does not content required value(s)."})
        }else{
            client.query('UPDATE "HARDWARE_STATUS" SET status = $1, latitude = $2, longitude = $3 WHERE "hardwareID" = $4;',[status, latitude, longitude, hardwareID],(error, results) => {
                if (error){
                    response.status(500).send({"HttpStatusCode": 500, "HttpMessage": "Internal Server Error", "MoreInformation": "Problems requesting data to the database."})
                    throw error
                }else{
                    done()
                    response.status(200).send({"HttpStatusCode": 201, "HttpMessage": "OK", "MoreInformation": "Hardware status updated."})
                }
            })
        }
    })
})

module.exports = router