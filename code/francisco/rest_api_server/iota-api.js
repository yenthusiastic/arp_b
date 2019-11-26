// Testing connection to IOTA Node
// Documentation: https://docs.iota.org/docs/getting-started/0.1/tutorials/get-started
const Iota = require('@iota/core')
const iotaLib = require('@iota/checksum')
const iotaValidators = require('@iota/validators')

// Specify which node to connect to
const iota = Iota.composeAPI({
    // List of IOTA nodes on: https://iota.dance/
    provider: 'https://nodes.devnet.iota.org:443'
    // provider: 'https://papa.iota.family:14267'
})

// Seed for test purpose
const seed = 'WKQDUZTGFKSSLACUCHHLZRKZBHSDSCEBHKUPDLKFBQALEBKDMFRPUQGZRXAADPG9TSRTZGGBZOFRJCFMM'

// Confirm if you are connected to the node and its synced
iota.getNodeInfo().then(info => {
    if(info.latestMilestone === info.latestSolidSubtangleMilestone){
        console.log('Node is synchronized.')
    } else{
        console.log('Node is not synchronized.')
    }
    // console.log(JSON.stringify(info, null,1))
    // console.log(Math.abs(info['latestMilestone'] - info['latestSolidSubtangleMilestone']))
}).catch(error => {
    console.log(error)
})

// Generate an address
let promise = iota.getNewAddress(seed, {
    index: 0,
    security: 2
}).then((address) => {
    console.log('Your address is: ' + address)
    console.log('Your address length is: ' + address.length)
    // Add checksum to the generated address  
    let addressWithChecksum = iotaLib.addChecksum(address)
    console.log('Your address with checksum is:' + addressWithChecksum)
    console.log('Your address length with checksum is: ' + addressWithChecksum.length)
    return addressWithChecksum
}).catch((error) => {
    console.log(error)
})

// Verifying address
setTimeout(() => {
    // console.log(promise)
    console.log(iotaValidators.isAddress(promise._rejectionHandler0))
},5000)
