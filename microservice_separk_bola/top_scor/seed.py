from app import app, db, TopScore

def seed_top_scores():
    with app.app_context():
        scores = [
            {'player_id': 1, 'goals': 20},
            {'player_id': 2, 'goals': 18},
            {'player_id': 3, 'goals': 15},
            {'player_id': 4, 'goals': 12},
            {'player_id': 5, 'goals': 10}
        ]

        for score in scores:
            top_score = TopScore(player_id=score['player_id'], goals=score['goals'])
            db.session.add(top_score)

        db.session.commit()

if __name__ == '__main__':
    seed_top_scores()
