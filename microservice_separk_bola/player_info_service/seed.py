from app import app, db
from app import Player

def seed():
    players = [
        {'name': 'Lionel Messi', 'age': 36, 'position': 'Forward', 'team_id': 1},
        {'name': 'Kevin De Bruyne', 'age': 32, 'position': 'Midfielder', 'team_id': 2},
        {'name': 'Virgil van Dijk', 'age': 32, 'position': 'Defender', 'team_id': 3},
        {'name': 'Thibaut Courtois', 'age': 31, 'position': 'Goalkeeper', 'team_id': 4},
        {'name': 'Robert Lewandowski', 'age': 35, 'position': 'Forward', 'team_id': 5},
        {'name': 'Kylian Mbappé', 'age': 25, 'position': 'Forward', 'team_id': 1},
        {'name': 'Luka Modrić', 'age': 38, 'position': 'Midfielder', 'team_id': 2},
        {'name': 'Sergio Ramos', 'age': 37, 'position': 'Defender', 'team_id': 3},
        {'name': 'Alisson Becker', 'age': 31, 'position': 'Goalkeeper', 'team_id': 4},
        {'name': 'Erling Haaland', 'age': 23, 'position': 'Forward', 'team_id': 5}
    ]

    for player_data in players:
        player = Player(**player_data)
        db.session.add(player)

    db.session.commit()
    print("Database seeded!")

if __name__ == "__main__":
    with app.app_context():
        seed()
