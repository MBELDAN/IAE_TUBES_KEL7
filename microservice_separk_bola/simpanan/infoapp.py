from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
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
    team = db.Column(db.String(64))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'position': self.position,
            'team': self.team
        }

@app.route('/players', methods=['GET'])
def get_players():
    players = Player.query.all()
    return jsonify([player.to_dict() for player in players])

@app.route('/players/<int:id>', methods=['GET'])
def get_player(id):
    player = Player.query.get_or_404(id)
    return jsonify(player.to_dict())

@app.route('/players', methods=['POST'])
def create_player():
    data = request.json
    player = Player(name=data['name'], age=data['age'], position=data['position'], team=data['team'])
    db.session.add(player)
    db.session.commit()
    return jsonify(player.to_dict()), 201

@app.route('/players/<int:id>', methods=['PUT'])
def update_player(id):
    player = Player.query.get_or_404(id)
    data = request.json
    player.name = data['name']
    player.age = data['age']
    player.position = data['position']
    player.team = data['team']
    db.session.commit()
    return jsonify(player.to_dict())

@app.route('/players/<int:id>', methods=['DELETE'])
def delete_player(id):
    player = Player.query.get_or_404(id)
    db.session.delete(player)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
