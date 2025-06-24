from flask import Flask, render_template
from flask_socketio import SocketIO, send
import os 

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

# Initialize SocketIO with app
socketio = SocketIO(app)

# --- Message Storage ---
chat_log = 'chatlog.txt'

# Create the file if it doesn't exist
if not os.path.exists(chat_log):
    open(chat_log, 'w').close()

# Main route (when someone goes to "/")
@app.route('/')
def index():
    return render_template('index.html')  # This will load our HTML chat page

@app.route('/messages')
def get_messages():
    with open(chat_log, 'r') as f:
        messages = f.readlines()
    return {'messages': messages}


# Handle incoming messages
@socketio.on('message')
def handleMessage(msg):
    with open(chat_log, 'a') as f:
        f.write(msg + '\n')
    send(msg, broadcast=True)


# Run the app
if __name__ == '__main__':
    socketio.run(app, debug=True)

