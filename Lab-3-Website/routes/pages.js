const express = require('express');
const router = express.Router();

router.post('/', (req, res) => {
    //render index.ejs page
    console.log(req.body);
    res.status(200);
    res.render('index', { 'temperature': req.body.temp, 'brightness': req.body.brightness });
});

router.get('/', (req, res) => {
    //render index.ejs page
    console.log(req.body);
    res.render('index', { 'temperature': 22.23, 'brightness': 150 });
});

module.exports = router;