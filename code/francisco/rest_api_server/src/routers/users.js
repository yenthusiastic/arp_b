const bcrypt = require ('bcrypt') // https://auth0.com/blog/hashing-in-action-understanding-bcrypt/
const pool = require('../db/postgresql')
const express = require('express')
const router = new express.Router()
const bodyParser = require('body-parser')

router.get('users/no_production_users_view',  (request, response) => {
    pool.query('SELECT * FROM "USERS";', (error,result) => {
        if(error) throw error
        response.status(200).send(result.rows)
    })
})

router.post('/users/register', bodyParser.json(), async (request, response) => {
    const { user, email, password } = request.body
    let hashedPassword = await bcrypt.hash(password,10)
    pool.query('INSERT INTO "USERS" ("user",email,password) VALUES ($1,$2,$3);', [user, email, hashedPassword], (error, result) => {
        if(error) throw error
        response.status(200).send("User added.")
    })
})

router.post('/users/login', bodyParser.json(), (request, response) => {   
    const { email, password } = request.body  
    // Retreive the pwd from the database
    pool.query ('SELECT password FROM "USERS" WHERE email = $1', [email], async (error,result) => {
        if (error) throw error            
        try{S
            // Compare both passwords
            if(await bcrypt.compare(password,result.rows[0].password )){
                response.status(200).send("Login Successful")
            } else{
                response.status(550).send("Wrong Password")
            }
        } catch(e) {
            result.status(500).send()
        }   
    })
})

module.exports = router