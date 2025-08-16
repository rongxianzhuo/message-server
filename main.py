from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


messages = {}
permanent_message = {}


@app.route('/push_permanent', methods=['POST'])
def push_permanent():
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

    permanent_message[header] = body

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
        return jsonify({}), 200

    body_list = messages[header]

    if body_list:
        messages[header] = []
        if header in permanent_message:
            return jsonify({"permanent": permanent_message[header], "messages": body_list})
        else:
            return jsonify({"messages": body_list})
    else:
        if header in permanent_message:
            return jsonify({"permanent": permanent_message[header]})
        else:
            return jsonify({})


if __name__ == '__main__':
    app.run('0.0.0.0', 5000)
