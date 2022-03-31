// const mysql = require('mysql');
// var db = mysql.createConnection({
//     host: process.env.DATABASE_HOST,
//     user: process.env.DATABASE_USER,
//     password: process.env.DATABASE_PASSWORD,
//     database: process.env.DATABASE
// });




// const express = require('express');
// const router = express.Router();

// module.exports = router.get('/', (req, res) => {
//     db.query(`
//         SELECT type, COUNT(*) AS count
//         FROM plastics.tracking
//         GROUP BY type
//     `, (err2, res2) => {
//         if (err2) {
//             console.log(err2);
//             return res.status(500).json({ error: 'Internal Server Error 500' })
//         }
//         res.render('/', { 'data': res2 });
//     });
// });

// module.exports = router;