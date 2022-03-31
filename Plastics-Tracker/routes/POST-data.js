// const mysql = require('mysql');
// var db = mysql.createConnection({
//     host: process.env.DATABASE_HOST,
//     user: process.env.DATABASE_USER,
//     password: process.env.DATABASE_PASSWORD,
//     database: process.env.DATABASE
// });


// const express = require('express');
// const router = express.Router();

// module.exports = router.post('/', (req, res) => {
//     db.query(`
//         INSERT INTO plastics.tracking (type, timestamp)
//         VALUES (${req.body.type}, NOW())
//     `, (err2) => {
//         if (err2) {
//             console.log(err);
//             return res.status(500).json({ error: 'Internal Server Error 500' })
//         }
//     });
//     return res.status(200);
// });

// module.exports = router;