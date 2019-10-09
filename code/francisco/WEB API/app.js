const express = require('express');

const app = express();

app.get('/address',(req,res) => {
    res.send('GET()')
    console.log('Get method requested.');
});
app.post('/data',(req,res) => {
    res.send('POST()');
    console.log('Post method requested');
});
app.put('/status',(req,res) => {
    res.send('PUT()');
    console.log('Put method requested');
});
app.listen(5100);
console.log('Listen to port 5100\n');