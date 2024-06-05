import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/playerdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PORT = 5001
    RANKING_SERVICE_URL = 'http://localhost:5002'
