const pg = require('pg')

// Setup the DB variables
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
const pool = new pg.Pool(conString)

module.exports = pool

















// NOTES

// Close db connection when finish by adding '//done()'
// https://stackoverflow.com/questions/34803691/node-js-and-pg-module-how-can-i-really-close-connection
// https://mherman.org/blog/postgresql-and-nodejs/

// Export "pool" object to reused in other files.
// https://stackoverflow.com/questions/39059990/reusing-pg-pool-via-module-exports#
// https://stackoverflow.com/questions/44643652/using-postgres-with-nodejs-for-connection-pool
// https://stackoverflow.com/questions/8484404/what-is-the-proper-way-to-use-the-node-js-postgresql-module