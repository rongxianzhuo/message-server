from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


messages = {}


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


if __name__ == '__main__':
    app.run()
