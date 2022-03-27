const express = require('express');
const router = express.Router();

//this might be wrong
router.post('/', (req, res) => {
    //render index.ejs page
    console.log(req.body.test);
    res.status(200);
    res.render('index', { 'temperature': req.body.test });
});

router.get('/', (req, res) => {
    //render index.ejs page
    console.log(req.body);
    res.render('index', { 'temperature': 5 });
});

module.exports = router;