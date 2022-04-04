const db = require('../config/db');
const express = require('express');
const router = express.Router();

router.post('/', (req, res) => {
    db.query(`
        INSERT INTO plastics.tracking (type, timestamp)
        VALUES (${req.body.type}, NOW())
    `, (res2, err2) => {
        if (err2) {
            console.log(err2);
            return res.status(500).json({ error: 'Internal Server Error 500' })
        }
    });
    db.query(`
        INSERT INTO plastics.archive (type, timestamp)
        VALUES (${req.body.type}, NOW())
    `,)
    res.status(200);
});

router.post('/reset', (req, res) => {
    db.query(`DELETE FROM plastics.tracking WHERE type=${req.query.type}`)
    db.query(`
        SELECT type, COUNT(*) AS count
        FROM plastics.tracking
        GROUP BY type
    `, (err2, res2) => {
        if (err2) {
            console.log(err2);
            return res.status(500).json({ error: 'Internal Server Error 500' })
        }
        let counts = {1: 0 , 2: 0}
        for (let i=0; i < res2.length; i++) {
            counts[res2[i].type] = res2[i].count
        }
        res.redirect(302, '/')
        res.render('index', { 'data': counts }, function (err, html) {
            res.send(html)
          });
    });
});

router.get('/', (req, res) => {
    db.query(`
        SELECT type, COUNT(*) AS count
        FROM plastics.tracking
        GROUP BY type
    `, (err2, res2) => {
        if (err2) {
            console.log(err2);
            return res.status(500).json({ error: 'Internal Server Error 500' })
        }
        let counts = {1: 0 , 2: 0}
        for (let i=0; i < res2.length; i++) {
            counts[res2[i].type] = res2[i].count
        }
        res.render('index', { 'data': counts })
    });
});

module.exports = router;