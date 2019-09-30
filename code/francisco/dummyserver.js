// Dummy Server

// Documentation used for http functions
// https://nodejs.org/api/http.html
const http = require('http')

// Documentation used for fs functions
// https://nodejs.org/api/fs.html
const fs = require('fs')

// The following function recives two arguments in the "options" array.
// http.createServer([options][, requestlistener])
// One is the IncomingMessage: in charge of working the request from the browser; and the other one is the ServerResponse: in charge of response the web content to the browser.
const server = http.createServer((req,res)=>{
    console.log('Request from: ' + req.url)
    console.log('Server address: ' + res.socket.remoteAddress + '\n' + 'Server port: ' + res.socket.remotePort)
    if(req.url === "/home" || req.url === "/"){
        res.writeHead(200,{'Content-Type':'text/html'})
        fs.createReadStream(__dirname + '/index.html').pipe(res)
    }else if(req.url === '/contacts'){
        res.writeHead(200,{'Content-Type':'text/html'})
        fs.createReadStream(__dirname + '/contacts.html').pipe(res)
    }else if(req.url === "/api"){
        res.writeHead(200,{'Content-Type':'application/json'})
        let students = [{name:'Cesar',age:12},{name:'Oscar',age:14}]
        res.end(JSON.stringify(students))
    }else{
        res.writeHead(404,{'Content-Type':'text/html'})
        fs.createReadStream(__dirname + '/404.html').pipe(res)
    }
})
server.listen(5100)
console.log("Listening port 5100\n")
