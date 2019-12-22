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
let nextSessionAddress
let privateKey

// TEST
let time = new Date()
console.log('\n*' + time.getSeconds() + ':' + time.getMilliseconds() + '\t# Start time')

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

    // // TEST
    // let time = new Date()
    // console.log('\n*' + time.getSeconds() + ':' + time.getMilliseconds() + '\t# Start getAddress f(x)')
    

    // Check if hardwareID is registered in the DB
    pool.query('SELECT * from "HARDWARE_STATUS" WHERE "hardwareID" = $1;',[hardwareID],(error,results) => {
        if (error) {
            //done()
            response.status(500).send({"HttpStatusCode": 500, "HttpMessage": "Internal Server Error", "MoreInformation": "Problems requesting data to the database."})
            throw error
        } 
        // If Hardware ID exist, request new *address based on the current *address_index
        else if(results.rows[0] != undefined){
            // console.log('\nDevice with ID ' + hardwareID + ' found.')

            // TEST
            let time = new Date()
            console.log('\n*' + time.getSeconds() + ':' + time.getMilliseconds() + '\t# Device with ID ' + hardwareID + ' found.')

            privateKey = results.rows[0].seed
            address_index = results.rows[0].address_index + 1
            address = results.rows[0].next_session_address
            
            // updateHardware_onDataBase(hardwareID,privateKey, address_index, response)
            
            //  // TEST
            // let time2 = new Date()
            // console.log('\n*' + time2.getSeconds() + ':' + time2.getMilliseconds() + '\t# updateHardware_onDataBase is being executed...')
            
            // FUNCTION TO UPDATE next_session_address
            updateHardware(hardwareID, address_index,response)
            // TEST
            let time3 = new Date()
            console.log('\n*' + time3.getSeconds() + ':' + time3.getMilliseconds() + '\t# updateHardware is being executed...')

            // // TEST
            // let time1 = new Date()
            // console.log('\n*' + time1.getSeconds() + ':' + time1.getMilliseconds() + '\t# Finish getAddress f(x)')

            //done();
            // next()
        }
        //  If Hardware ID does not exist, request new *seed, *address, and *address_index
        else {
            console.log('\nDevice with ID ' + hardwareID + ' not found.')
            saveNewHardware(hardwareID, response)
            //done();
        }
    })
}
// Original function with different name
// const updateAddress = (request, response, next) => {
//     let hardwareID = request.params.hardwareID

//     // TEST
//     let time = new Date()
//     console.log('\n*' + time.getSeconds() + ':' + time.getMilliseconds() + '\t# Start updateAddress')

//     // Check if hardwareID is registered in the DB
//     pool.query('SELECT * from "HARDWARE_STATUS" WHERE "hardwareID" = $1;',[hardwareID],(error,results) => {
//         if (error) {
//             //done()
//             response.status(500).send({"HttpStatusCode": 500, "HttpMessage": "Internal Server Error", "MoreInformation": "Problems requesting data to the database."})
//             throw error
//         } 
//         // If Hardware ID exist, request new *address based on the current *address_index
//         else if(results.rows[0] != undefined){
//             // console.log('\nDevice with ID ' + hardwareID + ' found.')

//             // TEST
//             let time = new Date()
//             console.log('\n*' + time.getSeconds() + ':' + time.getMilliseconds() + '\t# Device with ID ' + hardwareID + ' found.')

//             let privateKey = results.rows[0].seed
//             address_index = results.rows[0].address_index + 1
//             address = results.rows[0].next_session_address

//             // INSERT A FUNCTION TO RETURN IN A RESPONSE THE next_session_address as the session_address
//             updateHardware(hardwareID, address_index,response)
//             // FUNCTION TO UPDATE next_session_address
//             // updateHardware_onDataBase(hardwareID,privateKey, address_index, response)
//             //done();
//         }
//          // If Hardware ID does not exist, request new *seed, *address, and *address_index
//         else {
//             console.log('\nDevice with ID ' + hardwareID + ' not found.')
//             saveNewHardware(hardwareID, response)
//             //done();
//         }
//     })
// }

function reqSeed_promise(){
    return new Promise(resolve => {
        resolve(SEED.generateSeed())
    })
}

function reqAddress_promise(seed, address_index){
    return new Promise(resolve => {
        resolve(ADDRESS.generateAddress(seed, address_index))
    })
}

