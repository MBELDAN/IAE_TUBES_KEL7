import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/topscoredb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PLAYER_SERVICE_URL = 'http://localhost:5001'
    PORT = 5003
