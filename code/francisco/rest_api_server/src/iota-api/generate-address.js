
const IOTA = require('@iota/core')
const iotaLib = require('@iota/checksum')

const iota = IOTA.composeAPI({
    provider: 'https://nodes.iotadev.org'
})

// Generate an address promise
let newAddress = (seed, address_index = 0) => {
    return new Promise( resolve => {
        iota.getNewAddress(seed, {
            index: address_index,
            total: 2,
        }).then((addresses) => {
            let addressWithChecksum = new Array(0)
            // Add checksum to each address generated
            for(var address in addresses){
                let addChecksum = iotaLib.addChecksum(addresses[address],9)
                addressWithChecksum.push(addChecksum)
            }
            resolve(addressWithChecksum)            
        }).catch((e) => {
            console.log(e)
        })
    });
}
let generateAddress = async function(seed, address_index){
    let result = await newAddress(seed, address_index)
    return result
}

module.exports = {
    generateAddress
}
