
const http = require('http')
const fs = require('fs')

const server = http.createServer((req,res)=>{
    console.log("Request from: " + req.url)
    console.log(res.socket.remoteAddress + '\n' + res.socket.remotePort)
    if(req.url === "/home" || req.url === "/"){
        res.writeHead(200,{'Content-Type':'text/html'})
        fs.createReadStream(__dirname + "/index.html").pipe(res)
    }else if(req.url === "/contacts"){
        res.writeHead(200,{'Content-Type':'text/html'})
        fs.createReadStream(__dirname + "/contacts.html").pipe(res)
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
console.log("Listening port 5100")