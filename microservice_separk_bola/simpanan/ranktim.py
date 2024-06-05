from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
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
    teams = Team.query.order_by(Team.rank).all()
    return jsonify([team.to_dict() for team in teams])

@app.route('/teams/<int:id>', methods=['GET'])
def get_team(id):
    team = Team.query.get_or_404(id)
    return jsonify(team.to_dict())

@app.route('/teams', methods=['POST'])
def create_team():
    data = request.json
    team = Team(name=data['name'], points=data['points'], rank=data['rank'])
    db.session.add(team)
    db.session.commit()
    return jsonify(team.to_dict()), 201

@app.route('/teams/<int:id>', methods=['PUT'])
def update_team(id):
    team = Team.query.get_or_404(id)
    data = request.json
    team.name = data['name']
    team.points = data['points']
    team.rank = data['rank']
    db.session.commit()
    return jsonify(team.to_dict())

@app.route('/teams/<int:id>', methods=['DELETE'])
def delete_team(id):
    team = Team.query.get_or_404(id)
    db.session.delete(team)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, port=app.config['PORT'])
