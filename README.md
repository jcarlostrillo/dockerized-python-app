# dockerized-python-app

Basic python APP that contains a REST API. 

## API

The API is running in the port 5001

+ GET - '/requests': Retrieves a list of all the requests stored in the PostgreSQL database.
+ GET '/requests/create': Create a new entry in the PostgreSQL database with the information of the rquest:
  + IP ADDRESS
  + HOSTNAME
  + PATH ('/request/create')
  + HOSTNAME
  + TIME
+ GET '/requests/file': Persist the rquest information in a file: '/tmp/requests.txt'

## Commands

To start the python app and the PostgreSQL database:

```bash
docker-compose up
```