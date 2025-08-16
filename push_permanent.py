import requests
import json


url = 'http://127.0.0.1:5000/push_permanent'


data = {
    'header': 'test',
    'body': {
        'test_permanent': 'asd',
    }
}


json_data = json.dumps(data)

response = requests.post(url, headers={'Content-Type': 'application/json'}, data=json_data)


if response.status_code == 200:
    print('Response from server:')
    print(response.json())
else:
    print('Failed to get a successful response:', response.status_code)
