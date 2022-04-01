const db = require('../config/db');
const express = require('express');
const router = express.Router();

router.post('/', (req, res) => {
    if(req.body.request == "reset") {
        db.query(`DELETE FROM plastics.tracking WHERE type=${req.body.type}`)
    }
    if(req.body.request == "newdata")
        db.query(`
            INSERT INTO plastics.tracking (type, timestamp)
            VALUES (${req.body.type}, NOW())
        `, (res2, err2) => {
            if (err2) {
                console.log(err2);
                return res.status(500).json({ error: 'Internal Server Error 500' })
            }
        });
    res.status(200);
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
        let obj = {1: 0 , 2: 0}
        for (i=0; i< res2.length; i++) {
            obj[res2[i].type] = res2[i].count

        }
        res.render('index', { 'data': obj });
    });
});

module.exports = router;