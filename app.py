from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='.')

# Store messages in memory (for simplicity)
messages = []  # each message: {'username':..., 'pfp':..., 'message':...}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    data = request.json
    username = data.get('username')
    pfp = data.get('pfp', '')
    message = data.get('message')
    if username and message:
        messages.append({'username': username, 'pfp': pfp, 'message': message})
    return jsonify({'status': 'ok'})

@app.route('/get_messages')
def get_messages():
    # Return last 50 messages
    return jsonify(messages[-50:])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
