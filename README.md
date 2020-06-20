# Restaurant app

## Tables reservation
App gives users opportunity to make tables reservation in restaurant

## API

### Tables
Get list of tables
``` 
GET api/tables
```
Response:
```
200 OK
[{"id":  100, "max_capacity":  4, "shape":  "oval", "coordinates":  100, "size":  100}]
```
### Reservations

Get reservations on date 
```
GET api/reservations/?date=2020-07-21
```
Response
```
200 OK
{["id": 1, "tables": [1, 2], "date": "2020-07-21"]}

400 BAD REQUEST
{"error": "Wrong date format, need to be like YYYY-MM-DD"}
```

Create reservation for table
``` 
POST api/reservations/
```
Parameters:

Name | Type | Description
--- | --- | ---
name | str | name of the client
email | str | client's email
tables | [int] | tables for reservation
date | str | YYYY-MM-DD

Example:
```json
{"name":  "John", "email":  "test_email@test.com", "tables":  [2], "date":  "2020-02-06"}
```
Response:
```
201 Created
{"id": 1}
```
