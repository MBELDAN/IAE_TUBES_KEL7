from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import requests
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    points = db.Column(db.Integer)
    rank = db.Column(db.Integer)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'points': self.points,
            'rank': self.rank
        }
        

@app.route('/teams', methods=['GET'])
def get_teams():
    sort_order = request.args.get('sort', 'asc')
    min_points = request.args.get('min_points', type=int)
    max_points = request.args.get('max_points', type=int)
    rank = request.args.get('rank', type=int)

    query = Team.query

    if min_points is not None and max_points is not None:
        query = query.filter(Team.points.between(min_points, max_points))
    elif min_points is not None:
        query = query.filter(Team.points >= min_points)
    elif max_points is not None:
        query = query.filter(Team.points <= max_points)

    if rank is not None:
        query = query.filter_by(rank=rank)

    if sort_order == 'desc':
        teams = query.order_by(Team.rank.desc()).all()
    else:
        teams = query.order_by(Team.rank.asc()).all()

    teams_list = [team.to_dict() for team in teams]

    include_players = request.args.get('include_players', 'false').lower() == 'true'
    if include_players:
        for team in teams_list:
            team['players'] = get_players_for_team(team['id'])

    return jsonify(teams_list)

@app.route('/teams/<int:id>', methods=['GET'])
def get_team(id):
    team = Team.query.get_or_404(id)
    team_dict = team.to_dict()

    include_players = request.args.get('include_players', 'false').lower() == 'true'
    if include_players:
        team_dict['players'] = get_players_for_team(id)

    return jsonify(team_dict)

@app.route('/teams/rank/<int:rank>', methods=['GET'])
def get_team_by_rank(rank):
    teams = Team.query.filter_by(rank=rank).all()
    teams_list = [team.to_dict() for team in teams]

    include_players = request.args.get('include_players', 'false').lower() == 'true'
    if include_players:
        for team in teams_list:
            team['players'] = get_players_for_team(team['id'])

    return jsonify(teams_list)

@app.route('/teams/points/<int:points>', methods=['GET'])
def get_team_by_points(points):
    teams = Team.query.filter_by(points=points).all()
    teams_list = [team.to_dict() for team in teams]

    include_players = request.args.get('include_players', 'false').lower() == 'true'
    if include_players:
        for team in teams_list:
            team['players'] = get_players_for_team(team['id'])

    return jsonify(teams_list)

@app.route('/teams/points', methods=['GET'])
def get_teams_by_points_range():
    min_points = request.args.get('min', type=int)
    max_points = request.args.get('max', type=int)
    
    query = Team.query

    if min_points is not None and max_points is not None:
        query = query.filter(Team.points.between(min_points, max_points))
    elif min_points is not None:
        query = query.filter(Team.points >= min_points)
    elif max_points is not None:
        query = query.filter(Team.points <= max_points)
    
    teams = query.all()
    teams_list = [team.to_dict() for team in teams]

    include_players = request.args.get('include_players', 'false').lower() == 'true'
    if include_players:
        for team in teams_list:
            team['players'] = get_players_for_team(team['id'])

    return jsonify(teams_list)

def get_players_for_team(team_id):
    try:
        response = requests.get(f"{app.config['PLAYER_SERVICE_URL']}/players?team_id={team_id}")
        if response.status_code == 200:
            return response.json()
        else:
            return {'error': 'Players not found'}
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

if __name__ == '__main__':
    app.run(debug=True, port=app.config['PORT'])
