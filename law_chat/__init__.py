from flask import Flask
from flask_socketio import SocketIO
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
# cors_allowed_origins="*"はデバッグ用
socketio = SocketIO(app,cors_allowed_origins="*")  # WebSocket対応

import law_chat.main