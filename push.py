import util


url = 'http://127.0.0.1:5000'
print(util.push_message(url, '', 'Test', {
        'name': 'lion',
        'age': 18
    }))
