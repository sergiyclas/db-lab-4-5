# Laboratory work 4, 5 

## How to launch? 

1. Download this repo to your PC
2. Extract and open root of this project in your terminal
3. Enter command
```shell
pip install -r requirements.txt
```
4. Enter command
```shell
python app.py
```
5. Go to http://localhost:5000

6. For checking use ports and methods:
Port: ```http://127.0.0.1:5000/users```
Methods: GET, POST, PUT, DEL

Example of POST Method:
```
{"username": "John", "email": "john@example.com", "password": "123123123"}
```
PUT is the same, but you need choose user address, which data to change:
```
http://127.0.0.1:5000/users/{id_user_to_change}
```
