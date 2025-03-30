# **Kaggle Leaderboard Tracker**

This project is a web application that periodically fetches and displays the leaderboard data for a Kaggle competition. The app uses **Flask** for the backend, **Flask-SocketIO** for real-time updates, and **Kaggle's API** for fetching leaderboard data.

---

## **Features**
- 📊 Displays the leaderboard of a Kaggle competition.
- 🔄 Automatically fetches updates every minute.
- 🌐 Provides real-time updates to connected clients using WebSockets.

---

## **Requirements**
Ensure you have the following installed:
- **Python** (version 3.8 or above)
- **Kaggle API**: Set up Kaggle credentials and install the Kaggle CLI.
- **Pipenv** or any Python package manager.

---

## **Installation**

### Clone the repository:
```bash
git clone https://github.com/manarb881/leaderboardAdc/
cd leaderboardAdc
```


### Install the required dependencies:

#### Set up your Kaggle credentials:

Log in to your Kaggle account.

Go to Account Settings and download your API key (kaggle.json).

Place kaggle.json in the appropriate directory:

- **On Linux/MacOS**: ~/.kaggle/

- **On Windows**: %USERPROFILE%\.kaggle\

#### Ensure the Kaggle CLI is installed:


```pip install kaggle```

Test the installation:
```
kaggle competitions list
```
### Running the Application
Start the Flask app:

```python app.py```

Open your browser and navigate to:
http://127.0.0.1:5000/
The leaderboard data will update every minute and will refrech automatically when change is detected.

### Project Structure
- **app.py**: Main Flask application that handles routes and real-time updates.

- **utils/kaggle_api.py**: Utility script to fetch and parse Kaggle leaderboard data.

- **templates/leaderboard.html**: Frontend HTML template for displaying the leaderboard.

### Troubleshooting
Kaggle CLI Issues:

Ensure your kaggle.json is correctly placed and permissions are set:


```chmod 600 ~/.kaggle/kaggle.json```
Missing Dependencies:

Run the following to ensure all dependencies are installed:



### Port Issues:

If port 5000 is already in use, modify the app.py file:


socketio.run(app, host='0.0.0.0', port=<new_port>, debug=True)
Leaderboard Parsing Errors:

#### Check that the competition name is valid and accessible:

``` kaggle competitions leaderboard -c digit-recognizer ```
