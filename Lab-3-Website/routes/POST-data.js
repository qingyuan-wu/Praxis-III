module.exports = (app, db) => {
    app.post('/', (req, res) => {
        db.query(`INSERT INTO plastics.tracking `)

    })

}