from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import requests
from config import Config  # Perbaiki import ini

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Player(db.Model):
    __tablename__ = 'player'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    age = db.Column(db.Integer)
    position = db.Column(db.String(64))
    team_id = db.Column(db.Integer)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'position': self.position,
            'team_id': self.team_id
        }

@app.route('/players', methods=['GET'])
def get_players():
    position = request.args.get('position')
    team_id = request.args.get('team_id')
    name = request.args.get('name')
    age = request.args.get('age')

    query = Player.query

    if position:
        query = query.filter_by(position=position)
    if team_id:
        query = query.filter_by(team_id=team_id)
    if name:
        query = query.filter(Player.name.ilike(f'%{name}%'))
    if age:
        query = query.filter_by(age=age)

    players = query.all()
    players_list = [player.to_dict() for player in players]

    # Menambahkan informasi tim dari layanan ranking jika parameter query include_team = true
    include_team = request.args.get('include_team', 'false').lower() == 'true'
    if include_team:
        for player in players_list:
            team_id = player['team_id']
            team_info = get_team_info(team_id)
            player['team_info'] = team_info

    return jsonify(players_list)

@app.route('/players/<int:id>', methods=['GET'])
def get_player(id):
    player = Player.query.get_or_404(id)
    player_dict = player.to_dict()

    # Menambahkan informasi tim dari layanan ranking jika parameter query include_team = true
    include_team = request.args.get('include_team', 'false').lower() == 'true'
    if include_team:
        team_info = get_team_info(player.team_id)
        player_dict['team_info'] = team_info

    return jsonify(player_dict)

def get_team_info(team_id):
    try:
        response = requests.get(f"{app.config['RANKING_SERVICE_URL']}/teams/{team_id}")
        if response.status_code == 200:
            return response.json()
        else:
            return {'error': 'Team not found'}
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

if __name__ == '__main__':
    app.run(debug=True)
