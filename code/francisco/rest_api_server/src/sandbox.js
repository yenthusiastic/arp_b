// async

// function resolveAfter2Seconds() {
//     return new Promise(resolve => {
//       setTimeout(() => {
//         resolve('resolved');
//       }, 2000);
//     });
//   }
  
// async function asyncCall() {
//     console.log('calling');
//     var result = await resolveAfter2Seconds();
//     console.log(result);
//     // expected output: 'resolved'
//   }
  
// asyncCall();

const ADDRESS = require('./iota-api/generate-address')
const SEED = require('./iota-api/generate-seed')

// Set an async-await function to generate a seed and then generate the address
function reqSeed(){
    return new Promise(resolve => {
        resolve(SEED.generateSeed())
    })
}
function reqAddress(){
    return new Promise(resolve => {
        resolve(ADDRESS.generateAddress())
    })
}

async function async() {
    console.log('\n#1# Calling generate-seed.js...')
    let newSeed = await reqSeed()
    console.log('#2# Result from generate-seed.js is: ' + newSeed)
    console.log('\n#1# Calling generate-address.js...')
    let result = await reqAddress()
    console.log('#2# result from generate-address.js is: ' + result)
}

async()

// let newAddress = async function () {
//     console.log('## Calling generate-address.js...')
//     let result = await reqAddress()
//     console.log('## result from generate-address.js is: ' + result)
// }

// console.log(asyncCall())
// newAddress()