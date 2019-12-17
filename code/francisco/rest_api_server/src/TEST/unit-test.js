// // Request seed
// const SEED = require('../iota-api/generate-seed')
// function reqSeed(){
//     return new Promise(resolve => {
//         resolve(SEED.generateSeed())
//     })
// }
// let newSeed= async function () {
//     console.log('\n## Calling generate-seed.js...')
//     let result = await reqSeed()
//     console.log('## result from generate-seed.js is: ' + result)
//     console.log('## Result from generate-address.js type is: ' + typeof(result))
//     console.log('## Result length is: ' + result.length + '\n')
// }
// newSeed()

// // Request address
const ADDRESS = require('../iota-api/generate-address')
function reqAddress(seed){
    return new Promise(resolve => {
        resolve(ADDRESS.generateAddress(seed))
    })
}
let newAddress = async function (seed) {
    console.log('\n## Calling generate-address.js...')
    let results = await reqAddress(seed)
    console.log('## Result from generate-address.js type is: ' + typeof(results))
    console.log('## Result length is: ' + results.length + '\n')
    // Loop to check address length and add the Checksum
    for(var result in results){
        // Display each address length
        console.log('Address[' + result +  '] with checksum is: ' +  results[result])
        console.log('Address[' + result +  '] length with checksum is: ' +  results[result].length + '\n')
    }
}
newAddress('CRJZUHXEZETRQROUJITIEDETDVEGKOIHUZTQFETZHZTN9PC9WZEOMT99YP9LKN9KZGPHFFZE99WDTZBYJ')