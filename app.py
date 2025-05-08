
from gevent import monkey
monkey.patch_all()
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
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Cache for leaderboard data
leaderboard_cache = {}
app.config['LAST_UPDATE_TIME'] = {}

# Set a default competition start date (adjust as necessary)
DEFAULT_COMPETITION_START_DATE = datetime(2025, 3, 1)

@app.route("/api/leaderboard/<competition_name>", methods=["GET"])
def get_leaderboard_data(competition_name):
    try:
        # Fetch leaderboard data either from cache or from API
        data = leaderboard_cache.get(competition_name) or fetch_leaderboard_data(competition_name)
        
        # Determine last updated time
        last_updated_display = (
            app.config['LAST_UPDATE_TIME'].get(competition_name).strftime("%Y-%m-%d %H:%M:%S")
            if app.config['LAST_UPDATE_TIME'].get(competition_name)
            else DEFAULT_COMPETITION_START_DATE.strftime("%Y-%m-%d %H:%M:%S")
        )
        
        return jsonify({
            "leaderboard": data,
            "last_updated": last_updated_display
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# New API route: When this endpoint is POSTed to, update the leaderboard.
@app.route("/api/update_leaderboard/<competition_name>", methods=["POST"])
def update_leaderboard(competition_name):
    try:
        new_data = fetch_leaderboard_data(competition_name)
        
        # Update cache with the new data for the specific competition
        leaderboard_cache[competition_name] = new_data
        app.config['LAST_UPDATE_TIME'][competition_name] = datetime.now()
        
        # Notify clients via socket about the leaderboard update
        socketio.emit('update_leaderboard', {'competition_name': competition_name, 'leaderboard': new_data})
        
        return jsonify({"message": "Leaderboard updated successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    socketio.run(app, host="0.0.0.0", port=port, debug=False)
