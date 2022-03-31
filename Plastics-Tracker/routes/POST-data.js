module.exports = (app, db) => {
    app.post('/', (req, res) => {
        db.query(`
            INSERT INTO plastics.tracking (type, timestamp)
            VALUES (${req.body.type}, NOW())
        `, (err2) => {
            if (err2) {
                console.log(err);
                return res.status(500).json({ error: 'Internal Server Error 500' })
            }
        });
        return res.status(200);
    });
}