import requests
import os
import configparser
from datetime import datetime, timedelta, timezone

#this is a vibe coded project, if you find errors, problems, or suggestions, please email me at cyrusjaimes7@gmail.com
CONFIG_FILE = 'config.ini'
config = configparser.ConfigParser()

# 1. Improved check: Does file exist AND have a Username?
config.read(CONFIG_FILE)
has_username = config.has_option('SETTINGS', 'Username')

if not os.path.exists(CONFIG_FILE) or not has_username:
    username = input("Enter Chess.com username: ").strip()
    if not config.has_section('SETTINGS'):
        config.add_section('SETTINGS')
    config.set('SETTINGS', 'Username', username)
    with open(CONFIG_FILE, 'w') as f: 
        config.write(f)
else:
    username = config.get('SETTINGS', 'Username')

def get_activity_dates(username, year, month):
    headers = {'User-Agent': 'StreakTracker/2.0 (Contact: your@email.com)'}
    url = f"https://api.chess.com/pub/player/{username}/games/{year}/{month:02d}"
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        return set()
    return {datetime.fromtimestamp(g['end_time'], tz=timezone.utc).date() for g in resp.json().get('games', [])}

def calculate_true_streak(username):
    today = datetime.now(timezone.utc).date()
    current_date = today
    streak = 0
    
    current_month_dates = get_activity_dates(username, current_date.year, current_date.month)
    
    headers = {'User-Agent': 'StreakTracker/2.0'}
    profile = requests.get(f"https://api.chess.com/pub/player/{username}", headers=headers).json()
    last_online = datetime.fromtimestamp(profile.get('last_online', 0), tz=timezone.utc).date()
    
    while True:
        if current_date in current_month_dates or last_online == current_date:
            streak += 1
            yesterday = current_date - timedelta(days=1)
            if yesterday.month != current_date.month:
                current_month_dates = get_activity_dates(username, yesterday.year, yesterday.month)
            current_date = yesterday
        else:
            break
    return streak

print(f"Calculating streak for {username}...")
current_streak = calculate_true_streak(username)
print(f"Your estimated streak is: {current_streak} days")

# 2. Saving WITHOUT deleting the Username
config.set('SETTINGS', 'Streak', str(current_streak))
with open(CONFIG_FILE, 'w') as f:
    config.write(f)