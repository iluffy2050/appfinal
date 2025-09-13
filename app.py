import eventlet
eventlet.monkey_patch()  # MUST be first

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__, template_folder='.')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

users = {}  # sid -> {'username':..., 'pfp':...}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def handle_join(data):
    username = data.get('username')
    pfp = data.get('pfp', '')
    users[request.sid] = {'username': username, 'pfp': pfp}
    emit('user_joined', {'username': username, 'pfp': pfp}, broadcast=True)

@socketio.on('send_message')
def handle_message(data):
    user = users.get(request.sid)
    if not user: return
    message = data.get('message')
    emit('receive_message', {'username': user['username'], 'pfp': user['pfp'], 'message': message}, broadcast=True)

@socketio.on('typing')
def handle_typing(data):
    user = users.get(request.sid)
    if not user: return
    emit('user_typing', {'username': user['username']}, broadcast=True, include_self=False)

@socketio.on('disconnect')
def handle_disconnect():
    user = users.pop(request.sid, None)
    if user:
        emit('user_left', {'username': user['username']}, broadcast=True)

# For local testing only:
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
