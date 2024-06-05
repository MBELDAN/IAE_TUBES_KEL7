from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///transfer_rumors.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class TransferRumor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer)
    source_club = db.Column(db.String(100))
    destination_club = db.Column(db.String(100))
    transfer_fee = db.Column(db.String(20))
    rumor_details = db.Column(db.String(500))

    def to_dict(self):
        return {
            'id': self.id,
            'player_id': self.player_id,
            'source_club': self.source_club,
            'destination_club': self.destination_club,
            'transfer_fee': self.transfer_fee,
            'rumor_details': self.rumor_details
        }

@app.route('/transfer_rumors', methods=['GET'])
def get_transfer_rumors():
    rumors = TransferRumor.query.all()
    return jsonify([rumor.to_dict() for rumor in rumors])

@app.route('/transfer_rumors', methods=['POST'])
def create_transfer_rumor():
    data = request.json
    rumor = TransferRumor(
        player_id=data['player_id'],
        source_club=data['source_club'],
        destination_club=data['destination_club'],
        transfer_fee=data['transfer_fee'],
        rumor_details=data['rumor_details']
    )
    db.session.add(rumor)
    db.session.commit()
    return jsonify(rumor.to_dict()), 201

@app.route('/transfer_rumors/<int:id>', methods=['GET'])
def get_transfer_rumor(id):
    rumor = TransferRumor.query.get_or_404(id)
    return jsonify(rumor.to_dict())

@app.route('/transfer_rumors/<int:id>', methods=['PATCH'])
def update_transfer_rumor(id):
    rumor = TransferRumor.query.get_or_404(id)
    data = request.json
    rumor.source_club = data.get('source_club', rumor.source_club)
    rumor.destination_club = data.get('destination_club', rumor.destination_club)
    rumor.transfer_fee = data.get('transfer_fee', rumor.transfer_fee)
    rumor.rumor_details = data.get('rumor_details', rumor.rumor_details)
    db.session.commit()
    return jsonify(rumor.to_dict())

@app.route('/transfer_rumors/<int:id>', methods=['DELETE'])
def delete_transfer_rumor(id):
    rumor = TransferRumor.query.get_or_404(id)
    db.session.delete(rumor)
    db.session.commit()
    return jsonify({'message': 'Rumor deleted'})

if __name__ == '__main__':
    app.run(debug=True)
