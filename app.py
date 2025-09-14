from flask import Flask, render_template, request, jsonify
import time

app = Flask(__name__, template_folder='.')

messages = []   # [{username, pfp, message, seen_by}]
typing_user = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    data=request.get_json()
    msg={
        "username":data['username'],
        "pfp":data['pfp'],
        "message":data['message'],
        "seen_by": None,
        "timestamp": time.time()
    }
    messages.append(msg)
    return {"status":"ok"}

@app.route('/get_messages', methods=['POST'])
def get_messages():
    global typing_user
    data=request.get_json()
    user=data['username']
    # mark last message as seen by this user
    if messages:
        messages[-1]["seen_by"]=user
    return jsonify({"messages":messages,"typing":typing_user})

@app.route('/typing', methods=['POST'])
def typing():
    global typing_user
    data=request.get_json()
    typing_user=data['username']
    return {"status":"ok"}

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)

