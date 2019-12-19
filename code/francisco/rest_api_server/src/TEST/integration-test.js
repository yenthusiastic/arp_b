
const ADDRESS = require('../iota-api/generate-address')
const SEED = require('../iota-api/generate-seed')


function reqSeed(){
    return new Promise(resolve => {
        resolve(SEED.generateSeed())
    })
}
function reqAddress(seed){
    return new Promise(resolve => {
        resolve(ADDRESS.generateAddress(seed))
    })
}

// Set an async-await function to generate a seed and then generate the address
async function async() {
    console.log('\n#1# Calling generate-seed.js...')
    let newSeed = await reqSeed()
    console.log('#2# Result from generate-seed.js is: ' + newSeed)
    console.log('\n#1# Calling generate-address.js...')
    let result = await reqAddress(newSeed)
    console.log('#2# result from generate-address.js is: ' + result)
}

async()