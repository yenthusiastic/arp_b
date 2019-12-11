// Close db connection when finish by adding '//done()'
// https://stackoverflow.com/questions/34803691/node-js-and-pg-module-how-can-i-really-close-connection
// https://mherman.org/blog/postgresql-and-nodejs/

// If problem on production server persist, check the link below
// https://www.postgresql.org/message-id/63BB752C-5997-497C-9846-3475ADC9EB00@ausvet.com.au


const pg = require('pg')
const SEED = require('./generate-seed')
const ADDRESS = require('./generate-address')

let seed
let address
let address_index

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

// Connect to the DB
pool.connect(error => {
    if (error) {
        console.log("Problems when connecting to the database.")
        throw error
    }
})

// Request IOTA address and return it in the http response    
const getAddress = (request, response) => {
    let hardwareID = request.params.hardwareID

    // Check if hardwareID is registered in the DB
    pool.query('SELECT * from "HARDWARE_STATUS" WHERE "hardwareID" = $1;',[hardwareID],(error,results) => {
        if (error) {
            //done()
            response.status(500).send({"HttpStatusCode": 500, "HttpMessage": "Internal Server Error", "MoreInformation": "Problems requesting data to the database."})
            throw error
        } 
        // If Hardware ID exist, request new *address based on the current *address_index
        else if(results.rows[0] != undefined){
            console.log('\nDevice with ID ' + hardwareID + ' found.')
            let privateKey = results.rows[0].seed
            address_index = results.rows[0].address_index + 1
            updateHardware(hardwareID, privateKey, address_index,response)
            //done();
        }
         // If Hardware ID does not exist, request new *seed, *address, and *address_index
        else {
            console.log('\nDevice with ID ' + hardwareID + ' not found.')
            saveNewHardware(hardwareID, response)
            //done();
        }
    })
}

module.exports = {
    getAddress
}

function reqSeed(){
    return new Promise(resolve => {
        resolve(SEED.generateSeed())
    })
}

function reqAddress(seed, address_index){
    return new Promise(resolve => {
        resolve(ADDRESS.generateAddress(seed, address_index))
    })
}

let req_seed_address = async() => {
    let newSeed = await reqSeed().then((result) => {
        seed = result
        return seed
    })
    let newAddress = await reqAddress(newSeed).then((result) => {
        address = result
        return address
    })
} 

let saveNewHardware = async (hardwareID, response) => {                
    // Request new *seed, *address, and *address_index
    await req_seed_address() 
    // Saving values in the DB
    pool.query('INSERT INTO "HARDWARE_STATUS"("hardwareID", "seed", "session_address", "address_index") VALUES ($1, $2, $3, $4);',[hardwareID, seed, address, address_index = 0], (error,results) => {
        if (error){
            //done();
            response.status(500).send({"HttpStatusCode": 500, "HttpMessage": "Internal Server Error", "MoreInformation": "Problems requesting data to the database."})
            throw error
        }
        //done();
        console.log("\nHardware with ID " + hardwareID + ' added.')
        response.status(201).send({"HttpStatusCode": 201, "HttpMessage": "OK", "Session address": address, "MoreInformation": "Private key and session address were added to the database."})
    })
}

let req_address = async(seed, address_index) => {
    let newAddress = await reqAddress(seed, address_index).then((result) => {
        address = result
        return address
    })
}

let updateHardware = async (hardwareID, privateKey, new_address_index, response) => {                
    // Request *address
    await req_address(privateKey, new_address_index) 
    // Saving values in the DB
    pool.query('UPDATE "HARDWARE_STATUS" SET "address_index" = $1, "session_address" = $2 WHERE "hardwareID" = $3;',[new_address_index, address, hardwareID], (error,results) => {
        if (error){
            //done();
            response.status(500).send({"HttpStatusCode": 500, "HttpMessage": "Internal Server Error", "MoreInformation": "Problems requesting data to the database."})
            throw error
        }
        //done();
        console.log("\nHardware with ID " + hardwareID + ' updated.')
        response.status(201).send({"HttpStatusCode": 201, "HttpMessage": "OK", "Session address": address, "MoreInformation": "Address session and address index were updated in the database."})
    })
}