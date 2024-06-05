from app import app, db
from app import Team

def seed():
    teams = [
        {'name': 'Team A', 'points': 45, 'rank': 1},
        {'name': 'Team B', 'points': 40, 'rank': 2},
        {'name': 'Team C', 'points': 35, 'rank': 3},
        {'name': 'Team D', 'points': 30, 'rank': 4},
        {'name': 'Team E', 'points': 25, 'rank': 5}
    ]

    for team_data in teams:
        team = Team(**team_data)
        db.session.add(team)

    db.session.commit()
    print("Database seeded!")

if __name__ == "__main__":
    with app.app_context():
        seed()
