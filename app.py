from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from flask_cors import CORS
from utils.kaggle_api import fetch_leaderboard_data
from datetime import datetime
import time
import threading
import secrets
import os

# Generate a secret key
secret_key = secrets.token_hex(16)

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

# Cache for leaderboard data
leaderboard_cache = None
app.config['LAST_UPDATE_TIME'] = None

COMPETITION_START_DATE = datetime(2025, 3, 1)

@app.route("/api/leaderboard", methods=["GET"])
def get_leaderboard_data():
    competition_name = "digit-recognizer"
    try:
        data = leaderboard_cache or fetch_leaderboard_data(competition_name)
        last_updated_display = (
            app.config['LAST_UPDATE_TIME'].strftime("%Y-%m-%d %H:%M:%S")
            if app.config['LAST_UPDATE_TIME']
            else COMPETITION_START_DATE.strftime("%Y-%m-%d %H:%M:%S")
        )
        return jsonify({
            "leaderboard": data,
            "last_updated": last_updated_display
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# New API route: When this endpoint is POSTed to, update the leaderboard.
@app.route("/api/update_leaderboard", methods=["POST"])
def update_leaderboard():
    competition_name = "digit-recognizer"
    try:
        new_data = fetch_leaderboard_data(competition_name)
        global leaderboard_cache
        leaderboard_cache = new_data
        app.config['LAST_UPDATE_TIME'] = datetime.now()
        socketio.emit('update_leaderboard', {'leaderboard': leaderboard_cache})
        return jsonify({"message": "Leaderboard updated successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    socketio.run(app, host="0.0.0.0", port=port, debug=False)
