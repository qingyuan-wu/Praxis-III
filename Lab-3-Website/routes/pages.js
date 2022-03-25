const express = require('express');
const router = express.Router();

//this might be wrong
router.get('/', (req, res) => {
    //render index.ejs page
    console.log(req.body);
    res.render('index', { 'temp': req.body });
});

module.exports = router;