from law_chat import app, socketio  # `app` と `socketio` をインポート

if __name__ == "__main__":
    socketio.run(app)  # WebSocket を有効にして実行
