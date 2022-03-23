const express = require('express');
const router = express.Router();

router.get('/', (req, res) => {
    //render index.ejs page
    res.render('index', {  });
});

module.exports = router;