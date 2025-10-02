# Laboratory work 4, 5 

## How to launch? 

1. Download this repo to your PC
2. Extract and open root of this project in your terminal
3. Enter command
```shell
pip install -r requirements.txt
```
4. Open file scenery.sql which is in folder ```my_project/db/scenery.sql```
Open it and execute! After that you will have my database 😊
5. Enter command
```shell
python app.py
```
6. Go to http://localhost:5000
But there is nothing xD, better use POSTMAN to check all methods below
7. For checking use ports and methods in POSTMAN:
Port: ```http://127.0.0.1:5000/customers``` or ```transactions``` or ```accounts```
And only method is GET

Forget about it, I will do it later
<!-- Methods: GET, POST, PUT, DEL

Example of POST Method:
```
{"username": "John", "email": "john@example.com", "password": "123123123"}
```
PUT is the same, but you need choose user address, which data to change:
```
http://127.0.0.1:5000/users/{id_user_to_change}
``` -->


# Clouds

## Hot to launch:
### On Ubuntu:

```shell
git clone https://github.com/sergiyclas/db-lab-4-5.git
cd db-lab-4-5
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Tu run:

Go to the root folder of the app:
```shell
cd db-lab-4-5/
```
Run app:
```shell
./vevn/bin/gunicorn -b 0.0.0.0:5000 app:app
```
