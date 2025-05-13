import os
from flask import Flask, render_template_string
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
    {% if table %}
        {{ table|safe }}
    {% else %}
        <div class="alert alert-warning">No predictions available for today.</div>
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

@app.route("/")
def index():
    pred_file = get_today_prediction_file()
    if not pred_file or not os.path.exists(pred_file):
        return render_template_string(HTML_TEMPLATE, table=None)
    df = pd.read_html(pred_file)[0]
    table = df.to_html(classes="table table-striped", index=False)
    return render_template_string(HTML_TEMPLATE, table=table)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 11000)), debug=True)
