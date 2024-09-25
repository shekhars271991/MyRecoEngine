curl --location 'http://127.0.0.1:5000/register' \
--header 'Content-Type: application/json' \
--data '{
    "name": "allen",
    "username":"allen",
    "password":"1234"
}'

curl --location 'http://127.0.0.1:5000/register' \
--header 'Content-Type: application/json' \
--data '{
    "name": "shekhar",
    "username":"shekhar",
    "password":"1234"
}'

curl --location 'http://127.0.0.1:5000/register' \
--header 'Content-Type: application/json' \
--data '{
    "name": "suman",
    "username":"suman",
    "password":"1234"
}'
curl --location 'http://127.0.0.1:5000/register' \
--header 'Content-Type: application/json' \
--data '{
    "name": "tara",
    "username":"tara",
    "password":"1234"
}'

curl --location 'http://127.0.0.1:5000/load-movies'