from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import requests

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Stadium(db.Model):
    __tablename__ = 'stadiums'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    capacity = db.Column(db.Integer)
    address = db.Column(db.String(256))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'capacity': self.capacity,
            'address': self.address
        }

class MatchSchedule(db.Model):
    __tablename__ = 'match_schedules'
    id = db.Column(db.Integer, primary_key=True)
    match_date = db.Column(db.Date, nullable=False)
    team_home_id = db.Column(db.Integer, nullable=False)
    team_away_id = db.Column(db.Integer, nullable=False)
    stadium_id = db.Column(db.Integer, db.ForeignKey('stadiums.id'), nullable=False)

    stadium = db.relationship('Stadium', backref=db.backref('matches', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'match_date': self.match_date.isoformat(),
            'team_home_id': self.team_home_id,
            'team_away_id': self.team_away_id,
            'stadium': self.stadium.to_dict()
        }

def get_team_info(team_id):
    try:
        response = requests.get(f"{app.config['TEAM_SERVICE_URL']}/teams/{team_id}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        app.logger.error(f"Error fetching team info: {e}")
        return None

@app.route('/stadiums', methods=['GET'])
def get_stadiums():
    stadiums = Stadium.query.all()
    return jsonify([stadium.to_dict() for stadium in stadiums])

@app.route('/stadiums/<int:id>', methods=['GET'])
def get_stadium(id):
    stadium = Stadium.query.get_or_404(id)
    return jsonify(stadium.to_dict())

@app.route('/stadiums', methods=['POST'])
def create_stadium():
    data = request.json
    stadium = Stadium(
        name=data['name'],
        capacity=data['capacity'],
        address=data['address']
    )
    db.session.add(stadium)
    db.session.commit()
    return jsonify(stadium.to_dict()), 201

@app.route('/stadiums/<int:id>', methods=['PATCH'])
def update_stadium(id):
    stadium = Stadium.query.get_or_404(id)
    data = request.json
    if 'name' in data:
        stadium.name = data['name']
    if 'capacity' in data:
        stadium.capacity = data['capacity']
    if 'address' in data:
        stadium.address = data['address']
    db.session.commit()
    return jsonify(stadium.to_dict())

@app.route('/stadiums/<int:id>', methods=['DELETE'])
def delete_stadium(id):
    stadium = Stadium.query.get_or_404(id)
    db.session.delete(stadium)
    db.session.commit()
    return '', 204

@app.route('/match_schedules', methods=['GET'])
def get_match_schedules():
    match_schedules = MatchSchedule.query.all()
    match_schedules_list = []

    for match in match_schedules:
        match_dict = match.to_dict()
        team_home_info = get_team_info(match.team_home_id)
        team_away_info = get_team_info(match.team_away_id)
        
        if team_home_info:
            match_dict['team_home_info'] = team_home_info
        else:
            match_dict['team_home_info'] = {'error': 'Team information not available'}

        if team_away_info:
            match_dict['team_away_info'] = team_away_info
        else:
            match_dict['team_away_info'] = {'error': 'Team information not available'}

        match_schedules_list.append(match_dict)
    
    return jsonify(match_schedules_list)

@app.route('/match_schedules/<int:id>', methods=['GET'])
def get_match_schedule(id):
    match = MatchSchedule.query.get_or_404(id)
    match_dict = match.to_dict()

    # Get team info from team rank service
    team_home_info = get_team_info(match.team_home_id)
    team_away_info = get_team_info(match.team_away_id)
    
    if team_home_info:
        match_dict['team_home_info'] = team_home_info
    else:
        match_dict['team_home_info'] = {'error': 'Team information not available'}

    if team_away_info:
        match_dict['team_away_info'] = team_away_info
    else:
        match_dict['team_away_info'] = {'error': 'Team information not available'}
    
    return jsonify(match_dict)

@app.route('/match_schedules', methods=['POST'])
def create_match_schedule():
    data = request.json
    match = MatchSchedule(
        match_date=data['match_date'],
        team_home_id=data['team_home_id'],
        team_away_id=data['team_away_id'],
        stadium_id=data['stadium_id']
    )
    db.session.add(match)
    db.session.commit()
    return jsonify(match.to_dict()), 201

@app.route('/match_schedules/<int:id>', methods=['PATCH'])
def update_match_schedule(id):
    match = MatchSchedule.query.get_or_404(id)
    data = request.json
    if 'match_date' in data:
        match.match_date = data['match_date']
    if 'team_home_id' in data:
        match.team_home_id = data['team_home_id']
    if 'team_away_id' in data:
        match.team_away_id = data['team_away_id']
    if 'stadium_id' in data:
        match.stadium_id = data['stadium_id']
    db.session.commit()
    return jsonify(match.to_dict())

@app.route('/match_schedules/<int:id>', methods=['DELETE'])
def delete_match_schedule(id):
    match = MatchSchedule.query.get_or_404(id)
    db.session.delete(match)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, port=app.config['PORT'])
