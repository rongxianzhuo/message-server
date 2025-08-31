

def push_message(url, authorization, header, message: dict) -> dict:
    import requests
    import json
    url = f'{url}/push'
    data = {
        'header': header,
        'body': message
    }
    json_data = json.dumps(data)
    response = requests.post(url, headers={'Content-Type': 'application/json', "Authorization": authorization}, data=json_data)
    if response.status_code == 200:
        return response.json()
    else:
        print('Failed to get a successful response:', response.status_code)


def push_permanent_message(url, authorization, header, message: dict) -> dict:
    import requests
    import json
    url = f'{url}/push_permanent'
    data = {
        'header': header,
        'body': message
    }
    json_data = json.dumps(data)
    response = requests.post(url, headers={'Content-Type': 'application/json', "Authorization": authorization}, data=json_data)
    if response.status_code == 200:
        return response.json()
    else:
        print('Failed to get a successful response:', response.status_code)


def pull_message(url, authorization, header) -> tuple:
    import requests
    import json
    url = f'{url}/pull'
    data = {
        'header': header,
    }
    json_data = json.dumps(data)
    response = requests.post(url, headers={'Content-Type': 'application/json', "Authorization": authorization}, data=json_data)
    if response.status_code == 200:
        json_data = response.json()
        messages = []
        permanent_message = None
        if 'messages' in json_data:
            messages = json_data['messages']
        if 'permanent' in json_data:
            permanent_message = json_data['permanent']
        return messages, permanent_message
    else:
        print('Failed to get a successful response:', response.status_code)
