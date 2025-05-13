import os
import sys
import pandas as pd
from datetime import datetime, timedelta
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from predictor import ScorePredictor
from dotenv import load_dotenv

# Load API key from .env if present
load_dotenv()
API_KEY = os.getenv('FOOTBALL_API_KEY')

def get_tomorrow_fixtures(simulate=False):
    if simulate:
        # Return some sample fixtures for simulation
        return [
            {'home_team': 'Manchester United', 'away_team': 'Liverpool', 'competition': 'Premier League', 'utc_date': '2025-04-22T15:00:00Z'},
            {'home_team': 'Real Madrid', 'away_team': 'Barcelona', 'competition': 'La Liga', 'utc_date': '2025-04-22T19:00:00Z'},
            {'home_team': 'Bayern Munich', 'away_team': 'Borussia Dortmund', 'competition': 'Bundesliga', 'utc_date': '2025-04-22T17:30:00Z'}
        ]
    import requests
    tomorrow = (datetime.utcnow() + timedelta(days=1)).strftime('%Y-%m-%d')
    url = f'https://api.football-data.org/v4/matches?dateFrom={tomorrow}&dateTo={tomorrow}'
    headers = {'X-Auth-Token': API_KEY} if API_KEY else {}
    resp = requests.get(url, headers=headers)
    data = resp.json()
    fixtures = []
    for match in data.get('matches', []):
        fixtures.append({
            'home_team': match['homeTeam']['name'],
            'away_team': match['awayTeam']['name'],
            'competition': match['competition']['name'],
            'utc_date': match['utcDate']
        })
    return fixtures

def main(simulate=False):
    fixtures = get_tomorrow_fixtures(simulate=simulate)
    if not fixtures:
        print('No fixtures found for tomorrow.')
        return
    predictor = ScorePredictor()
    results = []
    for fixture in fixtures:
        pred = predictor.predict_score(fixture['home_team'], fixture['away_team'])
        home_result = 'goal' if pred[0] > 0 else 'no goal'
        away_result = 'goal' if pred[1] > 0 else 'no goal'
        results.append({
            'Competition': fixture['competition'],
            'Home': fixture['home_team'],
            'Away': fixture['away_team'],
            'Home Result': home_result,
            'Away Result': away_result,
            'Date': fixture['utc_date']
        })
    df = pd.DataFrame(results)
    print(df)
    today = datetime.now().strftime('%Y-%m-%d')
    csv_filename = f'goal_no_goal_predictions_{today}.csv'
    html_filename = f'goal_no_goal_predictions_{today}.html'
    df.to_csv(csv_filename, index=False)
    df.to_html(html_filename, index=False)
    print(f'Results saved to {html_filename}')

if __name__ == '__main__':
    import sys
    simulate = '--simulate' in sys.argv
    main(simulate=simulate)
