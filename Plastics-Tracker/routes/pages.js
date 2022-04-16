const db = require('../config/db');
const express = require('express');
const router = express.Router();
const dayjs = require('dayjs');

router.post('/', (req, res) => {
    db.query(`
        INSERT INTO plastics.tracking (type, timestamp)
        VALUES (${req.body.type}, NOW())
    `, (err2, res2) => {
        if (err2) {
            console.log(err2);
            return res.status(500).json({ error: 'Internal Server Error 500' })
        }
    });
    db.query(`
        INSERT INTO plastics.archive (type, timestamp)
        VALUES (${req.body.type}, NOW())
    `, (err3, res3) => {
        if (err3) {
            console.log(err3);
            return res.status(500).json({ error: 'Internal Server Error 500' })
        }
    });
    // must .send() or else request won't terminate
    return res.status(200).send("posting successful");
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
        const start = dayjs().startOf('day').subtract(6, 'day').toISOString();
        db.query(`
            SELECT *
            FROM plastics.archive
            WHERE timestamp > '${start}'
        `, (err3, res3) => {
            if (err3) {
                console.log(err3);
                return res.status(500).json({ error: 'Internal Server Error 500' })
            }
            let counts = {1: 0 , 2: 0}
            for (let i=0; i < res2.length; i++) {
                counts[res2[i].type] = res2[i].count

            }
            let type1 = [0,0,0,0,0,0,0];
            let type2 = [0,0,0,0,0,0,0];
            for (let i=0; i < res3.length; i++) {
                time = res3[i].timestamp
                const diffTime = Date.parse(dayjs().startOf('day')) - Date.parse(time);
                const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)); 
                loc = 6 - diffDays
                if (res3[i].type == 1) {
                    type1[loc] += 1
                }
                else if (res3[i].type == 2) {
                    type2[loc] += 1
                }
            }
            graph1 = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
            graph2 = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
            for (let i=0; i < 7; i++) {
                graph1[i][0] = dayjs().startOf('day').subtract(6-i, 'day').format('MMM D');
                graph1[i][1] = type1[i];
                graph2[i][0] = dayjs().startOf('day').subtract(6-i, 'day').format('MMM D');
                graph2[i][1] = type2[i];
            }

            res.render('index', { 'data': counts, 'graph1' : graph1, 'graph2' : graph2 })
        });       
    });
});

router.get('/latest', (req, res) => {
    db.query(`
    SELECT type, MAX(timestamp) as time
    FROM plastics.tracking
    `, (err2, res2) => {
        if (err2) {
            console.log(err2);
            return res.status(500).json({ error: 'Internal Server Error 500' });
        }
    res.json({ "latest": res2 });
    })
});

module.exports = router;