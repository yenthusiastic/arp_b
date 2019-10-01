// Dummy Server

// Documentation used for http methods
// https://nodejs.org/api/http.html
const http = require('http')

// Documentation used for fs methods
// https://nodejs.org/api/fs.html
const fs = require('fs')

// The following method recives two arguments in the "options" array.
// http.createServer([options][, requestlistener])
// One is the IncomingMessage or "req": in charge of working the request from the browser; and the other one is the ServerResponse or "res": in charge of response the web content to the browser.
const server = http.createServer((req,res)=>{
    console.log('Request from: ' + req.url)
    console.log('Server address: ' + res.socket.remoteAddress + '\n' + 'Server port: ' + res.socket.remotePort)
    if(req.url === "/home" || req.url === "/"){
        // The following method sends a response header to the request.
        // response.writeHead(statusCode[, statusMessage][, headers]) 
        // The status code is a 3-digit HTTP status code, like 404 (erro message). The statusMessage
        // is a optional human-readble message. The last argument is the response header.
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
// The following method start the HTTP server to listen for connections.
// server.listen()
server.listen(5100)
console.log("Listening port 5100\n")
