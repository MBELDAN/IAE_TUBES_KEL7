from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import requests
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class TopScore(db.Model):
    __tablename__ = 'top_score'
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, unique=True, nullable=False)
    goals = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'player_id': self.player_id,
            'goals': self.goals
        }

@app.route('/top_scores', methods=['GET'])
def get_top_scores():
    min_goals = request.args.get('min_goals')
    max_goals = request.args.get('max_goals')

    if min_goals and max_goals:
        top_scores = TopScore.query.filter(TopScore.goals.between(min_goals, max_goals)).order_by(TopScore.goals.desc()).all()
    elif min_goals:
        top_scores = TopScore.query.filter(TopScore.goals >= min_goals).order_by(TopScore.goals.desc()).all()
    elif max_goals:
        top_scores = TopScore.query.filter(TopScore.goals <= max_goals).order_by(TopScore.goals.desc()).all()
    else:
        top_scores = TopScore.query.order_by(TopScore.goals.desc()).all()

    top_scores_list = [score.to_dict() for score in top_scores]

    # Get player details from player service
    for score in top_scores_list:
        player_info = get_player_info(score['player_id'])
        score['player_info'] = player_info

    return jsonify(top_scores_list)


def get_player_info(player_id):
    try:
        response = requests.get(f"{app.config['PLAYER_SERVICE_URL']}/players/{player_id}")
        if response.status_code == 200:
            return response.json()
        else:
            return {'error': 'Player not found'}
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

if __name__ == '__main__':
    app.run(debug=True, port=app.config['PORT'])
