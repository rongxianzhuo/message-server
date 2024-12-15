from flask import Flask, request, jsonify
from flask_cors import CORS
import time


api_keys = set()


app = Flask(__name__)
CORS(app)


messages = {}
chat_messages = {}


@app.route('/add_api_key', methods=['POST'])
def add_api_key():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    if 'header' not in data:
        return jsonify({"error": "No header provided"}), 400

    header = data['header']

    if not header:
        return jsonify({"error": "No header provided"}), 400

    if 'body' not in data:
        return jsonify({"error": "No body provided"}), 400

    body = data['body']

    if not body:
        return jsonify({"error": "No body provided"}), 400

    api_keys.add(body)

    return jsonify({"status": "success"})


@app.route('/push', methods=['POST'])
def push():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    if 'header' not in data:
        return jsonify({"error": "No header provided"}), 400

    header = data['header']

    if not header:
        return jsonify({"error": "No header provided"}), 400

    if 'body' not in data:
        return jsonify({"error": "No body provided"}), 400

    body = data['body']

    if not body:
        return jsonify({"error": "No body provided"}), 400

    if header in messages and messages[header]:
        messages[header].append(body)
    else:
        messages[header] = [body, ]

    return jsonify({"status": "success"})


@app.route('/pull', methods=['POST'])
def pull():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    if 'header' not in data:
        return jsonify({"error": "No header provided"}), 400

    header = data['header']

    if not header:
        return jsonify({"error": "No header provided"}), 400

    if header not in messages:
        return jsonify({"status": "success", "messages": []}), 200

    body_list = messages[header]

    if body_list:
        messages[header] = []
        return jsonify({"status": "success", "messages": body_list})
    else:
        return jsonify({"error": "No message"})


@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    print("call chat_completions")
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Unauthorized"}), 401

    api_key = auth_header.split(' ')[1]
    if api_key not in api_keys:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    message_history = data['messages']
    print(message_history)
    start_index = 0
    if api_key in chat_messages:
        start_index = len(chat_messages[api_key])
    if start_index >= len(message_history):
        print("message not change")
        return
    chat_messages[api_key] = message_history
    message_header = f"chat-request:{api_key}"
    if message_header not in messages:
        messages[message_header] = []
    for i in message_history[start_index:]:
        messages[message_header].append(i)

    # response_header = f"chat-response:{api_key}"
    # while response_header not in messages or not messages[response_header]:
    #     time.sleep(1)
    # response_message = ''.join(messages[response_header])
    # messages[response_header] = []
    response_message = "test response"

    # Generate a dummy response
    response = {
        "id": "0",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": "gpt-dummy",
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": response_message
                },
                "finish_reason": "stop",
                "index": 0
            }
        ],
        "usage": {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0
        }
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)
