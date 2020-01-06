const IOTA = require('@iota/core')

const iota = IOTA.composeAPI({
    // List of IOTA nodes on: https://iota.dance/
    // provider: 'https://nodes.devnet.iota.org:443'
    // provider: 'https://papa.iota.family:14267'
    provider: 'https://nodes.iotadev.org'
})

module.exports = iota