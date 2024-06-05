

from app import app, db, TransferRumor

def seed_transfer_rumors():
    with app.app_context():
        rumors_data = [
            {
                'player_id': 1,
                'source_club': 'Club A',
                'destination_club': 'Club B',
                'transfer_fee': '20M',
                'rumor_details': 'Rumor about Player X moving from Club A to Club B.'
            },
            {
                'player_id': 2,
                'source_club': 'Club C',
                'destination_club': 'Club D',
                'transfer_fee': '30M',
                'rumor_details': 'Rumor about Player Y moving from Club C to Club D.'
            }
        ]

        for rumor_data in rumors_data:
            rumor = TransferRumor(**rumor_data)
            db.session.add(rumor)

        db.session.commit()

if __name__ == '__main__':
    seed_transfer_rumors()
