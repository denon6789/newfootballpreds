import os
import sys
import pandas as pd
from datetime import datetime, timedelta
from predictor import ScorePredictor
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('FOOTBALL_API_KEY')

def get_fixtures_for_date(target_date, simulate=False):
    if simulate:
        # Return some sample fixtures for simulation
        return [
            {'home_team': 'Manchester United', 'away_team': 'Liverpool', 'competition': 'Premier League', 'utc_date': f'{target_date}T15:00:00Z'},
            {'home_team': 'Real Madrid', 'away_team': 'Barcelona', 'competition': 'La Liga', 'utc_date': f'{target_date}T19:00:00Z'},
            {'home_team': 'Bayern Munich', 'away_team': 'Borussia Dortmund', 'competition': 'Bundesliga', 'utc_date': f'{target_date}T17:30:00Z'}
        ]
    import requests
    url = f'https://api.football-data.org/v4/matches?dateFrom={target_date}&dateTo={target_date}'
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

def main(date_str, simulate=False):
    fixtures = get_fixtures_for_date(date_str, simulate=simulate)
    if not fixtures:
        print(f'No fixtures found for {date_str}.')
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
    df.to_csv(f'goal_no_goal_predictions_{date_str}.csv', index=False)
    df.to_html(f'goal_no_goal_predictions_{date_str}.html', index=False)
    print(f'Results saved to goal_no_goal_predictions_{date_str}.html')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python predict_for_date.py YYYY-MM-DD [--simulate]')
        sys.exit(1)
    date_str = sys.argv[1]
    simulate = '--simulate' in sys.argv
    main(date_str, simulate=simulate)
