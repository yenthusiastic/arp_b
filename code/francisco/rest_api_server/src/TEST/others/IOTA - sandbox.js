// Documentation: https://docs.iota.org/docs/getting-started/0.1/tutorials/get-started
const Iota = require('@iota/core')
const crypto = require('crypto')
const iotaLib = require('@iota/checksum')
const iotaValidators = require('@iota/validators')
const Converter = require('@iota/converter')
const TransactionConverter = require('@iota/transaction-converter')

// Specify which node to connect to
const iota = Iota.composeAPI({
    // List of IOTA nodes on: https://iota.dance/
    // provider: 'https://nodes.devnet.iota.org:443'
    // provider: 'https://papa.iota.family:14267'
    provider: 'https://nodes.iotadev.org'
})

// Seed for test purpose
const seed = 'WKQDUZTGFKSSLACUCHHLZRKZBHSDSCEBHKUPDLKFBQALEBKDMFRPUQGZRXAADPG9TSRTZGGBZOFRJCFMM'

// Generate a seed
let GenerateSeed = function () {

    let length       = 81                               // The length of the seed and int array.
    let chars        = "ABCDEFGHIJKLMNOPQRSTUVWXYZ9"    // The allowed characters in the seed.
    let randomValues = new Uint32Array(length)          // An empty array to store the random values.
    let result       = new Array(length)                // An empty array to store the seed characters.

    crypto.randomFillSync(randomValues)                 // Generate random values and store them to randomValues.

    let cursor = 0                                      // A cursor is introduced to remove modulus bias.
    for (let i = 0; i < randomValues.length; i++) {     // Loop through each of the 81 random values.
        cursor += randomValues[i]                       // Add them to the cursor.
        result[i] = chars[cursor % chars.length]        // Assign a new character to the seed based on cursor mod 81.
    }

    return result.join('')                              // Merge the array into a single string and return it.

};

let newSeed = GenerateSeed()
console.log('Seed: ' + newSeed)
console.log('Seed length: ' + newSeed.length)

// Confirm if you are connected to the node and its synced
iota.getNodeInfo().then(info => {
    if(info.latestMilestone === info.latestSolidSubtangleMilestone){
        console.log('Node is synchronized.')
    } else{
        console.log('Node is not synchronized.')
    }
    // console.log(JSON.stringify(info, null,1))
}).catch(error => {
    console.log(error)
})

// Generate an address
let promise = iota.getNewAddress(seed, {
    index: 3,
    total: 1,
    // security: 2
}).then((address) => {
    console.log('Your address is: ' + address)
    console.log('Your address length is: ' + address[0].length)
    // return address
    // Add checksum to the generated address  
    let addressWithChecksum = iotaLib.addChecksum(address[0])
    console.log('Your address with checksum is:' + addressWithChecksum)
    console.log('Your address length with checksum is: ' + addressWithChecksum.length)
    return addressWithChecksum
}).catch((error) => {
    console.log(error)
})

// // Verifying address
// setTimeout(() => {
//     // console.log(promise)
//     console.log(iotaValidators.isAddress(promise._rejectionHandler0))
// },5000)

// // Confirming the balance of the biker
// let userAddr = {
//     address: 'CXDUYK9XGHC9DTSPDMKGGGXAIARSRVAFGHJOCDDHWADLVBBOEHLICHTMGKVDOGRU9TBESJNHAXYPVJ9R9'
// }
// let userAddr = ['CXDUYK9XGHC9DTSPDMKGGGXAIARSRVAFGHJOCDDHWADLVBBOEHLICHTMGKVDOGRU9TBESJNHAXYPVJ9R9']
// console.log('Checking user balance...')
// let verifyUserBalance = iota.getBalances(
//     // userAddr['address'],
//     userAddr,
//     100
// ).then(({balances}) => {
//     console.log(balances)
// }).catch((error) => {
//     console.log('Error: ' + error)
// })