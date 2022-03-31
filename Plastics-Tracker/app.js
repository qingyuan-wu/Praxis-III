// track when post requests are made from circuitpython
// retrieve those data and display on website

const http = require('http');
const express = require('express');
const PORT = 4003;
const path = require("path");
const app = express();
app.set('view engine', 'ejs');

const db = require('./config/db');

// parse url-encoded bodies (from HTML forms... probably don't need now)
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// get routes
app.use('/', require('./routes/pages'));

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
})