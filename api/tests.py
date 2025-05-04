from requests import get, post


print(get('http://127.0.0.1:8080/api/get_users').json())