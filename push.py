import requests
import json


url = 'http://127.0.0.1:5000/push'


data = {
    'header': 'test',
    'body': {
        'name': 'lion',
        'age': 18
    }
}


json_data = json.dumps(data)

response = requests.post(url, headers={'Content-Type': 'application/json', "Authorization": '123456'}, data=json_data)


if response.status_code == 200:
    print('Response from server:')
    print(response.json())
else:
    print('Failed to get a successful response:', response.status_code)
