import requests

def update_leaderboard():
    # Replace with your deployed backend URL; for local testing, use http://127.0.0.1:5001
    url = "http://127.0.0.1:5001/api/update_leaderboard"
    try:
        response = requests.post(url)
        if response.status_code == 200:
            print("Leaderboard updated successfully.")
        else:
            print("Failed to update leaderboard:", response.text)
    except Exception as e:
        print("Error during update:", e)

if __name__ == "__main__":
    update_leaderboard()
