const iota = require('./iota-api')

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