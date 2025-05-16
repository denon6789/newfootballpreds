import os
import subprocess
from flask import Flask, render_template_string, request
import pandas as pd

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Goal/No Goal Predictions</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>
<body class="bg-light">
<div class="container py-4">
    <h1 class="mb-4">Goal/No Goal Predictions</h1>
    <form method="post" class="mb-4">
        <div class="row g-2 align-items-center">
            <div class="col-auto">
                <label for="date" class="col-form-label">Enter date (YYYY-MM-DD):</label>
            </div>
            <div class="col-auto">
                <input type="date" id="date" name="date" class="form-control" required>
            </div>
            <div class="col-auto">
                <button type="submit" class="btn btn-primary">Get Predictions</button>
            </div>
        </div>
    </form>
    {% if table %}
        {{ table|safe }}
    {% else %}
        <div class="alert alert-warning">No predictions available for the selected date.</div>
    {% endif %}
    {% if error %}
        <div class="alert alert-danger mt-3">{{ error }}</div>
    {% endif %}
</div>
</body>
</html>
'''

def get_today_prediction_file():
    today = pd.Timestamp.now().strftime('%Y-%m-%d')
    # Try to find today's prediction file
    files = [f for f in os.listdir('.') if f.startswith('goal_no_goal_predictions') and f.endswith('.html')]
    for f in files:
        if today in f:
            return f
    # Fallback: return the latest
    if files:
        files.sort(reverse=True)
        return files[0]
    return None

@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    if request.method == "POST":
        date_str = request.form.get("date")
        if date_str:
            # Run the prediction script for the given date
            try:
                result = subprocess.run([
                    "python", "predict_for_date.py", date_str
                ], capture_output=True, text=True, timeout=60)
                if result.returncode != 0:
                    error = f"Prediction script error: {result.stderr}"
            except Exception as e:
                error = f"Error running prediction: {e}"
            pred_file = f"goal_no_goal_predictions_{date_str}.html"
        else:
            pred_file = None
    else:
        # GET: show today's predictions
        today = pd.Timestamp.now().strftime('%Y-%m-%d')
        pred_file = f"goal_no_goal_predictions_{today}.html"
    table = None
    if pred_file and os.path.exists(pred_file):
        df = pd.read_html(pred_file)[0]
        table = df.to_html(classes="table table-striped", index=False)
    return render_template_string(HTML_TEMPLATE, table=table, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 11000)), debug=True)
