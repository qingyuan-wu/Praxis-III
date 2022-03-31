## HTTP Requests
1. POST request - send data
2. GET request - gets data

* server: `http://localhost:4003/` (could be our website) - post from arduino to server
* GET with webstie server so we can display on HTML (.ejs)

### Database
```sql
CREATE TABLE `plastics`.`tracking` ( `type` INT(10) NOT NULL , `timestamp` DATE NOT NULL ) ENGINE = InnoDB;
```