let reqNewSeedAddress_async = async() => {
    let newSeed = await reqSeed_promise().then((result) => {
        seed = result
        return seed
    })
    let newAddress = await reqAddress_promise(newSeed).then((result) => {
        address = result
        let tempAddress
        for(var c = 0 in address[c]){
            if(c == 0) tempAddress = address[c]
            if(c == 1) nextSessionAddress = address[c]
        }
        address = tempAddress
        return address
    })
} 

let reqNewAddress_async = async(seed, address_index) => {
    let newAddress = await reqAddress_promise(seed, address_index).then((result) => {
        address = result
        let tempAddress
        for(var c = 0 in address[c]){
            if(c == 0) tempAddress = address[c]
            if(c == 1) nextSessionAddress = address[c]
        }
        address = tempAddress
        return address
    })
}

let saveNewHardware = async (hardwareID, response) => {                
    // Request new *seed, *address, and *address_index
    await reqNewSeedAddress_async() 
    // Saving values in the DB
    pool.query('INSERT INTO "HARDWARE_STATUS"("hardwareID", "seed", "session_address", "address_index", "next_session_address") VALUES ($1, $2, $3, $4, $5);',[hardwareID, seed, address, address_index = 0, nextSessionAddress], (error,results) => {
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

let updateHardware_onDataBase = async (hardwareID, privateKey, new_address_index, response) => {   
    
    
    // TEST
    let time1 = new Date()
    console.log("\n*" + time1.getSeconds() + ':' + time1.getMilliseconds() + "\t# Inside updateHardware_onDataBase: async started.")
    
    // // Request *address
    await reqNewAddress_async(privateKey, new_address_index) 
    // Saving values in the DB


    // TEST
    let time = new Date()
    console.log("\n*" + time.getSeconds() + ':' + time.getMilliseconds() + "\t# Inside updateHardware_onDataBase: async finished.")

    pool.query('UPDATE "HARDWARE_STATUS" SET "address_index" = $1, "next_session_address" = $2 WHERE "hardwareID" = $3;',[new_address_index, nextSessionAddress, hardwareID], (error,results) => {
        if (error){
            //done();
            response.status(500).send({"HttpStatusCode": 500, "HttpMessage": "Internal Server Error", "MoreInformation": "Problems requesting data to the database."})
            throw error
        }
        //done();
        // console.log("\n# Next session address for hardware with ID " + hardwareID + ' updated.')
                
        // TEST
        let time = new Date()
        console.log("\n*" + time.getSeconds() + ':' + time.getMilliseconds() + "\t# Next session address for hardware with ID " + hardwareID + ' updated.')
        // response.status(201).send({"HttpStatusCode": 201, "HttpMessage": "OK", "Session address": address, "MoreInformation": "Address session and address index were updated in the database."})
    })
}

let updateHardware = (hardwareID, new_address_index, response) => {   
    // Saving values in the DB
    pool.query('UPDATE "HARDWARE_STATUS" SET "address_index" = $1, "session_address" = $2 WHERE "hardwareID" = $3;',[new_address_index, address, hardwareID], (error,results) => {
        if (error){
            //done();
            response.status(500).send({"HttpStatusCode": 500, "HttpMessage": "Internal Server Error", "MoreInformation": "Problems requesting data to the database."})
            throw error
        }
        //done();

        // TEST
        let time = new Date()
        console.log("\n*" + time.getSeconds() + ':' + time.getMilliseconds() + "\t# Session address for hardware with ID " + hardwareID + ' updated.')

        // console.log("\n# Session address for hardware with ID " + hardwareID + ' updated.')
        response.status(201).send({"HttpStatusCode": 201, "HttpMessage": "OK", "Session address": address, "MoreInformation": "Address session and address index were updated in the database."})             
        

        // TEST
        let time2 = new Date()
        console.log('\n*' + time2.getSeconds() + ':' + time2.getMilliseconds() + '\t# updateHardware_onDataBase is being executed...')
             
        updateHardware_onDataBase(hardwareID,privateKey, address_index, response)
        // TEST
        let time1 = new Date()
        console.log("\n*" + time1.getSeconds() + ':' + time1.getMilliseconds() + "\t# Response status sent! ")

    })
}

module.exports = {
    getAddress,
    // updateAddress
}