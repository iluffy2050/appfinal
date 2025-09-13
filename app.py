from flask import Flask, render_template, request, jsonify
import time

app = Flask(__name__, template_folder='.')

# Store messages in memory
messages = []  # {'username','pfp','message','timestamp','seen':set()}
typing_users = set()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    data = request.json
    username = data.get('username')
    pfp = data.get('pfp','')
    message = data.get('message')
    if username and message:
        messages.append({
            'username': username,
            'pfp': pfp,
            'message': message,
            'timestamp': time.time(),
            'seen': set()  # track who has seen
        })
    return jsonify({'status':'ok'})

@app.route('/get_messages', methods=['POST'])
def get_messages():
    user = request.json.get('username')
    # Mark all messages as seen by this user
    for msg in messages:
        msg['seen'].add(user)
    # Return last 50 messages
    data = []
    for msg in messages[-50:]:
        data.append({
            'username': msg['username'],
            'pfp': msg['pfp'],
            'message': msg['message'],
            'seen_count': len(msg['seen'])
        })
    return jsonify(data)

@app.route('/typing', methods=['POST'])
def typing():
    user = request.json.get('username')
    if user:
        typing_users.add(user)
    return jsonify({'status':'ok'})

@app.route('/get_typing', methods=['GET'])
def get_typing():
    # Return typing users and clear set
    users = list(typing_users)
    typing_users.clear()
    return jsonify(users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
