const pg = require('pg')
const SEED = require('./generate-seed')
const ADDRESS = require('./generate-address')

let seed
let address
let address_index
let nextSessionAddress

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

let updateHardware_onDataBase = async (hardwareID, privateKey, new_address_index, response) => {   
    // // Request *address
    await reqNewAddress_async(privateKey, new_address_index) 
    // Saving values in the DB
    pool.query('UPDATE "HARDWARE_STATUS" SET "address_index" = $1, "next_session_address" = $2 WHERE "hardwareID" = $3;',[new_address_index, nextSessionAddress, hardwareID], (error,results) => {
        if (error){
            //done();
            response.status(500).send({"HttpStatusCode": 500, "HttpMessage": "Internal Server Error", "MoreInformation": "Problems requesting data to the database."})
            throw error
        }
        //done();
        console.log("\nNext session address for hardware with ID " + hardwareID + ' updated.')
        // response.status(201).send({"HttpStatusCode": 201, "HttpMessage": "OK", "Session address": address, "MoreInformation": "Address session and address index were updated in the database."})
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

function reqAddress_promise(seed, address_index){
    return new Promise(resolve => {
        resolve(ADDRESS.generateAddress(seed, address_index))
    })
}

// Fill the arguments for the function below to update next_session_address on the db.
updateHardware_onDataBase()