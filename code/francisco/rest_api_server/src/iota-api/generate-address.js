
const IOTA = require('@iota/core')

const iota = IOTA.composeAPI({
    provider: 'https://nodes.iotadev.org'
})

// Generate an address promise
let newAddress = (seed, address_index = 0) => {
    return new Promise( resolve => {
        iota.getNewAddress(seed, {
            index: address_index,
            total: 1,
            // security: 2
        }).then((address) => {
            resolve(address)
            // console.log('Your address is: ' + address)
            // console.log('Your address length is: ' + address[0].length)
        }).catch((e) => {
            console.log(e)
        })
        // Add checksum
    });
}
let generateAddress = async function(seed, address_index){
    let result = await newAddress(seed, address_index)
    return result[0]
}

// generateAddress('WKQDUZTGFKSSLACUCHHLZRKZBHSDSCEBHKUPDLKFBQALEBKDMFRPUQGZRXAADPG9TSRTZGGBZOFRJCFMM')

module.exports = {
    generateAddress
}
