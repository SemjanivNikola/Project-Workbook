from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect')
def handle_connect():
    print('Connections established!')

@socketio.on('update_to_team')
def handle_team_update(data):
    emit('teamUpdate', data, json=True, broadcast=True)

@socketio.on('update_to_leader')
def handle_message_to_leader(data):
    emit('updateItemStatus', data, json=True, broadcast=True)


if __name__ == '__main__':
    socketio.run(app)






    