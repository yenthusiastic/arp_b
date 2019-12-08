const pg = require('pg')
const bcrypt = require ('bcrypt') // https://auth0.com/blog/hashing-in-action-understanding-bcrypt/

const conString = {
    host: 'db.dev.iota.pw',
    // Do not hard code your username and password.
    // Consider using Node environment variables.
    // https://www.npmjs.com/package/pg-pool
    user: 'arp_b',     
    password: 'iota999',
    database: 'arp_b',
    port: 6000,
}
let pool = new pg.Pool(conString)

// Connect to the database
pool.connect(error => {
    if (error) {
        console.log("Problems when connecting to the database.")
        throw error
    }
})

const getUsers = (request, response) => {
    pool.query('SELECT * FROM "USERS";', (error,result) => {
        if(error) throw error
        response.status(200).send(result.rows)
    })
}
const registerUsers = async (request, response) => {
    const { user, email, password } = request.body
    let hashedPassword = await bcrypt.hash(password,10)
    pool.query('INSERT INTO "USERS" ("user",email,password) VALUES ($1,$2,$3);', [user, email, hashedPassword], (error, result) => {
        if(error) throw error
        response.status(200).send("User added.")
    })
}
const loginUsers = (request, response) => {   
    const { email, password } = request.body  
    // Retreive the pwd from the database
    pool.query ('SELECT password FROM "USERS" WHERE email = $1', [email], async (error,result) => {
        if (error) throw error            
        try{
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
}

module.exports = {
    getUsers,
    registerUsers,
    loginUsers,
}