const IOTA = require('@iota/core')

const iota = IOTA.composeAPI({
    // List of IOTA nodes on: https://iota.dance/
    // provider: 'https://nodes.devnet.iota.org:443'
    // provider: 'https://papa.iota.family:14267'
    provider: 'https://nodes.iotadev.org'
})

// Confirm if you are connected to the node and its synced
let queryNode =  () => {
    iota.getNodeInfo().then((info) => {
        if(info.latestMilestone === info.latestSolidSubtangleMilestone){
            console.log('Node is synchronized.')
            return true
        } else{
            console.log('Node is not synchronized.')
            return false
        }
    }).catch(error => {
        console.log(error)
    })
}

module.exports = {
    queryNode
}