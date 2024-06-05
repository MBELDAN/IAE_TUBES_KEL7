from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# Define the API base URL
BASE_PLAYER_INFO_URL = "http://127.0.0.1:5001"
BASE_RANK_TEAM_URL = "http://127.0.0.1:5002"
BASE_TOP_SCORE_URL = "http://127.0.0.1:5003"
BASE_SCHEDULE_URL = "http://127.0.0.1:5004"
BASE_RUMOR_URL = "http://127.0.0.1:5005"

# Route for the home page
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/players')
def players():
    player_info = requests.get(f"{BASE_PLAYER_INFO_URL}/players").json()
    return render_template('players.html', player_info=player_info)

@app.route('/rankings')
def rankings():
    rank_team = requests.get(f"{BASE_RANK_TEAM_URL}/teams").json()
    return render_template('rankings.html', teams=rank_team)

@app.route('/top-scorers')
def top_scorers():
    top_score = requests.get(f"{BASE_TOP_SCORE_URL}/top_scores").json()
    return render_template('top_scorers.html', top_scores=top_score)

@app.route('/match_schedules', methods=['GET', 'POST'])
def match_schedules():
    if request.method == 'POST':
        match_date = request.form['match_date']
        team_home_id = request.form['team_home_id']
        team_away_id = request.form['team_away_id']
        stadium_id = request.form['stadium_id']
        
        new_match = {
            "match_date": match_date,
            "team_home_id": team_home_id,
            "team_away_id": team_away_id,
            "stadium_id": stadium_id
        }
        
        response = requests.post(f"{BASE_SCHEDULE_URL}/match_schedules", json=new_match)
        if response.status_code == 201:
            return redirect(url_for('match_schedules'))
    
    match_schedules = requests.get(f"{BASE_SCHEDULE_URL}/match_schedules").json()
    teams = requests.get(f"{BASE_RANK_TEAM_URL}/teams").json()
    stadiums = requests.get(f"{BASE_SCHEDULE_URL}/stadiums").json()
    return render_template('match_schedules.html', match_schedules=match_schedules, teams=teams, stadiums=stadiums)

@app.route('/match_schedules/update/<int:match_id>', methods=['POST'])
def update_match_schedule(match_id):
    match_date = request.form['match_date']
    team_home_id = request.form['team_home_id']
    team_away_id = request.form['team_away_id']
    stadium_id = request.form['stadium_id']
    
    updated_match = {
        "match_date": match_date,
        "team_home_id": team_home_id,
        "team_away_id": team_away_id,
        "stadium_id": stadium_id
    }
    
    response = requests.patch(f"{BASE_SCHEDULE_URL}/match_schedules/{match_id}", json=updated_match)
    return redirect(url_for('match_schedules'))

@app.route('/match_schedules/delete/<int:match_id>', methods=['POST'])
def delete_match_schedule(match_id):
    response = requests.delete(f"{BASE_SCHEDULE_URL}/match_schedules/{match_id}")
    return redirect(url_for('match_schedules'))
    
@app.route('/stadiums', methods=['GET', 'POST'])
def stadiums():
    if request.method == 'POST':
        name = request.form['name']
        capacity = request.form['capacity']
        address = request.form['address']
        
        new_stadium = {
            "name": name,
            "capacity": capacity,
            "address": address
        }
        
        response = requests.post(f"{BASE_SCHEDULE_URL}/stadiums", json=new_stadium)
        if response.status_code == 201:
            return redirect(url_for('stadiums'))
    
    stadiums = requests.get(f"{BASE_SCHEDULE_URL}/stadiums").json()
    return render_template('stadiums.html', stadiums=stadiums)

@app.route('/stadiums/update/<int:stadium_id>', methods=['POST'])
def update_stadium(stadium_id):
    name = request.form['name']
    capacity = request.form['capacity']
    address = request.form['address']
    
    updated_stadium = {
        "name": name,
        "capacity": capacity,
        "address": address
    }
    
    response = requests.patch(f"{BASE_SCHEDULE_URL}/stadiums/{stadium_id}", json=updated_stadium)
    return redirect(url_for('stadiums'))

@app.route('/stadiums/delete/<int:stadium_id>', methods=['POST'])
def delete_stadium(stadium_id):
    response = requests.delete(f"{BASE_SCHEDULE_URL}/stadiums/{stadium_id}")
    return redirect(url_for('stadiums'))
    
@app.route('/transfer-rumors')
def transfer_rumors():
    rumors = requests.get(f"{BASE_RUMOR_URL}/transfer_rumors").json()
    return render_template('transfer_rumors.html', rumors=rumors)

if __name__ == '__main__':
    app.run(debug=True)
