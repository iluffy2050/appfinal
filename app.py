from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__, template_folder=".")
app.config["SECRET_KEY"] = "secret!"

# Use Gevent instead of Eventlet
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="gevent")

users = {}
messages = []

@app.route("/")
def index():
    return render_template("index.html")

# --- SocketIO handlers (same as before) ---
@socketio.on("join")
def handle_join(data):
    username = data.get("username")
    pfp = data.get("pfp", "https://cdn-icons-png.flaticon.com/512/149/149071.png")
    users[request.sid] = {"username": username, "pfp": pfp}
    emit("user_joined", {"username": username}, broadcast=True)

@socketio.on("send_message")
def handle_message(data):
    user = users.get(request.sid, {"username": "Anonymous", "pfp": "https://cdn-icons-png.flaticon.com/512/149/149071.png"})
    message = {
        "username": user["username"],
        "pfp": user["pfp"],
        "text": data.get("message", ""),
    }
    messages.append(message)
    emit("receive_message", message, broadcast=True)

@socketio.on("typing")
def handle_typing():
    user = users.get(request.sid)
    if user:
        emit("user_typing", {"username": user["username"]}, broadcast=True, include_self=False)

@socketio.on("seen")
def handle_seen():
    user = users.get(request.sid)
    if user:
        emit("seen_message", {"username": user["username"]}, broadcast=True, include_self=False)

@socketio.on("disconnect")
def handle_disconnect():
    user = users.pop(request.sid, None)
    if user:
        emit("user_left", {"username": user["username"]}, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
