import sys
from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


authorization = ''
messages = {}
permanent_message = {}


def check_authorization(json_request, *params):
    if authorization and request.headers.get("Authorization") != authorization:
        return False
    if not json_request:
        return False
    for i in params:
        if i not in json_request or not json_request[i]:
            return False
    return True


@app.route('/push_permanent', methods=['POST'])
def push_permanent():
    data = request.get_json()
    if not check_authorization(data, 'header', 'body'):
        return '', 400
    header = data['header']
    permanent_message[header] = data['body']
    return jsonify({"status": "success"})


@app.route('/push', methods=['POST'])
def push():
    data = request.get_json()
    if not check_authorization(data, 'header', 'body'):
        return '', 400
    header = data['header']
    body = data['body']
    if header in messages:
        messages[header].append(body)
    else:
        messages[header] = [body, ]
    return jsonify({"status": "success"})


@app.route('/pull', methods=['POST'])
def pull():
    data = request.get_json()
    if not check_authorization(data, 'header'):
        return '', 400
    header = data['header']
    response = {}
    if header in messages and messages[header]:
        response["messages"] = messages[header]
        messages[header] = []

    if header in permanent_message:
        response["permanent"] = permanent_message[header]
    return jsonify(response)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1]:
        authorization = sys.argv[1]
    app.run('0.0.0.0', 5000)
