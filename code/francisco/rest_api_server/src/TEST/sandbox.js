

// // Basic async call

//     function resolveAfter2Seconds() {
//         return new Promise(resolve => {
//           setTimeout(() => {
//             resolve('resolved');
//           }, 2000);
//         });
//       }
    
//     async function asyncCall() {
//         console.log('calling');
//         var result = await resolveAfter2Seconds();
//         console.log(result);
//         // expected output: 'resolved'
//       }
//     asyncCall();


// using next on http request 

var app = require("express")();

let time0 = new Date
console.log('Date: ' + time0)

app.get("/", function(httpRequest, httpResponse, next){
    setTimeout(() => {
      let time3 = new Date()
      console.log('Done with async!. Time3: ' + time3.getSeconds() + ':' + time3.getMilliseconds())
    },2000)
    let time1 = new Date()
    console.log('Fisrt function completed. Time1: ' + time1.getSeconds() + ':' + time1.getMilliseconds())
    next(); //remove this and see what happens 
});

app.get("/", function(httpRequest, httpResponse, next){
    httpResponse.send({"HttpStatusCode": 200, "HttpMessage": "Internal Server Error", "MoreInformation": "Problems requesting data to the database."})
    let time2 = new Date()
    console.log('Second function completed. Time2: ' + time2.getSeconds() + ':' + time2.getMilliseconds())
});

app.listen(8080, () => console.log('Listening port 8080.\n'));