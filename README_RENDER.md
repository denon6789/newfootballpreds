# Goal/No Goal Predictions Web Service

This Flask app predicts football match outcomes as "goal" or "no goal" for each team, once per day, and displays the results via a web interface. Designed for deployment on Render.com.

## How it works
- At 12:00 PM every day, the prediction script (`main.py`) generates a new prediction file for that day.
- The web server (`web_goal_no_goal.py`) serves the latest predictions for the current day.

## Deploying to Render.com

1. **Push this folder to your GitHub repository.**
2. **Create a new Web Service on Render.com:**
   - Select your repo and this folder as the root.
   - Set the build and start commands:
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `python web_goal_no_goal.py`
   - Set environment variables (e.g. `FOOTBALL_API_KEY`) in the Render dashboard.
3. **(Optional) Schedule Daily Predictions:**
   - Use a Render "Background Worker" or "Cron Job" with command: `python main.py` (scheduled daily at 12:00 PM UTC).

## Environment Variables
- `FOOTBALL_API_KEY`: Your football-data.org API key (add in Render's dashboard).

## Ports
- The Flask app runs on port 11000 by default. Render sets `PORT` automatically, so the app will use that if present.

## Files
- `requirements.txt`: Python dependencies
- `Procfile`: Tells Render how to start the web server
- `main.py`: Generates predictions
- `web_goal_no_goal.py`: Web server

---

If you need help with Render setup, see https://render.com/docs/deploy-flask or ask for more details!
